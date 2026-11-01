# -*- coding: utf-8 -*-
"""
Skill: docker-command-checker
Static, deterministic validator for docker / docker-compose command lines, calibrated
by the Docker Handbook (DOCKHB, 2021). It does NOT execute anything; it only tokenizes and applies rules.
Each finding carries its origin: [from source] (DOCKHB p.N), [inference], [extrapolation] or [DATED].
Uso: python -I docker_cmd_check.py "docker container run -p 8080:80 nginx"
     python -I docker_cmd_check.py --file comandos.txt        (one command per line; # = comment)
Output: findings; exit code 1 if there is an error (ERROR).
"""
import argparse
import re
import shlex
import sys

# `run`/`create` options that consume a value
RUN_VALUE_OPTS = {"-p", "--publish", "--name", "-e", "--env", "-v", "--volume", "--network", "--net", "-w", "--workdir",
                  "-u", "--user", "--entrypoint", "--restart", "-m", "--memory", "--cpus", "--env-file", "--mount",
                  "-l", "--label", "--hostname", "-h", "--add-host", "--cap-add", "--cap-drop", "--platform", "--pull"}
RUN_BOOL_OPTS = {"-d", "--detach", "--rm", "-i", "--interactive", "-t", "--tty", "--privileged", "--read-only", "--init", "-P"}
BOOK_RUN_OPTS = {"-p", "--publish", "--name", "-e", "--env", "-v", "--volume", "--network", "-d", "--detach", "--rm",
                 "-i", "--interactive", "-t", "--tty"}
INTERACTIVE_IMAGES = {"ubuntu", "debian", "fedora", "alpine", "busybox", "node", "python", "bash", "centos", "deno", "php", "golang", "go"}
LEGACY = {"run": "container run", "ps": "container ls", "rm": "container rm", "stop": "container stop", "start": "container start",
          "kill": "container kill", "restart": "container restart", "exec": "container exec", "logs": "container logs",
          "build": "image build", "images": "image ls", "rmi": "image rm", "pull": "image pull", "push": "image push",
          "tag": "image tag", "history": "image history", "inspect": "(container|image|network|volume) inspect"}
OBJECTS = {"container", "image", "network", "volume"}
DESTRUCTIVE = [
    (("container", "prune"), "Removes ALL stopped containers.", "[from source] (DOCKHB p.42)"),
    (("image", "prune"), "Removes dangling images; with -a it removes all locally cached images.", "[from source] (DOCKHB p.61)"),
    (("network", "prune"), "Removes unused networks.", "[from source] (DOCKHB p.111)"),
]


class R:
    def __init__(self):
        self.items = []

    def add(self, sev, msg, origin):
        self.items.append((sev, msg, origin))


def split_short(tok):
    """-dit -> ['-d','-i','-t'] (known boolean flags only)."""
    if re.fullmatch(r"-[dit]{2,}", tok):
        return ["-" + c for c in tok[1:]]
    return [tok]


def check_publish(val, r):
    if re.fullmatch(r"\d+:\d+(/(tcp|udp))?", val):
        return
    if re.fullmatch(r"(\d{1,3}(\.\d{1,3}){3}):\d+:\d+(/(tcp|udp))?", val) or re.fullmatch(r"\d+(/(tcp|udp))?", val):
        r.add("INFO", f"-p {val}: form outside the <host>:<container> format shown in the book (IP in the bind, or only the container port).",
              "[extrapolation]; book format in DOCKHB p.31")
        return
    r.add("ERROR", f"-p {val}: expected format <host port>:<container port>.", "[from source] (DOCKHB p.31)")


def check_volume(val, r):
    parts = val.split(":")
    if len(parts) == 1:
        if parts[0].startswith("/"):
            r.add("INFO", f"-v {val}: anonymous volume (container path only).", "[from source] (DOCKHB p.95-96)")
        else:
            r.add("ERROR", f"-v {val}: a single field must be an absolute container path (anonymous volume).", "[from source] (DOCKHB p.95)")
        return
    src, dst = parts[0], parts[1]
    if not dst.startswith("/"):
        r.add("ERROR", f"-v {val}: the destination in the container must be an absolute path.", "[from source] (DOCKHB p.51)")
    if "/" in src or src.startswith((".", "~", "$")):
        if not (src.startswith("/") or src.startswith(("$(pwd)", "${PWD}", "$PWD", "~", "$HOME", "%cd%"))):
            r.add("ERROR", f"-v {val}: bind mount with a relative source ({src}); the book requires an absolute path (use $(pwd)/...).", "[from source] (DOCKHB p.51)")
        elif "docker.sock" in src:
            r.add("WARNING", "Mounting docker.sock gives the container control of the daemon.", "[extrapolation]")
    else:
        r.add("INFO", f"-v {val}: '{src}' is treated as a NAMED volume (data persistence, like the book's postgres).", "[from source] (DOCKHB p.113-115)")


def check_run(args, r, sub):
    # args: tokens after 'run'/'create'
    i, opts, image, cmd = 0, [], None, []
    flags = set()
    while i < len(args):
        t = args[i]
        if image is None and t.startswith("-") and t != "-":
            if "=" in t and t.startswith("--"):
                k, v = t.split("=", 1)
                opts.append((k, v))
                i += 1
                continue
            for s in split_short(t):
                if s in RUN_VALUE_OPTS:
                    if i + 1 >= len(args):
                        r.add("ERROR", f"Option {s} has no value.", "[inference]")
                        i += 1
                        break
                    opts.append((s, args[i + 1]))
                    i += 1
                elif s in RUN_BOOL_OPTS:
                    opts.append((s, None))
                    flags.add(s)
                else:
                    opts.append((s, None))
                    r.add("INFO", f"Option {s} is not covered by the book; check the current Docker documentation.", "[extrapolation]")
            i += 1
        elif image is None:
            image = t
            i += 1
        else:
            cmd = args[i:]
            break
    if image is None:
        r.add("ERROR", f"docker {sub}: the image name is missing.", "[from source] (DOCKHB p.29-30)")
        return
    # options after the image
    late = [t for t in cmd if t.startswith("-") and t in (RUN_VALUE_OPTS | RUN_BOOL_OPTS)]
    if late:
        r.add("WARNING", f"Option(s) {late} AFTER the image name: they become entry-point arguments, not docker options.", "[from source] (DOCKHB p.32)")
    for k, v in opts:
        if k in ("-p", "--publish") and v:
            check_publish(v, r)
        elif k in ("-v", "--volume") and v:
            check_volume(v, r)
        elif k in ("-e", "--env") and v:
            if re.match(r"(?i)\w*(PASSWORD|SECRET|TOKEN|KEY)\w*=.+", v):
                r.add("WARNING", f"Literal secret in {k} ({v.split('=')[0]}): it shows up in the shell history and in docker inspect. The book uses this only as a didactic example.",
                      "[extrapolation]; book example in DOCKHB p.112")
        elif k == "--privileged":
            r.add("WARNING", "--privileged removes the container isolation.", "[extrapolation]")
    short = (bool({"-i", "--interactive"} & flags), bool({"-t", "--tty"} & flags))
    base = image.split("/")[-1].split(":")[0].lower()
    if base in INTERACTIVE_IMAGES and not cmd and not (short[0] and short[1]):
        r.add("WARNING", f"Interactive image '{base}' without -it: the container starts and exits without showing anything useful.", "[from source] (DOCKHB p.45-46)")
    if (short[0] != short[1]):
        r.add("WARNING", "Use -i and -t together (-it) for an interactive session with a pseudo-tty.", "[from source] (DOCKHB p.46)")
    if "--rm" in flags and sub == "create":
        pass
    if ":" not in image.split("/")[-1] and "@" not in image:
        r.add("INFO", f"Image '{image}' without a tag: it uses latest, which does not guarantee the most recent version.", "[from source] (DOCKHB p.27-28, 86)")
    elif image.endswith(":latest"):
        r.add("INFO", "Explicit latest tag: it does not guarantee the latest version.", "[from source] (DOCKHB p.86)")
    if not any(k == "--name" for k, _ in opts) and ("-d" in flags or "--detach" in flags):
        r.add("INFO", "Background container without --name: it gets a random name (and will not resolve by DNS on a user-defined network).", "[from source] (DOCKHB p.34, 110)")
    # options outside the book already flagged


def check_build(args, r):
    vals = {"--tag": 1, "-t": 1, "--file": 1, "-f": 1, "--build-arg": 1, "--target": 1, "--platform": 1, "--label": 1}
    i, ctx, tag, file_ = 0, None, None, None
    while i < len(args):
        t = args[i]
        if t in vals:
            if i + 1 < len(args):
                if t in ("-t", "--tag"):
                    tag = args[i + 1]
                if t in ("-f", "--file"):
                    file_ = args[i + 1]
            i += 2
            continue
        if t.startswith("-"):
            r.add("INFO", f"Build option {t} is not covered by the book (it covers --tag/-t and --file/-f).", "[extrapolation]")
            i += 1
            continue
        ctx = t
        i += 1
    if ctx is None:
        r.add("ERROR", "Missing build context (e.g. '.' at the end).", "[from source] (DOCKHB p.57)")
    if tag is None:
        r.add("INFO", "Build without --tag: the image has no name (ID only) and no tag.", "[from source] (DOCKHB p.58-60)")
    elif ":" not in tag:
        r.add("INFO", f"Tag '{tag}' without :version assumes latest.", "[from source] (DOCKHB p.83, 86)")
    if file_ and not file_.endswith("Dockerfile"):
        r.add("INFO", "Non-default Dockerfile name: --file is required (and present).", "[from source] (DOCKHB p.91)")


def check_compose(tokens, r):
    r.add("DATED", "docker-compose (with a hyphen, v1) is the book's form; today the standard is the 'docker compose' plugin. Check the current documentation.", "[DATED] DOCKHB p.12-15, 135")
    rest = tokens[1:]
    sub = next((t for t in rest if not t.startswith("-") and t in
                {"up", "down", "start", "stop", "ps", "exec", "logs", "build", "run", "restart", "pull", "config"}), None)
    if sub is None:
        r.add("INFO", "Subcommand not identified.", "[inference]")
        return
    book = {"up", "down", "start", "stop", "ps", "exec", "logs"}
    if sub not in book:
        r.add("INFO", f"Subcommand '{sub}' is not covered by the book (it covers up, down, start, stop, ps, exec, logs).", "[extrapolation]")
    if sub == "exec" and any(t in ("-it", "-i", "-t") for t in rest):
        r.add("WARNING", "In Compose exec, interactive sessions are automatic; -it is not necessary (at the time).", "[from source] (DOCKHB p.138) [DATED]")
    if sub == "down" and any(t in ("--volumes", "-v") for t in rest):
        r.add("WARNING", "down --volumes REMOVES the named volumes (database data included).", "[from source] (DOCKHB p.140)")
    if sub == "down":
        r.add("INFO", "down removes containers and networks; stop only stops and keeps the containers.", "[from source] (DOCKHB p.139-140)")
    if sub == "up" and not any(t in ("-d", "--detach") for t in rest):
        r.add("INFO", "up without -d stays in the foreground, attached to the logs.", "[inference]; -d em DOCKHB p.135-137")
    if sub == "start":
        r.add("INFO", "start does not create missing containers; use up.", "[from source] (DOCKHB p.137)")
    if sub == "logs" and not any(t in ("-f", "--follow") for t in rest):
        r.add("INFO", "Use -f/--follow to follow in real time.", "[from source] (DOCKHB p.139)")
    if any(t in ("-f", "--file") for t in rest[:rest.index(sub)] if True):
        r.add("INFO", "-f/--file before the subcommand: only needed if the file is not named docker-compose.yaml.", "[from source] (DOCKHB p.137)")


def check(line):
    r = R()
    try:
        tokens = shlex.split(line, posix=True)
    except ValueError as e:
        r.add("ERROR", f"Invalid quotes/escape: {e}", "[inference]")
        return r
    if not tokens:
        return r
    if tokens[0] == "docker-compose":
        check_compose(tokens, r)
        return r
    if tokens[0] != "docker":
        r.add("ERROR", "Not a docker/docker-compose command.", "[inference]")
        return r
    if len(tokens) >= 2 and tokens[1] == "compose":
        r.add("INFO", "'docker compose' (v2 plugin) is not covered by the book, which uses docker-compose; the subcommand syntax is similar.", "[extrapolation]; [DATED]")
        check_compose(["docker-compose"] + tokens[2:], r)
        r.items = [x for x in r.items if x[0] != "DATED"]
        return r
    if len(tokens) < 2:
        r.add("ERROR", "Missing subcommand.", "[inference]")
        return r
    obj = tokens[1]
    if obj in OBJECTS:
        sub = tokens[2] if len(tokens) > 2 else None
        rest = tokens[3:]
        key = (obj, sub)
    elif obj in LEGACY:
        sub, rest = obj, tokens[2:]
        key = (obj, None)
        r.add("INFO", f"Legacy short form 'docker {obj}'; the book presents docker <object> <command> (e.g. docker {LEGACY[obj]}) from 1.13 on, although it itself uses 'docker run' and 'docker ps' in the first examples.",
              "[from source] (DOCKHB p.17-18, 29)")
        obj = {"run": "container", "ps": "container", "rm": "container", "stop": "container", "start": "container", "kill": "container",
               "restart": "container", "exec": "container", "logs": "container", "build": "image", "images": "image", "rmi": "image",
               "pull": "image", "push": "image", "tag": "image", "history": "image"}.get(obj, obj)
        sub = {"ps": "ls", "images": "ls", "rmi": "rm"}.get(sub, sub)
        key = (obj, sub)
    else:
        r.add("INFO", f"Object/command '{obj}' outside what the book covers (container, image, network, volume).", "[extrapolation]")
        return r
    if obj == "container":
        if sub in ("run", "create"):
            check_run(rest, r, sub)
        elif sub in ("stop", "kill", "restart", "start", "rm", "rename", "logs", "inspect"):
            ids = [t for t in rest if not t.startswith("-")]
            if not ids:
                r.add("ERROR", f"container {sub}: the identifier (ID or name) is missing.", "[from source] (DOCKHB p.36-37)")
            if sub == "kill":
                r.add("INFO", "kill sends SIGKILL directly; stop sends SIGTERM and then SIGKILL.", "[from source] (DOCKHB p.37)")
            if sub == "rm" and any(t in ("-f", "--force") for t in rest):
                r.add("WARNING", "rm -f also removes a running container (the book does not cover -f on container rm).", "[extrapolation]")
            if sub == "rename" and len(ids) != 2:
                r.add("ERROR", "container rename <current> <new>.", "[from source] (DOCKHB p.35)")
            if sub == "start" and any(t in ("-a", "-i") for t in rest):
                r.add("INFO", "start is detached by default in the book.", "[from source] (DOCKHB p.38)")
        elif sub == "exec":
            ids = [t for t in rest if not t.startswith("-")]
            if len(ids) < 2:
                r.add("ERROR", "container exec <container> <command>.", "[from source] (DOCKHB p.126)")
            elif ids[1] in ("sh", "bash", "ash") and not any(t in ("-it", "-ti") or (t.startswith("-") and "i" in t and "t" in t) for t in rest):
                r.add("WARNING", f"Interactive shell ({ids[1]}) without -it.", "[from source] (DOCKHB p.126)")
        elif sub in ("ls",):
            pass
        elif sub == "prune":
            pass
        else:
            r.add("INFO", f"container {sub}: not covered by the book.", "[extrapolation]")
    elif obj == "image":
        if sub == "build":
            check_build(rest, r)
        elif sub == "push":
            ids = [t for t in rest if not t.startswith("-")]
            if not ids:
                r.add("ERROR", "image push <repository>:<tag>.", "[from source] (DOCKHB p.86)")
            elif "/" not in ids[0]:
                r.add("WARNING", f"'{ids[0]}' without <user>/ : for Docker Hub the tag needs <user>/<image>:<tag>.", "[from source] (DOCKHB p.84)")
        elif sub in ("rm", "tag", "history", "pull", "ls", "inspect"):
            if sub in ("rm", "history", "tag", "pull") and not [t for t in rest if not t.startswith("-")]:
                r.add("ERROR", f"image {sub}: missing argument.", "[from source] (DOCKHB p.60-62)")
        elif sub == "prune":
            pass
        else:
            r.add("INFO", f"image {sub}: not covered by the book.", "[extrapolation]")
    elif obj == "network":
        if sub in ("create", "rm", "connect", "disconnect"):
            ids = [t for t in rest if not t.startswith("-")]
            need = 2 if sub in ("connect", "disconnect") else 1
            if len(ids) < need:
                r.add("ERROR", f"network {sub}: not enough arguments (connect/disconnect <network> <container>).", "[from source] (DOCKHB p.107-111)")
        elif sub not in ("ls", "inspect", "prune"):
            r.add("INFO", f"network {sub}: not covered by the book.", "[extrapolation]")
        if sub == "create" and any(t.startswith("--driver") or t == "-d" for t in rest):
            r.add("INFO", "The book only uses the bridge driver.", "[from source] (DOCKHB p.105)")
    elif obj == "volume":
        if sub == "create" and not [t for t in rest if not t.startswith("-")]:
            r.add("INFO", "volume create without a name creates an anonymous volume; the book names it (volume create <name>).", "[from source] (DOCKHB p.113-114)")
        elif sub not in ("create", "ls", "inspect", "rm", "prune"):
            r.add("INFO", f"volume {sub}: not covered by the book.", "[extrapolation]")
        if sub == "rm":
            r.add("WARNING", "Removing a volume deletes the persisted data.", "[inference]")
    for k, msg, org in DESTRUCTIVE:
        if key == k:
            extra = " (-a/--all: all cached images)" if k == ("image", "prune") and any(t in ("-a", "--all") for t in rest) else ""
            r.add("WARNING", f"Destructive command: {msg}{extra}", org)
    return r


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Static validator for docker commands (calibrated by the Docker Handbook)")
    ap.add_argument("command", nargs="?", help="Command line in quotes")
    ap.add_argument("--file", help="File with one command per line")
    a = ap.parse_args()
    lines = []
    if a.file:
        lines = [l.strip() for l in open(a.file, encoding="utf-8") if l.strip() and not l.strip().startswith("#")]
    elif a.command:
        lines = [a.command]
    else:
        ap.print_help()
        return
    errs = 0
    for l in lines:
        r = check(l)
        print(f"$ {l}")
        if not r.items:
            print("  OK: no findings from the covered rules.")
        for sev, msg, org in r.items:
            print(f"  [{sev}] {msg}\n         Origin: {org}")
            errs += sev == "ERROR"
        print()
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
