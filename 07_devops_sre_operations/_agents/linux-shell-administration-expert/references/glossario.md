# Glossary (terms from the book, explained in our own words)

Pages = PDF (printed + 8). Abbreviation TLDP. English terms kept as in the book.

| Term | Explanation | Page |
|---|---|---|
| CLUE | "Command Line User Experience": the experience of using Linux/UNIX from the command line, the book's goal | TLDP p.9 |
| shell | interpreter that talks to the system; the book compares it to a language in which the user also leads | TLDP p.50 |
| bash | "Bourne Again SHell", the default GNU shell and a superset of sh | TLDP p.50 |
| prompt | text that precedes typing (user, machine, directory); it is not part of the command | TLDP p.27 |
| built-in (command built into the shell) | command that is part of the shell (cd, exit, logout, pwd), with no man page of its own | TLDP p.36 |
| man page / Info page | documentation in numbered sections / GNU project documentation in nodes | TLDP p.31-34 |
| root (account) | the administrator account; use only when necessary | TLDP p.26, 28 |
| / (root) vs /root | root directory of the tree vs the administrator's home | TLDP p.46 |
| partition | division of the disk; isolates damage and organizes data | TLDP p.42 |
| swap | partition used as an extension of physical memory | TLDP p.42-43 |
| mount point | directory where a partition is attached to the tree | TLDP p.44 |
| inode | structure with the attributes and the data location of a file (it does not store the name) | TLDP p.47 |
| hard link / symlink | another name for the same inode / small file that points to a path | TLDP p.66-68 |
| PATH | list of directories where the shell looks for executables | TLDP p.48 |
| absolute / relative path | starts with `/` / does not start with `/` | TLDP p.49 |
| glob (wildcard) | `*`, `?` and `[ ]` expanded by the shell | TLDP p.61-62 |
| umask | mask subtracted from 666/777 to set the permissions of new files | TLDP p.72 |
| SUID / SGID | executable runs with the file's owner/group; on a directory, SGID inherits the group | TLDP p.74, 86-87 |
| sticky bit | on a directory, prevents deleting/changing others' files (e.g. /var/tmp) | TLDP p.74 |
| user private group | scheme in which each user has a group of their own with the same name | TLDP p.71 |
| process / PID / PPID | running program / its identifier / the parent's identifier | TLDP p.81 |
| daemon | server that runs continuously in the background | TLDP p.81 |
| nice | number that measures the process's "niceness"; high = less important | TLDP p.81, 95 |
| fork and exec | create a copy of the process and replace it with another program | TLDP p.84 |
| zombie | terminated process whose parent has not reaped it | TLDP p.85 |
| exit status | number returned to the parent when the process ends; 0 = success | TLDP p.85 |
| signal (SIGTERM...) | message sent to a process (15, 2, 9, 1) | TLDP p.86 |
| job control | shell features (&, jobs, bg, fg, Ctrl+Z) to manage processes | TLDP p.80 |
| runlevel | configuration of init processes (0-6) | TLDP p.89, 91 |
| init | first process (PID 1); in SysV it reads /etc/inittab | TLDP p.84, 89 |
| MBR / GRUB | boot sector / boot loader | TLDP p.88 |
| cron / crontab | periodic scheduling service / file of schedules | TLDP p.100-101 |
| at / batch | one-time execution at a set time / when the load allows | TLDP p.81, 100 |
| stdin, stdout, stderr | descriptors 0, 1 and 2 | TLDP p.108 |
| pipe | `\|`: connects one command's stdout to another's stdin | TLDP p.105 |
| noclobber | Bash option that prevents `>` from overwriting existing files | TLDP p.106 |
| filter | program that reads input, transforms it and writes to stdout (grep, sort, uniq) | TLDP p.109 |
| environment variable | variable inherited by child processes (PATH, HOME) | TLDP p.122 |
| source | applies a command file to the current shell | TLDP p.126 |
| PS1 | prompt variable | TLDP p.128 |
| shebang (`#!`) | first line that indicates the script's interpreter | TLDP p.129 |
| display / X server | name of the graphical screen `host:display.screen` / program that controls the screen | TLDP p.132-133 |
| tarball | file produced by tar (usually compressed) | TLDP p.152-153 |
| rsync | efficient copy/synchronization, local or remote | TLDP p.160 |
| GnuPG | PGP-compatible encryption suite | TLDP p.161 |
| loopback (lo) | internal interface 127.0.0.1 | TLDP p.170 |
| (x)inetd | super-server that starts daemons on demand | TLDP p.175 |
| PAM | pluggable authentication modules | TLDP p.182-183 |
| SSH | encrypted remote shell, with scp/sftp | TLDP p.186-189 |
| firewall / packet filter | barrier by rules / filter that looks inside IP packets | TLDP p.192 |
| IDS | intrusion detection system (host: tripwire; network: Snort) | TLDP p.193-194 |

For the book's own glossary (command index), use `python -I scripts/linux_lookup.py cmd <command>` (TLDP p.212-223).
