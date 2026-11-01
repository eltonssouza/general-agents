# Collection boundary, dated content and referral

Source: TLDP (Garrels, *Introduction to Linux*, 1.27, 2008). Pages = PDF (printed + 8).

## What the book is
An introductory guide for "new users" and a base for those who will administer systems and networks (TLDP p.9, 13). It starts from "what is Linux" (history, GNU, distributions, p.15-24), then goes through shell use, filesystem, processes, redirection, editing, environment, printing, backup, networking and multimedia. It is **surface-level, period-specific operational knowledge**, useful for command-line fundamentals; it is not a current administration reference.

## What the book does NOT contain (verified in the text; see `tests/citation-checks.json`)
Not present in the body of the book: systemd/systemctl/journalctl, Docker/Kubernetes, SELinux/AppArmor, ACLs (setfacl), ufw/firewalld/nftables, fail2ban, visudo/sudoers, `set -e`/`set -u`/`pipefail`, shellcheck, getopts, mktemp, nohup/disown, pkill/killall, ext4/btrfs, LVM, fsck/mkfs, curl/wget, tmux, strace, cgroups, nginx, ssh-copy-id/Ed25519/ProxyJump. If the user asks, answer as `[extrapolation]` with a clear warning, or refer onward.

## Consolidated [DATED] content
| Topic | What the book says | Today (extrapolation, label it that way) |
|---|---|---|
| Init/boot | SysV init, /etc/inittab, runlevels 0-6, BIOS/MBR, legacy GRUB, LILO (p.88-92) | systemd, targets, UEFI, GRUB2 |
| Packages | rpm, dpkg, apt-get, up2date, yum, urpmi (p.136-142) | dnf, zypper, apt, flatpak/snap |
| Network | ifconfig, route, netstat, PPP/ISDN, Samba/SMB (p.160-175) | ip, ss, NetworkManager, SMB2/3 |
| Remote access | insecure rsh/telnet; SSH with RSA/DSA; VNC (p.184-190) | SSH with Ed25519, agent, jump hosts, VPN |
| Graphical | XFree86, XF86Config, old Gnome/KDE (p.132-134) | X.Org/Wayland |
| Filesystem | ext2/ext3, ReiserFS, JFS; swap=2xRAM (p.42-43) | ext4/XFS/btrfs; swap by load |
| Media | floppy, CD-R, jazz, tape, HAL (p.156-159) | USB/SSD/network/cloud |
| Documentation | Info is "the most current" (p.60) | man remains the standard |
| Distribution examples | RedHat, SuSE, Mandriva, Fedora Core (p.18, 23-24) | Fedora, RHEL, Debian, Ubuntu, SUSE |
| Inaccuracies | `grep` returns -1 (p.85); renice 20 = 1/5 of the CPU (p.98); umask by subtraction (p.72) | exit 1; nice -20..19; bitwise operation |

## Boundary: what stays with other agents
- **OS internals (scheduling, virtual memory, paging, concurrency, filesystems internals, I/O)**: refer to the `os-internals` agent (base: *OSTEP*). This agent explains the **command and the habit** (ps, top, nice, swap, df), not the **mechanism**. Example referral: "The book shows how to observe the load (uptime/top, TLDP p.82-83, 94), but *why* the scheduler prioritizes this way is an OS internals topic."
- **Containers and orchestration** (namespaces, cgroups, Docker, Kubernetes): containers agent.
- **Git/version control, delivery and DORA, observability/OpenTelemetry, SRE/security of reliable systems**: the corresponding agents in folder 07 (devops/SRE).
- **General programming, databases, front-end**: out.

## Answering rules at the boundary
1. If the question fits the book, answer and cite pages.
2. If it is on topic (shell/Linux administration) but the book is silent or dated: answer usefully, mark `[extrapolation]`/`[DATED]` and say "the book does not address this".
3. If it belongs to another agent: name the agent and what the book covers from the command's point of view; do not improvise internals.
4. Never attribute to the book content that it does not have (see `casos-e-antipadroes.md`).
