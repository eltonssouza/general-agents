# Boot, GRUB, SysV init, runlevels and shutdown [DATED] (Ch. 4, 4.2)

Pages = PDF (printed + 8). Abbreviation TLDP.

> **This entire file is [DATED].** The book (2008) describes BIOS/MBR, legacy GRUB, LILO and SysV init with /etc/inittab. Current systems generally use UEFI, GRUB2 and **systemd** (units, targets, journalctl), which the book does **not** cover. Use this content to understand legacy systems and the *idea* of run levels; for current systems, warn that it is `[extrapolation]`.

## Boot sequence according to the book
1. The x86 runs the BIOS, which tests the hardware and chooses the boot device; it reads the **MBR** of the first disk and hands over control [from source] (TLDP p.88).
2. The MBR loads the boot loader (GRUB or LILO), which shows a menu and hands control to the operating system (p.88).
3. The book details only GRUB (easier and more flexible than LILO); "direct loading" (Linux) vs "chain loading" (DOS/Windows, which overwrite the MBR); GRUB reads its configuration at every boot, without rewriting the MBR; supports LBA (1024-cylinder limit) [from source] (TLDP p.88-89). `info grub` (p.89).
4. The loaded kernel finds and runs **init** (in /sbin), which becomes the parent/grandparent of all automatic processes [from source] (TLDP p.89).

## SysV init
- init reads **/etc/inittab**: it runs an initial script (path, swap, filesystem checks, clock...), sets the **default runlevel** (`id:5:initdefault:`) and the rules per runlevel [from source] (TLDP p.89, 91).
- Runlevels in the example inittab: 0 halt, 1 single user, 2 multiuser without NFS, 3 full multiuser, 4 unused, 5 X11, 6 reboot; do **not** set initdefault to 0 or 6 [from source] (TLDP p.91). `who -r` shows the current runlevel (p.89). Runlevel 1/S: administrator only, for maintenance (p.89).
- init runs the scripts in the runlevel directory: first the **K** (kill) ones with `stop`, then the **S** (start) ones; you can run them by hand (`/etc/init.d/httpd stop` or `service httpd stop`) [from source] (TLDP p.89-90).
- The files in `/etc/rc<x>.d` are **symbolic links** to the real scripts in `/etc/init.d`; the start/stop order comes from the numbers in the name (S10network before S55sshd); same number = alphabetical order [from source] (TLDP p.90).
- After the runlevel, inittab spawns a **getty** per virtual console (6 by default) and defines the handling of Ctrl+Alt+Del (`/sbin/shutdown -t3 -r now`) and of power loss with a UPS; on RPM systems the graphical login is at runlevel 5 (prefdm script; gdm/kdm/xdm); on Debian, `/etc/X11/default-display-manager` [from source] (TLDP p.90).
- `/etc/default` and `/etc/sysconfig` hold defaults read at boot; variations: BSD-style init without rcN.d directories; `/etc/rc.d/init.d` instead of `/etc/init.d`; Gentoo uses another directory [from source] (TLDP p.90-92).
- If the system does not come up because of a bad /etc/inittab, a corrupted /etc/passwd or a forgotten password, **start in single-user mode** [from source] (TLDP p.91).
- If there is no graphical screen, console 7 onward is usually graphical; `who -r` helps; change runlevel with `telinit`; switching between text and graphical console does not change the runlevel [from source] (TLDP p.91-92).
- Tools to manage the links: `chkconfig`, `update-rc.d`, `ntsysv` (text), `yast`/`insserv` (SuSE), DrakConf (Mandriva); all require root [from source] (TLDP p.92).

## Shutdown
- `shutdown` stops in an orderly way: `-h` to halt, `-r` to reboot; `reboot` and `halt` call shutdown in runlevels 1-5, but relying on that is a "bad habit" because it varies between systems; only power the machine off after the halt message, to give time to unmount the partitions [from source] (TLDP p.92).

## How to use this content
- Question about "how runlevels and K/S scripts work": explain from the book and label it [DATED].
- Question about "restarting a service on a current machine": the book does not cover systemctl; answer as `[extrapolation]` and, if appropriate, refer onward.
- Boot internals (initramfs, UEFI, kernel) are outside the book and the scope of this agent.
