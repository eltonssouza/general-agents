# Shell environment, variables, setup files, prompt and scripts (Ch. 7, 7.1-7.4; Appendices B and C)

Pages = PDF (printed + 8). Abbreviation TLDP. Support: `scripts/shell_lint.py`.

## Shell types
- sh (Bourne, small), **bash** (GNU standard, superset of sh: what runs in sh runs in bash, but not the reverse), csh, tcsh, ksh; all the book's examples use bash [from source] (TLDP p.50).
- `/etc/shells` lists the shells; the user's default shell is in `/etc/passwd`; `echo $SHELL` shows the current one; `/bin/sh` is usually a link to Bash in compatibility mode [from source] (TLDP p.50-51).
- The shell is described as a language for conversing with the system (unlike the GUI, where the computer leads); it allows automation [from source] (TLDP p.50).

## Environment variables
- Programs need to know things like the terminal (`TERM`), editor, shell (`SHELL`); `printenv` lists them [from source] (TLDP p.122).
- **Environment variables are inherited** by any program started (a copy that the child can change and pass on); ordinary shell variables are not [from source] (TLDP p.122).
- Assigning (`PATH=$PATH:/opt/FlightGear/bin`) is **not enough**: without `export` the value does not reach other programs (the `runfgfs: command not found` example); in Bash: `export VARIABLE=value` in one step; it also applies to `MANPATH` [from source] (TLDP p.123).
- Table 7-1: DISPLAY, EDITOR, HISTSIZE, HOME, HOSTNAME, LANG, LD_LIBRARY_PATH, LOGNAME, MAIL, MANPATH, PAGER, PATH, PS1, PS2, PWD, SHELL, TERM, UID, USER, VISUAL... [from source] (TLDP p.124). By convention, names are in uppercase.
- To make it permanent, put the lines in the setup files (below) [from source] (TLDP p.123).

## Bash startup files
- Interactive login: login authenticates, sets the environment and starts the shell; bash reads `/etc/profile` and then the **first** existing and readable one among `~/.bash_profile`, `~/.bash_login`, `~/.profile`; on exit, it reads `~/.bash_logout` [from source] (TLDP p.124-125). `.bashrc` is the personal counterpart of `/etc/bashrc` (p.124).
- Examples (RedHat of the time): `/etc/profile` sets PATH (sbin for root), `ulimit -S -c 0` (no core dumps), USER, LOGNAME, MAIL, HOSTNAME, HISTSIZE, INPUTRC, and does the `export`; it reads `/etc/profile.d/*.sh`; `.bash_profile` does `source ~/.bashrc`; `/etc/bashrc` sets umask (002 if group = user and uid > 99; otherwise 022) and the prompt [from source] (TLDP p.125-127) [DATED: RedHat/2008-specific content].
- `source` applies the file to the current shell (TLDP p.126). `.bash_logout` can clear the terminal (p.127).
- Seeing what changed: the book tells you to keep `info bash` at hand (p.127).

## Prompt (PS1)
Save the prompt (`MYPROMPT=$PS1`), test it on the command line and only then fix it in `~/.bashrc`; sequences such as `\u`, `\h`, `\w` (full path), `\W` (name only), `\t`, `\j`, `\d`, `\!`; colors with `\[\033[1;35m\]...\[\033[0m\]` [from source] (TLDP p.128-129). More in the Bash-Prompt HOWTO (p.129).

## Organization and space (7.1)
Personal `bin`, directories by theme, `chmod 700` on private ones, sensible names [from source] (TLDP p.119). Emptying (`> file`), `touch`, `tail -5 ... > new`, logs (remove, limit, symlink to /dev/null, with caution on boot/cron programs), `.forward`, symlinks instead of copies, `ulimit -a`, core dumps, z* tools (zgrep, zcat, bzless) for compressed files [from source] (TLDP p.120-122).

## Shell scripts: what the book really teaches
The book **is not a scripting course**: it has about 3 pages (TLDP p.129-131) and points to a Bash course by the same author and to *Advanced Bash Scripting* (p.131).
- Script = text file with commands; it becomes executable with `chmod`; when running `script ARGS` Bash creates a subshell (equivalent to `bash script ARGS`); `$0` is the script's name, the arguments are the positional parameters [from source] (TLDP p.129).
- `#!` on the first line chooses the interpreter (`#!/bin/bash` guarantees Bash; it can be awk, perl...) [from source] (TLDP p.129).
- Examples: `echo "Hello $USER"`; `who | cut -d " " -f 1 | sort -u`; `.old` copy script with `LIST=\`ls\``, `for i in $LIST; do ... cp $ORIG $DEST; echo "copied $i"; done`; `mv * *.old` does not work (TLDP p.130). `echo` after doubtful steps helps find the error (p.130).
- Init script with `case "$1" in start|stop|status|restart|*)`, functions from a library (`. /etc/rc.d/init.d/functions`), `exit 1` on wrong usage and `exit 0` on success; uses `#!/bin/sh` for portability; Bash called as `sh` runs in POSIX mode [from source] (TLDP p.130-131).
- Exercise: the script on p.130 generates errors with directories; adapt it with `find` to pick up only regular files (TLDP p.143).
- Limitations to declare: the book uses `for i in $LIST` without quotes and backticks for command substitution; it **does not teach** quoting variables, `set -e`, `trap`, `getopts`, functions with scope, `[[ ]]`, arrays, here-docs or `[ ]` tests (table C-2 shows `if [ $i -eq 5 ]` only as an example of a condition, TLDP p.211). All advice beyond that is `[extrapolation]`.

## Appendix B (DOS → Linux) and C (shell features)
- B-1: `cls`→`clear`, `copy`→`cp`, `del`→`rm`, `dir`→`ls`, `edit`→`vim`, `fc`→`diff`, `find`→`grep`, `format`→`mke2fs`/`mformat`, `mem`→`free`, `move`/`ren`→`mv`, `more`→`more`/`less`, `<cmd> /?`→`man cmd`/`--help` [from source] (TLDP p.207).
- C-1 (common to every shell): `> >> < << |`, `&`, `;`, `* ? [ ]`, `( )`, backtick, `" "` (partial quotes: allow expansion), `' '` (full quotes), `\`, `$var`, `$$` (PID), `$0`, `$n`, `$*`, `#`; built-ins: bg, break, cd, continue, echo, eval, exec, fg, jobs, kill, newgrp, shift, stop, suspend, time, umask, unset, wait [from source] (TLDP p.208-209).
- C-2 (differences): redirecting stdout and stderr (`> file 2>&1` in sh; `&> file` or `> file 2>&1` in bash; `>& file` in csh), `` `cmd` `` vs `$(cmd)` (the table lists only the backtick for sh), assignment and `export`, `"$@"`, `$#`, `$?`, `$!`, `. file` vs `source file`, alias, case/esac, for/do, history (`!!`, `!str`), `trap`, `read`, `while`/`until`, `ulimit`, hash [from source] (TLDP p.209-211) [DATED: today `$()` is POSIX].
- Bash incorporates features from other shells; there are no blank cells in the bash column (p.211).

## Localization (7.4)
`loadkeys` (text), `XkbLayout` in X (back up before editing), `setfont`, NTP (`ntpd`, `ntpdate` with the daemon stopped), `tzconfig`, `LANG`/`LANGUAGE`, default `en_US.UTF-8`; UTF-8 problems on old systems: `recode` or a temporary `export LANG=en_US` [from source] (TLDP p.134-136) [DATED: today timedatectl/localectl/chrony].
