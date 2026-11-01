# Software installation, packages and updates [DATED] (Ch. 7, 7.5)

Pages = PDF (printed + 8). Abbreviation TLDP.

> **[DATED]** The book (2008) covers RPM, dpkg/APT, up2date, yum (as a novelty), YaST and urpmi. It does not cover dnf, zypper, pacman, snap/flatpak, modern signatures or containers. The *principles* (update right away and always, read the README, keep the old kernel available) remain useful; the exact commands, not necessarily.

## Book principles
- Most distributions already ship common drivers and applications; software comes in packages (installation CDs or the Internet); **always read the README** and the package instructions [from source] (TLDP p.136).
- The first thing after installing is to **apply updates**; then, regularly (daily if possible, every few weeks as a reasonable start); use the distribution's site and mirrors; this includes security fixes [from source] (TLDP p.139). The networking chapter repeats it: updating is "almost a daily habit" (TLDP p.192).

## RPM
- `rpm -Uvh package.rpm` (upgrade, verbose, progress bar) installs or updates; **new kernels** use `-i` (install without overwriting) to allow going back to the old one; `rpm -qa | grep vim` lists; `rpm -qf /bin/cat` says which package a file comes from; `rpm -e package` removes; querying does not require root, changing does [from source] (TLDP p.137).
- An RPM package has files plus metadata (helper scripts, attributes); there are binary and source packages; there is authenticity verification (TLDP p.136).

## DEB / APT
- `dpkg -l pattern` shows versions (`ii` installed, `un` unknown/not installed); `dpkg -S /bin/cat` says which package owns the file; dselect/aptitude manage [from source] (TLDP p.138).
- `apt-get update` downloads the index, `apt-get upgrade` updates the system, `apt-get install package` installs resolving dependencies; example with `su - -c "apt-get install xsnow"` (the `-c` runs only that command as root and returns, "so you don't forget to leave the root account") [from source] (TLDP p.139-140).

## Other managers mentioned [DATED]
`up2date` (RedHat/Fedora), `yum` (Fedora), YaST/YOU (SuSE), URPMI (Mandriva) [from source] (TLDP p.140).

## Source code
Tarball (`program-version.tar.gz`) or `.src.rpm`; Debian has `apt-get source`; needs `gcc` and the README with dependencies [from source] (TLDP p.138).

## Kernel
Only compile/install a kernel manually if you need a feature absent from the default one; install it **alongside** the old one and create a double entry in `grub.conf` (default=0, timeout, two `title`); once proven, remove the old one, but wait a few days [from source] (TLDP p.140-141). `grub.conf` does not require rerunning grub (p.141).

## Mounting and ejecting a CD (useful for installing packages)
`mount /dev/cdrom /mnt/cdrom`; entry in `/etc/fstab` with `noauto,owner,ro`; `mount` without arguments checks; to eject, leave the mount point (`cd`) and use `umount /mnt/cdrom` or `eject cdrom`; "device busy": check shells and applications using the CD and use `lsof`; never force the tray [from source] (TLDP p.141-142).

## For current systems
Answer as `[extrapolation]`: current apt/dnf/zypper, signed repositories, `dpkg -L`, `rpm -V`, snap/flatpak, automatic updates and livepatch. Supply-chain security and containers are not from the book.
