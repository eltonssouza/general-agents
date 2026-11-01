# Operational procedures (step by step, based on the book)

Pages = PDF (printed + 8). Abbreviation TLDP. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

## P1. "command not found" or the wrong program runs
1. `echo $PATH` to see the order; 2. `which -a command` (or `which command`) to see who answers and whether it is an alias; 3. if the program is in a directory outside the PATH, run it with the full path or `export PATH=$PATH:/dir`; if a personal program shadows the system's, rename it, use the full path or change the PATH order; 4. to persist, edit `~/.bashrc`/`~/.bash_profile` [from source] (TLDP p.48-49, 62, 123).

## P2. "Permission denied"
1. `ls -l file` (and `ls -ld` on the directories in the path); 2. check owner/group/others and the `x` bit (a script without `x` gives "bad interpreter: Permission denied"); 3. `id` to see your groups; 4. `chmod u+x` or the numeric mode from table 3-9; 5. "works as root" or "worked yesterday" point to permissions [from source] (TLDP p.69-71). Use `scripts/chmod_calc.py`. On a directory, a missing `x` blocks access (TLDP p.72).

## P3. Sharing files in a group
`mkdir` the directory → `chgrp group dir` → `chmod 2775 dir` (SGID to inherit the group; the 2 in the 4th digit is `[inference]` from TLDP p.71 and 74) → umask 002 so the group can write; files moved in from outside **keep** their owner/group (TLDP p.72, 74). Alternative: `newgrp` (TLDP p.71-72).

## P4. Process consuming resources
1. `top` (or `ps -ef | grep`); 2. if it must keep running: `renice` (not on interactive ones); 3. if it must stop: `kill -15 PID`, then SIGINT, finally `kill -9 PID`; 4. confirm with `ps -ef | grep PID`; 5. for hung graphical programs, `xkill` (SIGKILL) [from source] (TLDP p.95, 98-99). Also look at the load (`uptime`) and compare it with what is "normal" on the machine (TLDP p.94).

## P5. Run something later or periodically
- Once: `at 0237` ("odd" time), `atq`, `atrm`; with low load: `batch`. Periodic: `crontab -e` (5 fields, 0/7 = Sunday); output goes by e-mail; no need to restart cron [from source] (TLDP p.99-102). Review with `shell_lint.py --crontab`.

## P6. Find out what a command does
`man command` (sections with `man 5 x`), `info command`, `command --help`, `apropos term`, `whatis cmd`; builtins: the shell's man; documents in `/usr/share/doc` [from source] (TLDP p.31-36).

## P7. Find files
Known name: `find <path> -name 'pattern'` (or `locate`, faster but with a daily index); content: `grep -r pattern dir`; command: `which`; size: `find . -size +5000k`; test the selection **before** `-exec rm`; prefer `| xargs rm` [from source] (TLDP p.62-64, 110).

## P8. Simple, restorable backup
1. `tar cvf /var/tmp/home.tar dir/` (archive the **directory**); 2. `gzip`/`bzip2`; 3. incremental: `tar -g snapshot` (better than `-N`); 4. copy to another host (`scp`) or USB/`rsync -avz`; 5. if sensitive, `gpg -e -r recipient file`; 6. **test the restore** `[extrapolation]` (the book does not address it) [from source p.152-163].

## P9. Avoid overwriting a file by mistake
`set -o noclobber` in `.bashrc`; use `>>` to append; to filter the file itself: `tail -5 f > new && mv new f` [from source] (TLDP p.106, 120). `rm -i`/`cp -i`/`mv -i` (p.61).

## P10. Basic network diagnosis
`ip addr show` (UP/RUNNING) → `ip route show`/`netstat -nr` (default route) → `ping` the gateway and an external IP → `host name` (DNS; check `/etc/resolv.conf` and `nsswitch.conf`) → `traceroute` → `netstat -l | grep tcp` for what is listening [from source] (TLDP p.169-174, 191). `[extrapolation]`: today use `ip`, `ss`.

## P11. Secure remote access
`ssh user@host` (accept the fingerprint by typing `yes`), `scp`/`sftp`, `ssh-keygen` with a passphrase; remote X via ssh; do not use telnet/rsh/non-anonymous FTP; if ssh warns that the host key changed, **investigate** before continuing [from source] (TLDP p.184-189).

## P12. Suspected break-in
Checklist (mysterious ports, wiped logs, strange binaries...) → disconnect from the network → investigate → save data → reinstall → new passwords → restore → update → re-examine → reconnect [from source] (TLDP p.194-195).

## P13. Review a script (with the package's checker)
1. `python -I scripts/shell_lint.py script.sh`; 2. read each finding with its **origin** ([from source]/[inference]/[extrapolation]) and pass it on to the user; 3. the absence of findings does not prove correctness (the checker covers few rules); 4. suggest `shellcheck` as a complement `[extrapolation]` (the book does not mention it); 5. check `#!`, permissions (`chmod u+x`) and which destructive commands use variables.

## P14. Install/update software (legacy) [DATED]
Read the README → update the system → `rpm -Uvh` (kernel: `-i`) or `apt-get update && apt-get upgrade`/`install` → keep the old kernel in grub.conf [from source] (TLDP p.136-141).
