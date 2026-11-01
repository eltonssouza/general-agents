# Backup, compression and encryption (Ch. 9)

Pages = PDF (printed + 8). Abbreviation TLDP.

## The book's idea
Accidents happen (user error, power failure, disk failure); keep an extra copy of important or sensitive data [from source] (TLDP p.152). Prepare (archive/compress) → move to media or another host → optionally encrypt.

## tar
- Main options: `-c` creates, `-x` extracts, `-t` lists, `-v` verbose, `-f file` (default: the first tape device), `-j` filters through bzip2; the hyphen is usually omitted (`tar cvf`) [from source] (TLDP p.152).
- **Use GNU tar** on all systems: proprietary tars may be incompatible; on Linux it is always GNU; `tar --help` reveals it [from source] (TLDP p.152-153).
- **Archive directories, not loose files**: extracting "files without a directory" scatters them wherever you are, possibly on another machine (the `images/` vs `*.jpg` example) [from source] (TLDP p.153).
- **Incremental**: `-N date/file` includes files modified after the date (the timestamp of an earlier file); limitation: downloading an old file into the directory makes `-N` ignore it; **better** `-g snapshot-file`, which keeps the file list; use different snapshots for daily and weekly backups in cron and swap the snapshot on full backups [from source] (TLDP p.154-155). The book itself says tar suits simple directories and that there are better tools for whole partitions (rsync) (TLDP p.155, 160).
- Redirecting tar's stderr to /dev/null avoids messages about unchanged files with `-N` (p.154).
- By default tar stores the **symbolic link**, not the target (`-h` changes this); `jar` follows links [from source] (TLDP p.156).

## Compression
`gzip file` (creates `.gz` and **removes the original**; `-d` decompresses), `bzip2` (better algorithm, smaller files); `tar zxvf arch.tar.gz` / `tar jxvf arch.tar.bz2`; after extracting a software tarball, read the README [from source] (TLDP p.155). `jar` compresses by default and can sign entries (p.156).

## Media and other hosts [DATED]
- Floppy: `fdformat`, `mformat`/`mcopy` (mtools), `mount /mnt/floppy`; `dd if=... of=/dev/fd0` writes raw (not mountable; serves boot disks) [from source] (TLDP p.156-157).
- CD: `mkisofs -J -r -o cd.iso .` + `cdrecord`; check space with `df`/`du` [from source] (TLDP p.158).
- USB/camera: mount, copy, `umount`; names /dev/sda, /dev/sdb change according to connection order; `dmesg` shows where the device ended up; HAL in kernel 2.6 [from source] (TLDP p.159) [DATED].
- Tape: `tar` + `mt`; database backups may require their own procedure; Amanda for several hosts [from source] (TLDP p.159).
- Copying to another host with scp/ftp (Ch. 10) (TLDP p.156). BSD `dump`/`restore` copy ext2/ext3 systems bit by bit (p.160).

## rsync
Fast and flexible, common on UNIX, easy in scripts; "remote" can be a local partition or a USB drive: `rsync -avz /home/karl/ /mnt/usbstore` (after `mount -t vfat /dev/sda1 /mnt/usbstore`, as root, and checking the device with `dmesg`) [from source] (TLDP p.160).

## GnuPG (encryption)
- Why: data in a place you do not control (the provider's server); e-mail normally travels in clear [from source] (TLDP p.160).
- Generate a pair: **private** key (never share it; protected by a passphrase) and **public** key (for correspondents); generation uses system entropy (move the mouse) [from source] (TLDP p.161-162). `gpg --list-keys` shows them; `gpg --export -a` exports the public one (p.162).
- Encrypt: `gpg -e -r (part of the uid) file`; only the `-r` recipient will be able to decrypt; decrypt: `gpg -d -o output file.gpg` [from source] (TLDP p.162-163).
- **"No password = no data"**: if you forget the passphrase, the data is lost, not even the administrator can recover it; keep a copy of important keys (e.g. bank vault) [from source] (TLDP p.163).
- [DATED] the example uses GnuPG 1.4 and DSA/ElGamal keys of 1024/4096 bits; do not use it as a current algorithm recommendation.

## Not covered (extrapolation)
restic/borg/duplicity, snapshots (LVM/ZFS/btrfs), 3-2-1 policy, retention, RPO/RTO, **restore testing**, integrity verification, disk encryption (LUKS), cloud backups. If asked, answer `[extrapolation]` (and, for operational reliability, refer to the SRE/operations agent).
