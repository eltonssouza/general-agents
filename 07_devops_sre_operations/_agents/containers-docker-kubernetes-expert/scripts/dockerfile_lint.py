# -*- coding: utf-8 -*-
"""
Skill: dockerfile-linter
Static, read-only, deterministic Dockerfile linter, calibrated by what the Docker
Handbook (DOCKHB, 2021) actually teaches. No network, executes nothing, reads nothing outside the
given file (and, with --context, only checks whether .dockerignore exists).
Each finding carries its origin: [from source] (DOCKHB p.N), [inference] or [extrapolation].
Rules the book does NOT contain (HEALTHCHECK, digest pinning, scan, secrets) appear only as
[extrapolation] and never as "the book says".
Uso: python -I dockerfile_lint.py Dockerfile [--context DIR] [--json]
     cat Dockerfile | python -I dockerfile_lint.py -
Output: findings + 0-100 score; exit code 1 if there is HIGH severity.
"""
import argparse
import json
import os
import re
import sys

SECRET_RE = re.compile(r"(PASSWORD|PASSWD|SECRET|TOKEN|API_?KEY|PRIVATE_?KEY)", re.I)
INSTALL_RE = re.compile(r"\b(apt-get|apt)\s+(-y\s+)?install\b|\bapk\s+add\b|\byum\s+install\b|\bdnf\s+install\b")
REMOVE_RE = re.compile(r"\b(apt-get|apt)\s+(remove|purge|autoremove)\b|\bapk\s+del\b|\brm\s+-rf?v?\b|\bapt-get\s+clean\b")


def parse(text):
    """Returns a list of instructions (lineno, KEYWORD, args), joining backslash continuations."""
    out, buf, start = [], "", None
    for n, raw in enumerate(text.splitlines(), 1):
        line = raw.rstrip()
        if not buf and (not line.strip() or line.lstrip().startswith("#")):
            continue
        if buf == "" :
            start = n
        if line.lstrip().startswith("#"):
            continue
        if line.endswith("\\"):
            buf += line[:-1] + " "
            continue
        buf += line
        parts = buf.strip().split(None, 1)
        if parts:
            out.append((start, parts[0].upper(), parts[1] if len(parts) > 1 else ""))
        buf = ""
    if buf.strip():
        parts = buf.strip().split(None, 1)
        out.append((start, parts[0].upper(), parts[1] if len(parts) > 1 else ""))
    return out


def stages(instrs):
    res, cur = [], None
    for ins in instrs:
        if ins[1] == "FROM":
            cur = {"from": ins, "ins": []}
            res.append(cur)
        elif cur is not None:
            cur["ins"].append(ins)
    return res


def lint(text, context=None):
    instrs = parse(text)
    F = []

    def add(sev, rule, line, msg, fix, origin, pen):
        F.append({"severity": sev, "rule": rule, "line": line, "message": msg, "fix": fix, "origin": origin, "_pen": pen})

    if not instrs:
        add("HIGH", "DF001", 0, "Empty Dockerfile.", "Start with FROM.", "[from source] (DOCKHB p.55)", 40)
        return F
    first = next((i for i in instrs if i[1] != "ARG"), instrs[0])
    if first[1] != "FROM":
        add("HIGH", "DF001", first[0], f"The first instruction is {first[1]}, not FROM.",
            "Every valid Dockerfile starts with FROM (ARG before FROM is an exception in the real syntax: [extrapolation]).",
            "[from source] (DOCKHB p.55)", 40)

    st = stages(instrs)
    for s in st:
        ln, _, args = s["from"]
        img = args.split()[0] if args.split() else ""
        aliases = {m.group(1).lower() for x in st for m in [re.search(r"\s[Aa][Ss]\s+(\S+)\s*$", x["from"][2])] if m}
        if img.lower() != "scratch" and not img.startswith("$") and img.lower() not in aliases:
            name = img.split("@")[0]
            tagpart = name.rsplit("/", 1)[-1]
            if "@sha256:" in img:
                pass
            elif ":" not in tagpart:
                add("MEDIUM", "DF002", ln, f"FROM {img} without a tag (equivalent to :latest).",
                    "Use an explicit version tag. The book warns that latest does not guarantee the latest version; recommending a pin is [extrapolation].",
                    "[from source] (DOCKHB p.86) + [extrapolation] for the pin recommendation", 8)
            elif tagpart.endswith(":latest"):
                add("MEDIUM", "DF002", ln, f"FROM {img} uses :latest.",
                    "Pin a version. The book shows latest in examples (p.55, 77) but warns that the tag does not mean 'most recent' (p.86).",
                    "[from source] (DOCKHB p.86) + [extrapolation] for the pin", 8)
        if re.match(r"(ubuntu|debian|centos|fedora)(:|$)", img.split("/")[-1], re.I):
            add("LOW", "DF017", ln, f"Base {img} is a full distribution.",
                "Consider the Alpine/slim variant to reduce size (in the book: 81.6MB -> 12.8MB); check compatibility (musl vs glibc is [extrapolation]).",
                "[from source] (DOCKHB p.77-80)", 3)

    final = st[-1] if st else {"from": instrs[0], "ins": instrs}
    fins = final["ins"]
    kws = [i[1] for i in fins]

    # USER
    users = [i for i in fins if i[1] == "USER"]
    if not users:
        add("MEDIUM", "DF003", final["from"][0], "Final stage without USER: the container runs as root.",
            "Define a non-root user (e.g. USER node in node images); the book recommends non-root \"whenever possible\" (but some of the book's own images, such as rmbyext and nginx, run as root).",
            "[from source] (DOCKHB p.89)", 10)
    elif users[-1][2].strip().lower() in ("root", "0", "0:0"):
        add("MEDIUM", "DF004", users[-1][0], "Explicit USER root in the final stage.",
            "Run the application as a non-root user.", "[from source] (DOCKHB p.89)", 20)

    # CMD / ENTRYPOINT
    if "CMD" not in kws and "ENTRYPOINT" not in kws:
        add("MEDIUM", "DF016", final["from"][0], "Final stage without CMD or ENTRYPOINT.",
            "Define the default command (CMD) or the executable program (ENTRYPOINT), as in all the book's examples. Inheriting from the base is only valid if intentional.",
            "[inference] from DOCKHB p.54-56, 81-82", 6)
    for ln, kw, args in fins:
        if kw in ("CMD", "ENTRYPOINT") and not args.strip().startswith("["):
            add("LOW", "DF008", ln, f"{kw} in shell form.",
                "Prefer exec form (JSON). The book uses exec form and mentions shell form as an alternative, without condemning it; the technical reason (signals/PID 1) is [extrapolation].",
                "[inference] (DOCKHB p.56) + [extrapolation]", 4)

    # Install without cleanup, in the same layer
    all_ins = [(i, s) for s in st for i in s["ins"]] if st else []
    for ln, kw, args in fins:
        if kw != "RUN":
            continue
        if re.search(r"\b(apt-get|apt)\b.*\binstall\b", args) and not re.search(r"(rm\s+-rf\s+/var/lib/apt/lists|apt-get\s+clean)", args):
            add("MEDIUM", "DF005", ln, "apt-get install without cleaning the cache in the same RUN.",
                "Chain 'apt-get clean && rm -rf /var/lib/apt/lists/*' in the same RUN instruction so the cache is not carried in a layer.",
                "[from source] (DOCKHB p.55-56, 74)", 10)
        if re.search(r"\bapk\s+add\b", args) and "--no-cache" not in args:
            add("MEDIUM", "DF006", ln, "apk add without --no-cache.",
                "Use apk add --no-cache (the book explains that it avoids keeping the downloaded cache).",
                "[from source] (DOCKHB p.78)", 8)
    # install in one RUN and remove in another
    runs = [(ln, a) for ln, kw, a in fins if kw == "RUN"]
    for idx, (ln, a) in enumerate(runs):
        if INSTALL_RE.search(a) and re.search(r"build|dev|g\+\+|gcc|make|\.build-deps", a):
            for ln2, a2 in runs[idx + 1:]:
                if re.search(r"\b(apt-get|apt)\s+(remove|purge)\b|\bapk\s+del\b", a2):
                    add("HIGH", "DF007", ln2, "Build packages installed in one RUN and removed in another: the size stays in the earlier layer.",
                        "Install, compile and remove in the SAME RUN (or use multi-stage). Removing in another layer does not shrink the image.",
                        "[from source] (DOCKHB p.75)", 20)
                    break

    # ADD local
    for ln, kw, args in fins:
        if kw == "ADD" and not re.match(r"https?://", args.strip().split()[0] if args.split() else ""):
            add("LOW", "DF009", ln, "ADD used for a local file.",
                "Prefer COPY for local files. The book only shows ADD for downloading from a URL (and that it does not extract); 'prefer COPY' is [extrapolation].",
                "[extrapolation]; ADD from URL in DOCKHB p.68-69", 3)

    # COPY . . before installing dependencies
    for i, (ln, kw, args) in enumerate(fins):
        if kw == "COPY" and re.match(r"^(\./?|\.)\s+(\./?|\.|/\S*)\s*$", args.strip()):
            later = [a for _, k, a in fins[i + 1:] if k == "RUN" and re.search(r"npm (install|ci)|pip install|yarn|bundle install|composer install", a)]
            if later:
                add("LOW", "DF010", ln, "COPY . . before installing dependencies.",
                    "Copy only the manifest (package.json) first and install; then copy the rest. It is the pattern in the book's examples (the cache gain is [inference]).",
                    "[inference] (pattern in DOCKHB p.88-90, 97)", 4)
            break

    # WORKDIR missing with COPY
    if any(k in ("COPY", "ADD") for k in kws) and "WORKDIR" not in kws:
        add("LOW", "DF014", final["from"][0], "Final stage copies files without WORKDIR (they will land in the root /).",
            "Define a WORKDIR (e.g. /home/node/app); the book reminds that the default is the root and that you do not want files scattered in it.",
            "[from source] (DOCKHB p.66, 89)", 4)

    # Single-stage with a build tool
    if len(st) == 1 and any(k == "RUN" and re.search(r"npm run build|make\b|\./configure|go build|mvn |gradle ", a) for _, k, a in fins):
        add("LOW", "DF013", st[0]["from"][0], "A single stage runs build/compilation: the final image carries the toolchain.",
            "Consider multi-stage (builder + lean final image). The book does this for the JS app (nginx) and for the API (node-gyp).",
            "[from source] (DOCKHB p.96-98, 118-119); the book's alternative for native compilation: install, compile and remove in the same RUN (p.75)", 4)

    # Secrets in ENV/ARG
    for s in st:
        for ln, kw, args in s["ins"]:
            if kw in ("ENV", "ARG"):
                name = re.split(r"[= ]", args.strip(), maxsplit=1)[0]
                val = args.strip()[len(name):].lstrip("= ").strip()
                if SECRET_RE.search(name) and val and not val.startswith("$"):
                    add("HIGH", "DF015", ln, f"{kw} {name} with an embedded value: the secret is recorded in the image/history.",
                        "Do not put secrets in the Dockerfile; inject them at runtime. The book does NOT cover secrets management: the whole recommendation is [extrapolation].",
                        "[extrapolation]", 20)

    if context:
        if not os.path.isfile(os.path.join(context, ".dockerignore")):
            add("LOW", "DF020", 0, f"No .dockerignore in {context}.",
                "Create a .dockerignore (the book excludes .git, node_modules and Docker/Compose files); remember that it does not affect bind mounts.",
                "[from source] (DOCKHB p.101-102)", 3)
    return F


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Static Dockerfile linter (calibrated by the Docker Handbook)")
    ap.add_argument("file", help="Dockerfile path or '-' for stdin")
    ap.add_argument("--context", help="Context directory (only checks .dockerignore)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    text = sys.stdin.read() if a.file == "-" else open(a.file, encoding="utf-8").read()
    F = lint(text, a.context)
    score = max(0, 100 - sum(f["_pen"] for f in F))
    for f in F:
        f.pop("_pen")
    F.sort(key=lambda f: ({"HIGH": 0, "MEDIUM": 1, "LOW": 2}[f["severity"]], f["line"]))
    if a.json:
        print(json.dumps({"score": score, "findings": F}, ensure_ascii=False, indent=1))
    else:
        print(f"Static score: {score}/100  ({len(F)} finding(s))")
        for f in F:
            print(f"\n[{f['severity']}] {f['rule']} line {f['line']}: {f['message']}")
            print(f"   Fix: {f['fix']}")
            print(f"   Origin: {f['origin']}")
        if not F:
            print("No findings from the covered rules. This does NOT attest security: the book does not cover scan, secrets, HEALTHCHECK, etc.")
    sys.exit(1 if any(f["severity"] == "HIGH" for f in F) else 0)


if __name__ == "__main__":
    main()
