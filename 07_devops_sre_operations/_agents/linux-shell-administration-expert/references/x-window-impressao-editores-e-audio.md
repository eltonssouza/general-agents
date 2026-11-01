# X Window, editors, printing and audio/video (Ch. 6, 7.3, 8, 11)

Pages = PDF (printed + 8). Abbreviation TLDP. Peripheral chapters for server administration; **all the graphical, printing and multimedia content is [DATED]**.

## Editors (Ch. 6)
- Mastering at least one terminal text editor is "the first step to independence"; it works on remote machines without transferring the graphical environment [from source] (TLDP p.113).
- **Emacs**: extensible, customizable, self-documenting (Ctrl+H) (TLDP p.113-114). **vi/vim**: present on practically every UNIX ("if you know how to use vi, you survive on any UNIX"); help with `:help` (TLDP p.114).
- vi has **two modes**: command (initial) and insert; **Esc** returns to command mode [from source] (TLDP p.114-116).
- Commands: `h j k l` (move), `G` (end), `n dd` (delete lines), `n dw`, `x`, `:n` (go to line), `:w`, `:q`, `:q!` (quit discarding), `:wq`, `:w new`, `/text` and `/` (repeat), `:1,$s/word/other/g`, `yy`, `p`, `:recover`; `a`, `i`, `o` enter insert mode [from source] (TLDP p.115). `vimtutor` (30 min) is the "easy" path (p.116).
- **Do not edit configuration files with office suite components**: they insert formatting/fonts and break the program that reads the file; for the graphical case, gedit/kedit/kwrite/xedit or gvim [from source] (TLDP p.117).
- Office section (StarOffice/OpenOffice/KOffice) [DATED] (TLDP p.116-117); use GPG, not a signature image in .doc, to sign messages (p.117).

## X Window (7.3 and 10.4.3)
- X is a **network-transparent** window system: the X server controls screen/keyboard/mouse; clients (terminal, browser, editor) can run on the same machine or on another [from source] (TLDP p.132, 185-186).
- Display name `hostname:displaynumber.screennumber` (display starts at 0; default screen 0); the `DISPLAY` variable holds the default and xterm sets it by itself; on a remote login you may need to set it [from source] (TLDP p.132-133).
- Window manager (twm, Sawfish, Enlightenment) controls the layout of the windows; desktop manager (Gnome, KDE) uses a window manager and adds menus, panels and a file manager [from source] (TLDP p.133).
- Server configuration: `XF86Config` (XFree86) or `xorg.conf` (X.Org), normally in `/etc/X11`, in sections; **back up before changing** because an error produces an unreadable screen [from source] (TLDP p.133-134) [DATED: XFree86/XF86Config].
- Remote display: `xhost +machine` + `export DISPLAY="local:0.0"` on the remote one, or, better, SSH with X11 forwarding (see `redes-servicos-e-acesso-remoto.md`) [from source] (TLDP p.186-187).

## Printing (Ch. 8)
- `lp file` or `lpr file` (accept a pipe: `command | lp`); each job gets an id (`blob-253`); `lpq`/`lpstat` show the queue, `lpstat -d` the default printer, `lpstat -p` the state; `lprm`/`cancel` remove jobs; `lpc` controls several printers [from source] (TLDP p.145-146). There are two sets of commands because of BSD vs System V history; CUPS accepts both (p.146).
- Formatting: Linux prints text, PDF, PostScript and images directly; converters `pdf2ps`, `a2ps`...; `man -t cmd > file.ps` to print man pages; viewing with gv, xdvi, xpdf (TLDP p.146-147) [DATED].
- Server: LPD → LPRng → **CUPS** (IPP), with a web interface on **port 631** (`localhost:631`) [from source] (TLDP p.147-148).
- Diagnosing "it didn't come out": `lpq`, see whether the job appears and whether the printer is printing; check paper and connections; print from another host; test sending the formatted file by FTP to the network printer; remove a wrong job with `lprm` (only works before the job reaches the printer) [from source] (TLDP p.148-150).

## Audio, video and VoIP (Ch. 11) [DATED]
OSS vs ALSA architecture (`alsaconf`, `alsamixer`), an audio CD is not "mounted" (a data CD with mp3s is), `mplayer`, `arecord`/`play` to test the microphone, non-free codecs; **VoIP**: does not replace telephony (emergencies), generally unencrypted (eavesdropping risk), and requires opening the firewall; NAT can get in the way [from source] (TLDP p.197-202). None of this is needed for server administration; answer briefly and label it [DATED].
