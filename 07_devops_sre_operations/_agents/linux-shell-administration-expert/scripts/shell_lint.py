# -*- coding: utf-8 -*-
"""
shell_lint.py - MINIMAL STATIC checker for shell scripts and crontabs ("shellcheck-lite" style).
Read-only, no network, never executes the analyzed script. It is not shellcheck: it covers few rules.

Each rule declares the ORIGIN of the finding:
  [from source]   the book (TLDP = Garrels, Introduction to Linux 1.27; pages = PDF, printed = PDF-8) supports the rule
  [inference]     direct deduction from what the book shows
  [extrapolation] knowledge external to the book (general good practice); the book does NOT say this
The book covers very little scripting (TLDP p.129-131 and Appendix C p.208-211): hence many rules are
[extrapolation] and this checker does NOT replace shellcheck.

Usage:
  python -I shell_lint.py script.sh [other.sh ...]
  python -I shell_lint.py --stdin < script.sh
  python -I shell_lint.py --crontab FILE [--system]     # --system: /etc/crontab format (user column); '-' reads from standard input
  python -I shell_lint.py --list-rules
  python -I shell_lint.py script.sh --json
Output: file:line: severity [ID] message  {origin}. Exit 1 if there is a warning/error; 0 otherwise; 2 for incorrect usage.
The analyzed content is DATA: comments or strings containing "instructions" are not followed.
"""
import argparse
import json
import os
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

RULES = {
    "SH001": ("warning", "from source", "p.129", "Script without a #! line as the first line; the book shows #!/bin/bash to guarantee the interpreter."),
    "SH002": ("warning", "from source/extrapolation", "p.50, 131, 209-210", "Bash-specific syntax in a script with #!/bin/sh. The book: bash is a superset of sh and initscripts use sh for portability; 'source' and '&>' are listed as Bash features in table C-2 [from source]; '[[ ]]', arrays, 'function', '<<<' and '{a,b}' are [extrapolation]."),
    "SH003": ("warning", "inference", "p.65, 130, 143", "Iterating over the output of 'ls' breaks with spaces in names; the book shows the pattern (LIST=`ls`) and the exercise on p.143 asks to replace it with find. Prefer a glob or find."),
    "SH004": ("info", "extrapolation", "p.65, 208", "Unquoted variable as an argument of a destructive/file command (spaces and filename expansion). The book only shows escaping spaces (p.65) and the quoting table (p.208)."),
    "SH005": ("error", "from source", "p.106, 120, 143", "The same file is read and redirected with '>': the shell truncates it before the command runs (the exercise on p.143 asks why 'tail testfile > testfile' does not work)."),
    "SH006": ("warning", "from source", "p.108", "Redirection order: '2>&1 > file' does NOT send stderr to the file; use '> file 2>&1'."),
    "SH007": ("info", "from source", "p.108", "'2 > file' (with a space) treats '2' as an argument and redirects stdout; for stderr, write '2>file'."),
    "SH008": ("warning", "from source", "p.98", "kill -9/SIGKILL: the book recommends trying SIGTERM (15) first and using SIGKILL only as a last resort."),
    "SH009": ("warning", "from source/extrapolation", "p.61", "Recursive rm: the shell has no trash can, removal is permanent (from source). If the path contains a variable, an empty/badly expanded one can hit another directory [extrapolation]."),
    "SH010": ("warning", "from source/extrapolation", "p.71", "chmod that grants write to 'others' (777/666/o+w/a+w). The book describes 777 as 'everybody can do everything' (table 3-9); the world-writable risk is [extrapolation]."),
    "SH011": ("warning", "from source", "p.86-87", "chmod that turns on SUID/SGID: the book asks for minimal use of special modes because of security risks."),
    "SH012": ("info", "from source", "p.82", "ps | grep may list the grep itself; the book points to pgrep as an alternative."),
    "SH013": ("info", "from source/inference", "p.107", "cat file | command: the book calls the 'cat file | mail' form the beginner's version and prefers '<' (command < file)."),
    "SH014": ("info", "from source/extrapolation", "p.55", "Use of /tmp: the book warns that /tmp can be cleaned without notice and suggests /var/tmp for temporary files; predictable names in /tmp are a risk (mktemp) [extrapolation]."),
    "SH015": ("info", "from source", "p.131", "case without a default branch '*)': the book's initscript uses '*)' to show usage and exit with exit 1."),
    "SH016": ("info", "from source", "p.63", "find ... -exec rm {} \\; calls rm once per file; the book suggests find | xargs rm for fewer executions (and testing the selection first)."),
    "SH017": ("warning", "from source", "p.180, 184, 192", "telnet/rsh/rlogin/rcp (and non-anonymous FTP) send passwords unencrypted; the book says to use ssh/scp/sftp."),
    "SH018": ("warning", "extrapolation", "p.179", "Credential embedded in a URL (user:password@host). The book itself shows this in http_proxy (p.179), but storing a password in a script/rc file is bad practice [extrapolation]."),
    "SH019": ("info", "from source", "p.70", "Script file without the execute bit: the book shows 'bad interpreter: Permission denied' solved with chmod u+x."),
    "CR001": ("error", "from source", "p.101", "crontab: wrong number of time fields (there are 5: min hour day-of-month month day-of-week; /etc/crontab also has the user column)."),
    "CR002": ("error", "from source", "p.101", "crontab: value out of range (min 0-59, hour 0-23, day 1-31, month 1-12, day-of-week 0-7 with 0 and 7 = Sunday)."),
    "CR003": ("info", "extrapolation", "p.101", "crontab: syntax beyond what the book describes (steps */n, month/day names, @reboot/@daily)."),
    "CR004": ("info", "from source", "p.102", "crontab: without redirection, the command output is sent by e-mail to the crontab owner."),
    "CR005": ("info", "inference", "p.101", "crontab: command without an absolute path and without PATH defined in the file (the book's example crontab defines SHELL, PATH and MAILTO)."),
    "CR006": ("warning", "extrapolation", "p.101", "crontab: '%' in the command is treated by cron as a newline (escape it with \\%). The book does not mention this."),
    "CR007": ("info", "inference", "p.100", "crontab: time on the hour. The book recommends 'strange' times for 'at' jobs because system jobs run at round hours; by analogy this applies to cron."),
}

NOT_COVERED = [
    "quoting variables in general and handling word splitting/globbing (only 2 points in the book)",
    "set -e / set -u / set -o pipefail, trap for cleanup",
    "[[ ]], arrays, functions, getopts, here-doc, process substitution",
    "$(...) vs backticks (the book uses backticks; table C-2 only lists backticks for sh)",
    "shellcheck, shfmt, bats, script tests",
    "in-depth POSIX portability, dash vs bash",
]


class Finding:
    def __init__(self, path, line, rid, extra=""):
        sev, origin, pages, msg = RULES[rid]
        self.path, self.line, self.rid = path, line, rid
        self.sev, self.origin, self.pages = sev, origin, pages
        self.msg = msg + (" " + extra if extra else "")

    def as_dict(self):
        return dict(file=self.path, line=self.line, id=self.rid, severity=self.sev,
                    origin=self.origin, pages=f"TLDP {self.pages}", message=self.msg)

    def __str__(self):
        return f"{self.path}:{self.line}: {self.sev} [{self.rid}] {self.msg}  {{{self.origin} (TLDP {self.pages})}}"


def mask_quotes(s):
    """Returns (masked, raw_without_comment). Masked: the content of '...' and "..." becomes 'x'; comments removed."""
    out, i, q = [], 0, None
    end = len(s)
    while i < len(s):
        c = s[i]
        if q:
            if c == "\\" and q == '"' and i + 1 < len(s):
                out.append("xx")
                i += 2
                continue
            if c == q:
                q = None
                out.append(c)
            else:
                out.append("x")
        else:
            if c == "\\" and i + 1 < len(s):
                out.append(s[i:i + 2])
                i += 2
                continue
            if c in "'\"":
                q = c
                out.append(c)
            elif c == "#" and (i == 0 or s[i - 1] in " 	;"):
                end = i
                break
            else:
                out.append(c)
        i += 1
    return "".join(out), s[:end]


def logical_lines(text):
    """Returns [(starting_line_number, text)] joining continuations and removing here-doc bodies."""
    res, buf, start, heredoc = [], "", 0, None
    for n, raw in enumerate(text.splitlines(), 1):
        if heredoc:
            if raw.strip() == heredoc:
                heredoc = None
            continue
        line = raw
        if not buf:
            start = n
        if line.rstrip().endswith("\\"):
            buf += line.rstrip()[:-1] + " "
            continue
        buf += line
        m = re.search(r"<<-?\s*['\"]?([A-Za-z_][A-Za-z0-9_]*)['\"]?", buf)
        if m:
            heredoc = m.group(1)
        res.append((start, buf))
        buf = ""
    if buf:
        res.append((start, buf))
    return res


def lint_shell(text, path, check_exec=None):
    f = []
    lines = text.splitlines()
    if not lines or not lines[0].startswith("#!"):
        f.append(Finding(path, 1, "SH001"))
    shebang = lines[0] if lines and lines[0].startswith("#!") else ""
    is_sh = bool(re.search(r"(/bin/sh|/usr/bin/env\s+sh)\b\s*$", shebang.strip()))
    case_depth = []
    for n, raw in logical_lines(text):
        code, raw = mask_quotes(raw)
        if not code.strip():
            continue
        c = code
        # SH002
        if is_sh:
            toks = []
            if re.search(r"(^|[;&|]\s*|\s)source\s+\S", c):
                toks.append("'source' (use '. file'; table C-2, p.210)")
            if "&>" in c:
                toks.append("'&>' (use '> file 2>&1'; table C-2, p.209)")
            if re.search(r"\[\[", c):
                toks.append("'[[ ]]' [extrapolation]")
            if re.search(r"<<<", c):
                toks.append("'<<<' [extrapolation]")
            if re.search(r"(^|\s)function\s+\w+", c):
                toks.append("'function name' [extrapolation]")
            if re.search(r"\b\w+=\(", c) or re.search(r"\$\{\w+\[", c):
                toks.append("arrays [extrapolation]")
            if re.search(r"\{[^{}\s$]+,[^{}\s]+\}", c):
                toks.append("brace expansion {a,b} [extrapolation]")
            if toks:
                f.append(Finding(path, n, "SH002", "Found: " + "; ".join(toks) + "."))
        # SH003
        if re.search(r"\bfor\s+\w+\s+in\s+[^;]*(\$\(\s*ls\b|`\s*ls\b)", c):
            f.append(Finding(path, n, "SH003"))
        if re.search(r"\b\w+=\s*(`\s*ls\b|\$\(\s*ls\b)", c):
            f.append(Finding(path, n, "SH003", "(assignment of the ls output to a variable)"))
        # SH004
        m = re.search(r"\b(rm|mv|cp|chmod|chown|chgrp|ln|mkdir|rmdir|touch)\b([^|;&]*)", c)
        if m and re.search(r"(?<![\\\"'])\$\{?\w+", m.group(2)):
            f.append(Finding(path, n, "SH004"))
        # SH005
        for mm in re.finditer(r"(?<![>2&0-9])>(?![>&])\s*([^\s;|&<>]+)", c):
            target = mm.group(1).strip("\"'")
            before = c[:mm.start()].replace("|", " ").split()
            if target and target not in ("/dev/null", "-") and not target.startswith(("&", "$("))                     and target in [t.strip("\"'") for t in before[1:]] and not target.startswith("-"):
                f.append(Finding(path, n, "SH005", f"(file: {target})"))
                break
        m2 = re.search(r"<\s*([^\s;|&<>]+).*?(?<![>2&0-9])>(?![>&])\s*([^\s;|&<>]+)", c)
        if m2 and m2.group(1) == m2.group(2) and m2.group(1) != "/dev/null":
            f.append(Finding(path, n, "SH005", f"(file: {m2.group(1)})"))
        # SH006 / SH007
        if re.search(r"2>&1\s*>(?!&)\s*\S", c):
            f.append(Finding(path, n, "SH006"))
        if re.search(r"(^|\s)2\s+>+\s*\S", c) and not re.search(r"\becho\b", c):
            f.append(Finding(path, n, "SH007"))
        # SH008
        if re.search(r"\bkill\s+(-9\b|-KILL\b|-SIGKILL\b|-s\s+(9|KILL|SIGKILL)\b)", c):
            f.append(Finding(path, n, "SH008"))
        # SH009
        if re.search(r"\brm\s+(-[a-zA-Z]*[rR][a-zA-Z]*|--recursive)\b", c):
            extra = ""
            if re.search(r"\brm\s+-\S+\s+[\"']?[^;|&]*\$\{?\w+", raw):
                extra = "The path contains a variable."
            f.append(Finding(path, n, "SH009", extra))
        # SH010 / SH011
        mc = re.search(r"\bchmod\s+((?:-\w+\s+)*)(\S+)", c)
        if mc:
            mode = mc.group(2)
            world = suid = False
            if re.fullmatch(r"[0-7]{3,4}", mode):
                v = int(mode, 8)
                world = bool(v & 0o002)
                suid = bool(v & 0o6000)
            else:
                for cl in mode.split(","):
                    m3 = re.fullmatch(r"([ugoa]*)([+=])([rwxst]*)", cl)
                    if m3:
                        who, op, perms = m3.groups()
                        if "w" in perms and (who in ("a", "o", "ugo", "go", "ou") or (op == "=" and who == "")):
                            world = True
                        if "s" in perms and ("u" in who or "g" in who):
                            suid = True
            if world:
                f.append(Finding(path, n, "SH010"))
            if suid:
                f.append(Finding(path, n, "SH011"))
        # SH012
        if re.search(r"\bps\b[^|;]*\|\s*grep\b", c) and not re.search(r"grep\s+-v\s+grep|grep\s+['\"]?\[\w\]", raw):
            f.append(Finding(path, n, "SH012"))
        # SH013
        if re.match(r"^\s*cat\s+[^\s|<>;&-][^\s|<>;&]*\s*\|", c):
            f.append(Finding(path, n, "SH013"))
        # SH014
        if re.search(r"(?<![\w/.])/tmp\b", raw):
            f.append(Finding(path, n, "SH014"))
        # SH015 (case)
        if re.search(r"(^|[;&|]\s*)case\s+.+\s+in\s*$", c) or re.search(r"(^|[;&|]\s*)case\s+.+\s+in\b", c):
            case_depth.append([n, False])
        if case_depth and re.match(r"^\s*\*\)", c):
            case_depth[-1][1] = True
        if case_depth and re.search(r"(^|[;&|\s])esac\b", c):
            start, has_default = case_depth.pop()
            if not has_default:
                f.append(Finding(path, start, "SH015"))
        # SH016
        if re.search(r"\bfind\b.*-exec\s+rm\b.*(\\;|\\ ;)", raw):
            f.append(Finding(path, n, "SH016"))
        # SH017
        if re.search(r"(^|[;&|(]\s*|\bsudo\s+)(telnet|rsh|rlogin|rcp)\b", c) or re.search(r"(^|[;&|(]\s*)ftp\b", c):
            f.append(Finding(path, n, "SH017", "(anonymous FTP is the exception cited by the book, p.180)." if re.search(r"\bftp\b", c) else ""))
        # SH018
        if re.search(r"://[^/\s:@\"']+:[^/\s@\"']+@", raw):
            f.append(Finding(path, n, "SH018"))
    if check_exec is False:
        f.append(Finding(path, 1, "SH019"))
    f.sort(key=lambda x: (x.line, x.rid))
    return f


FIELD_RANGES = [("minute", 0, 59), ("hour", 0, 23), ("day of month", 1, 31), ("month", 1, 12), ("day of week", 0, 7)]
NAMES = {"jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", "sun", "mon", "tue", "wed", "thu", "fri", "sat"}


def check_field(tok, lo, hi):
    """Returns (ok, uses_extrapolation)."""
    extra = False
    for part in tok.split(","):
        step = None
        if "/" in part:
            part, step = part.split("/", 1)
            extra = True
            if not step.isdigit():
                return False, extra
        if part == "*":
            continue
        if part.lower() in NAMES:
            extra = True
            continue
        m = re.fullmatch(r"(\d+)(?:-(\d+))?", part)
        if not m:
            if "-" in part and all(x.lower() in NAMES for x in part.split("-")):
                extra = True
                continue
            return False, extra
        a = int(m.group(1))
        b = int(m.group(2)) if m.group(2) else a
        if a < lo or b > hi or a > b:
            return False, extra
    return True, extra


def lint_crontab(text, path, system=False):
    f = []
    has_path = any(re.match(r"^\s*PATH\s*=", l) for l in text.splitlines())
    for n, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*\s*=", line):
            continue
        toks = line.split()
        if toks[0].startswith("@"):
            f.append(Finding(path, n, "CR003", "(@-shortcuts)"))
            cmd_toks = toks[2:] if system else toks[1:]
            cmd = " ".join(cmd_toks)
        else:
            need = 5 + (1 if system else 0) + 1
            if len(toks) < need:
                f.append(Finding(path, n, "CR001", f"(found {len(toks)} fields; minimum expected {need} including the command)."))
                continue
            ok_all = True
            for i, (nm, lo, hi) in enumerate(FIELD_RANGES):
                ok, extra = check_field(toks[i], lo, hi)
                if extra:
                    f.append(Finding(path, n, "CR003", f"(field {nm}: '{toks[i]}')"))
                if not ok:
                    ok_all = False
                    if toks[i].isalpha() and toks[i].lower() not in NAMES:
                        f.append(Finding(path, n, "CR001", f"(field {nm} = '{toks[i]}' looks like a user/command: is a time field missing?)"))
                    else:
                        f.append(Finding(path, n, "CR002", f"(field {nm}: '{toks[i]}')"))
            cmd = " ".join(toks[(6 if system else 5):])
            if ok_all and re.fullmatch(r"0", toks[0]) and re.fullmatch(r"\d+", toks[1]):
                f.append(Finding(path, n, "CR007"))
        if cmd:
            first = cmd.split()[0]
            if "%" in cmd and "\\%" not in cmd:
                f.append(Finding(path, n, "CR006"))
            if ">" not in cmd and "|" not in cmd and "mail" not in cmd:
                f.append(Finding(path, n, "CR004"))
            if not first.startswith("/") and not has_path and not first.startswith(("cd", "[", "(")):
                f.append(Finding(path, n, "CR005"))
    return f


def main():
    ap = argparse.ArgumentParser(description="Minimal static checker for shell scripts/crontabs, calibrated by the TLDP book.")
    ap.add_argument("files", nargs="*")
    ap.add_argument("--stdin", action="store_true", help="reads the script from standard input")
    ap.add_argument("--crontab", metavar="ARQ", help="analyzes a crontab file")
    ap.add_argument("--system", action="store_true", help="with --crontab: /etc/crontab format (with user)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--list-rules", action="store_true")
    a = ap.parse_args()

    if a.list_rules:
        for rid, (sev, origin, pages, msg) in RULES.items():
            print(f"{rid} [{sev}] {{{origin} (TLDP {pages})}} {msg}")
        print("\nNOT COVERED BY THE BOOK NOR BY THIS CHECKER (use shellcheck):")
        for x in NOT_COVERED:
            print("  - " + x)
        return 0

    findings = []
    try:
        if a.crontab:
            if a.crontab == "-":
                findings += lint_crontab(sys.stdin.read(), "<stdin>", a.system)
            else:
                with open(a.crontab, "r", encoding="utf-8", errors="replace") as fh:
                    findings += lint_crontab(fh.read(), a.crontab, a.system)
        if a.stdin:
            findings += lint_shell(sys.stdin.read(), "<stdin>")
        for p in a.files:
            with open(p, "r", encoding="utf-8", errors="replace") as fh:
                text = fh.read()
            x_ok = None
            if os.name != "nt":
                x_ok = os.access(p, os.X_OK)
            findings += lint_shell(text, p, x_ok)
    except OSError as e:
        print("ERROR: " + str(e))
        return 2
    if not (a.crontab or a.stdin or a.files):
        ap.print_help()
        return 2
    if a.json:
        print(json.dumps([x.as_dict() for x in findings], ensure_ascii=False, indent=1))
    else:
        for x in findings:
            print(x)
        n = len(findings)
        print(f"-- {n} finding(s). Minimal checker: absence of findings does NOT prove the script is correct.")
    return 1 if any(x.sev in ("warning", "error") for x in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
