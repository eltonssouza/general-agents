# Cases, antipatterns and attributions that are NOT from the book

Pages = PDF (printed + 8). Abbreviation TLDP.

## A. Cases worked through by the book (and what each illustrates)
| Case | Lesson | Page |
|---|---|---|
| `sendsms` "command not found" for one user and not for another | each user has a different PATH; `which` + `su - user` to compare | TLDP p.48 |
| Homemade `wc` in ~/bin hangs the terminal | the first hit in PATH wins; full path or reorder | TLDP p.48-49 |
| `acroread` outside the PATH (tina) | `which` fails; `export PATH=$PATH:/opt/acroread/bin`; `locate` finds the program | TLDP p.62-63 |
| `./hello` "bad interpreter: Permission denied" | missing execute bit; `chmod u+x` | TLDP p.70 |
| `tar` of files vs of a directory | extracting "without a directory" scatters files | TLDP p.153 |
| tar's `-N` ignores an old file downloaded later | that is why `-g` (snapshot) is better | TLDP p.154 |
| `mv * *.old` does not rename in bulk | the shell expands both `*` before mv; use a loop | TLDP p.130 |
| `ls 2 > tmp` gives "No such file" | a space after the 2 makes it an argument | TLDP p.108 |
| `ls > f 2>&1` vs `ls 2>&1 > f` | order of the redirections | TLDP p.108 |
| `tail testfile > testfile` (exercise) | the `>` truncates before the command reads | TLDP p.106, 143 |
| passwd with SUID, write/wall with SGID | special modes solve access to protected resources | TLDP p.86-87 |
| /var/tmp with sticky bit | everyone's directory, without deleting others' files | TLDP p.74 |
| Hung browser: `kill -15`, then `kill -9` | signal escalation; confirm with ps | TLDP p.98 |
| `(sleep 1800; echo "Lunch time..") &` | sleep as a simple reminder | TLDP p.99 |
| Bad `at 0100` time | system jobs run at round hours | TLDP p.100 |
| SSH host key changed warning | protection against Trojan horse/man-in-the-middle | TLDP p.188 |
| Lost key passphrase | no recovery; generate a new one | TLDP p.163, 189 |
| "Was I broken into?" | checklist and recovery order | TLDP p.194-195 |
| New kernel with `rpm -i` + double grub.conf | keep the old one to go back | TLDP p.137, 140-141 |
| CD "device busy" on eject | someone is using the FS; `cd`, close apps, `lsof` | TLDP p.142 |

## B. Antipatterns (with the origin of the warning)
1. Working as root day to day [from source] (TLDP p.26, 28, 30).
2. Removing without a backup, expecting a trash can [from source] (TLDP p.61); `rm -r` with an unchecked variable `[extrapolation]`.
3. Reading and writing the same file on the same line with `>` [from source] (TLDP p.106; exercise p.143).
4. Using `kill -9` as the first choice [from source] (TLDP p.98).
5. `nice`/`renice` on interactive programs [from source] (TLDP p.95).
6. Giving `777` to "fix" permissions: the book lists 777 as "everyone does everything" (TLDP p.71); the risk is `[extrapolation]`.
7. SUID/SGID spread around [from source] (TLDP p.86).
8. telnet/rsh/rlogin/non-anonymous FTP on untrusted networks [from source] (TLDP p.180, 184, 192).
9. Updating "someday" instead of right away and regularly [from source] (TLDP p.139, 192).
10. Removing `127.0.0.1 localhost` from /etc/hosts or tampering with the `lo` interface [from source] (TLDP p.169-170).
11. Archiving loose files (without a directory) in a backup [from source] (TLDP p.153).
12. Editing configuration files with an office editor [from source] (TLDP p.117).
13. Editing `/etc/passwd`/`group` by hand without need (use useradd/usermod/groupadd) [from source] (TLDP p.52-53); never edit `mtab` (p.53).
14. Scheduling `at`/cron jobs all at round hours `[inference]` from TLDP p.100.
15. Keeping a password in a proxy variable in `.bashrc` (the book shows the example, TLDP p.179) `[extrapolation]`: bad practice.
16. Moving files into an SGID directory expecting them to inherit the group (they do not: they keep their original owner and group) [from source] (TLDP p.74).
17. Changing the X/grub files without a backup [from source] (TLDP p.134, 140).

## C. Common attributions that the book does NOT support (correct them with the real page)
| Circulating claim | Situation in the book |
|---|---|
| "The book teaches systemd/systemctl" | It does not appear; init is SysV (TLDP p.89-92) |
| "The book explains `set -e`, `trap`, `getopts`, `[[ ]]`" | No; only ~3 pages of scripting (TLDP p.129-131) |
| "The book says to always quote variables" | No; the example uses `for i in $LIST` without quotes (TLDP p.130) |
| "The book recommends `chmod 755` for scripts" | Table 3-9 lists 755 for directories and 700/u+x appear in examples (TLDP p.70-71) |
| "The book forbids 777" | It only describes what 777 does (TLDP p.71) |
| "The book explains umask bit by bit" | It explains by subtraction (TLDP p.72) |
| "The book covers ACLs/SELinux" | They do not appear |
| "The book teaches `ss`" | Only netstat/ifconfig/ip (TLDP p.170-172) |
| "The book explains nohup" | It mentions `screen` (TLDP p.80) |
| "The book says `grep` returns 1" | It says -1 (TLDP p.85), which is imprecise |
| "The book covers cron `*/5`, `@reboot`" | No; only lists and ranges (TLDP p.101) |
| "The book recommends `sudo` as a rule" | It recommends su and, **better**, sudo in the security tips (TLDP p.194); sudo configuration is not covered |
| "The book covers modern firewalls (ufw/nftables)" | Only Netfilter/iptables and TCP wrappers in broad strokes (TLDP p.192-193) |
| "The book explains containers/Docker" | It does not appear |
| "The book teaches scheduling/virtual memory in depth" | Only practical use (nice, swap, top); internals belong to the OSTEP agent |
