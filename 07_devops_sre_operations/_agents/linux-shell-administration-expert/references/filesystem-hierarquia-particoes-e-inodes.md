# Filesystem: tree, partitions, swap, mount, inodes (Ch. 3, sections 3.1 and 3.2)

Pages = PDF (printed + 8). Abbreviation TLDP.

## Mental model
- "In UNIX, everything is a file; what is not a file is a process": an acceptable simplification, since named pipes and sockets are special files [from source] (TLDP p.40). A directory is a file that lists other files; devices are also files (p.40).
- File types and the first character of `ls -l`: `-` regular, `d` directory, `l` link, `c` special, `s` socket, `p` named pipe, `b` block (table 3-1) [from source] (TLDP p.41). `ls -F` adds the suffixes `/ = * | @` (p.41).
- As a user, you deal mostly with regular files, executables, directories and links; the special ones are a matter for administrators and programmers [from source] (TLDP p.41).

## Why partition
- Isolate damage: a problem hits only the affected partition; and, today, the main reason is security and robustness (a breach or a runaway process that fills the disk does not bring down the whole system) [from source] (TLDP p.42).
- Journaling only protects against power failure and sudden disconnection; it does **not** protect against bad blocks and logical errors, for that use RAID [from source] (TLDP p.42).
- Types: data partition (includes the root) and swap partition; fdisk marks 82 (swap) and 83 (data); filesystems mentioned: ext2/ext3, Reiser, JFS, NFS, FATxx [from source] (TLDP p.42) [DATED].
- Book rule: swap of about twice the RAM; with two disks, a swap partition on each gives better I/O [from source] (TLDP p.43) [DATED: the rule was already being revised and varies with load].
- Standard separation: /boot (kernel), /usr, /home, /var, /opt; on servers, service data separate from programs [from source] (TLDP p.43-44). Once created, it is advisable only to **add** partitions, not resize them (p.43).

## Mount points, fstab and df
- Every partition enters the tree through a mount point (empty directory in the root); `mount` attaches; at startup, partitions are mounted according to `/etc/fstab` [from source] (TLDP p.44).
- `df -h` shows usage, size and mount point of active partitions (not swap); `df -h .` tells you which partition you are on; directories under `/` belong to the root partition, unless they have their own entry in df [from source] (TLDP p.44-45, 47).

## The tree (table 3-2) and conventions
- Layout varies by distribution; names are convention; the root `/` is the base; `/root` (the administrator's home) is not `/` [from source] (TLDP p.46).
- Figure 3-1 (seen as an image, TLDP p.45) draws the tree: below `/` are bin, boot, dev, etc (with default, rc.d, sound, sysconfig, X11), home (users), lib, lost+found, misc, mnt (cdrom, floppy), net, opt, proc, root, sbin, tmp, usr (X11R6, bin, games, include, lib, local, man, sbin, share/doc, src) and var (gdm, lib, lock, run, log, spool, tmp) [from source] (TLDP p.45).
- Table: /bin, /boot (kernel, grub), /dev, /etc (configuration), /home, /lib, /lost+found, /mnt, /opt, /proc (virtual), /root, /sbin, /tmp (cleared on reboot; do not keep work there), /usr, /var [from source] (TLDP p.46). `man hier` describes the hierarchy (p.47).
- `/var` holds variable data (logs, mail and print queues, locks); it sits on a separate partition for security (a "mail bomb" does not fill the rest of the system) [from source] (TLDP p.55). `/var/tmp` is recommended for temporary files; `/tmp` can be wiped without warning [from source] (TLDP p.55). Logs in `/var/log` (the syslog configuration determines retention) (p.55); `/var/spool` has at, cron, lpd, mail (p.55).
- Configuration files in /etc (table 3-3: aliases, bashrc, crontab, fstab, group, hosts, inittab, issue, motd, mtab, nsswitch.conf, pam.d, passwd, profile, rc*, resolv.conf, services, ssh, sysconfig, xinetd.*): edit `passwd`/`group` with the shadow package tools (useradd, usermod, groupadd...) and do **not** edit `mtab` [from source] (TLDP p.52-53). Devices in /dev (table 3-4) (p.54).

## Inodes
- Each file has an inode with owner, type, permissions, times, link count, size and the address of the data; **the name is not in the inode** (it is in the directory file); each partition has its own set of inodes, and the number is fixed when the FS is created (about 1 inode per 2 to 8 KB); `ls -i` shows the number [from source] (TLDP p.47).
- Consequence `[inference]`: the maximum number of files per partition is limited by the inodes (the book says so: "maximum amount of files"), and hard links do not cross partitions (TLDP p.47, 66-67).

## Outside the book (do not cite as from the book)
Formal FHS, /run, /sys, /srv, /media, ext4/XFS/btrfs, LVM, GPT/UEFI, fsck/mkfs, df -i, tmpfs, snapshots. Internal FS structures, journaling and virtual memory belong to the OS internals agent (OSTEP), `[extrapolation]` here.
