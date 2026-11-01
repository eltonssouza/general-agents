# Permissions, ownership, umask and special modes (Ch. 3, 3.4; Ch. 4, 4.1.6)

Pages = PDF (printed + 8). Abbreviation TLDP. Use `scripts/chmod_calc.py` to calculate (see the end).

## Model
- Every file belongs to a user and a group; there is the "others" category; for each one, read (r), write (w), execute (x); the 9 characters after the type in `ls -l` follow the order user, group, other [from source] (TLDP p.68-69).
- Codes: r=4, w=2, x=1, "-"=0 (table 3-7); categories u, g, o (table 3-8) [from source] (TLDP p.69). `id` shows uid/gid/groups; `$USER` holds the name (p.69).
- Interpretation of the example `-rw-rw-r--`: owner and group read and write, others only read, nobody executes (p.69).

## chmod
- Symbolic: `chmod u+x hello`; `+`/`-` grant/deny; combinations by comma: `chmod u+rwx,go-rwx hello` [from source] (TLDP p.70). `chmod o= file` clears the rights of "others" (p.73).
- The error `bad interpreter: Permission denied` when running `./hello` with `#!/bin/bash` is solved with `chmod u+x hello` [from source] (TLDP p.70). "It worked yesterday" and "it works as root" point, in most cases, to wrong permissions [from source] (TLDP p.70).
- Numeric: sum per category, 3 digits; **table 3-9**: 400 (protect against overwriting), 500 on a directory (avoid accidental removal/renaming), 600 (private), 644 (publicly readable), 660 (group can change), 700 (owner only), 755 on a directory (readable/executable by others), 775 (standard group sharing), 777 (everyone does everything) [from source] (TLDP p.70-71).
- Fewer than 3 digits: leading zeros; there is a **fourth digit** on the left for special modes (p.71).
- Note `[extrapolation]`: the book describes 777 but does **not** explicitly discourage it; write permission for "others" is a classic risk, and `chmod -R` does not appear in the book.

## Groups
- `id` lists the possible groups; most systems allow being active in **one** group at a time; the primary group comes from the 4th field of `/etc/passwd` and is resolved in `/etc/group` [from source] (TLDP p.71).
- **User private group** scheme: each user has a group of their own, with the same name; secondary groups require `newgrp` (and `gpasswd` for a group password) [from source] (TLDP p.71). Joining the group with newgrp makes new files be created with that group and avoids chown (p.71-72); the mask does not change when switching group (p.72).

## umask
- New files start from 666 and directories from 777; the umask value is **subtracted** (the book's model): with 0002, file 664 and directory 775; root usually has 022 [from source] (TLDP p.72-73). The first zero of the 4-digit umask belongs to the special attributes (p.72).
- A directory always gets x by default; without x it becomes inaccessible (the book suggests trying chmod 644 on a directory) (p.72).
- The default umask is set in /etc/bashrc or /etc/profile and can be changed in the user's file (p.73, 127).
- `[extrapolation]` The real operation is bitwise (base AND NOT umask). Subtraction and bitwise coincide for the common masks (022, 002, 027) but diverge in cases such as 033; `chmod_calc.py umask 033` shows both.

## chown and chgrp
- `chown new-owner file`; `chown user: file` also changes the group to the user's primary group; `chgrp group file`; `-R` recursive; ordinary users are usually prevented from changing ownership, to keep them from assigning files to third parties [from source] (TLDP p.73-74).

## Special modes
- **Sticky bit**: on a directory, the user can only change/delete files they own (or that the permissions allow); shown as `t` (`drwxrwxrwt /var/tmp`); `chmod o+t dir`; the historical use on executable files (keep in memory) is obsolete [from source] (TLDP p.74) [DATED].
- **SUID/SGID** (letter `s`): the executable runs with the user/group **of the file**; central example: `passwd` (`-r-s--x--x`, owner root) changes `/etc/passwd`; `write` and `wall` use the tty group's SGID to write to other people's terminals [from source] (TLDP p.74, 86-87).
- **SGID on a directory**: new files inherit the directory's group; files moved in from elsewhere keep their original owner and group; it is "the standard way to share files in UNIX" according to the book [from source] (TLDP p.74).
- Use: as little as possible; special modes carry security risks; Linux's ps uses /proc to avoid SUID [from source] (TLDP p.86).
- Group names (tty etc.) vary by distribution (p.87).

## Not covered
ACLs (setfacl), SELinux/AppArmor, capabilities, chattr/lsattr, `chmod X`, SUID auditing with find, nosuid in mount. Treat as `[extrapolation]`.

## Support script
`python -I scripts/chmod_calc.py octal 755 | from-ls -rwxr-xr-x | symbolic "u+rwx,go-rwx" --from 664 | umask 0027 [--dir] | common | check 777`. In Git Bash use `MSYS_NO_PATHCONV=1` if passing paths that start with `/`.
