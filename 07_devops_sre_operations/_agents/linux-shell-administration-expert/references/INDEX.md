# Reference index: linux-shell-administration-expert

Single source: **TLDP** = Machtelt Garrels, *Introduction to Linux: A Hands on Guide*, edition 1.27 (2008-06-06), The Linux Documentation Project, 223 pages in the PDF. It is an introductory guide, **not** a modern administration manual: the book is from 2008 and describes the distributions, init and tools of that time.

## Page convention (mandatory)
- All citations use the **PDF page number** (`TLDP p.N`).
- Map to the printed number in the footer: **PDF = printed + 8** in the body of the book (Introduction printed 1 = PDF 9; Ch. 1 printed 7 = PDF 15; Glossary printed 204 = PDF 212). PDF 1-8: cover and table of contents.
- The table of contents and the book's internal cross-references ("see Section 3.2.1") use **printed** section/page numbering; add 8 when looking in the PDF.

## Epistemic labels
`[from source]` seen on the cited page · `[inference]` direct deduction from what the book shows · `[extrapolation]` external knowledge (general good practice; the book does not say it) · `[DATED]` changed since 2008 (SysV init, legacy GRUB, old RPM/yum, ifconfig, XFree86, floppy etc.).

## Chapter map (PDF pages)
| Chapter | PDF | Content | Main file |
|---|---|---|---|
| Introduction, Ch. 1 | 9-25 | what Linux is, distributions, installation checklist | fronteira-conteudo-datado-e-encaminhamento.md |
| Ch. 2 Quickstart | 26-39 | login, root, basic commands, Bash shortcuts, man/info | ajuda-e-documentacao-do-sistema.md |
| Ch. 3 Files and filesystem | 40-78 | partitions, tree, inodes, PATH, shells, ls/cp/mv/rm, find/grep, links, permissions | filesystem-..., arquivos-links-..., permissoes-... |
| Ch. 4 Processes | 79-104 | process types, ps/top, signals, SUID, boot/init, performance, at/cron | processos-..., boot-init-..., agendamento-... |
| Ch. 5 Redirection | 105-112 | stdin/stdout/stderr, pipes, filters | redirecionamento-pipes-e-filtros.md |
| Ch. 6 Editors | 113-118 | vi/vim, Emacs, office | x-window-impressao-editores-e-audio.md |
| Ch. 7 Home | 119-144 | housekeeping, variables, setup files, prompt, scripts, X, regional settings, packages | ambiente-do-shell-..., instalacao-de-software-... |
| Ch. 8 Printing | 145-151 | lp/lpr, CUPS | x-window-impressao-editores-e-audio.md |
| Ch. 9 Backup | 152-164 | tar, gzip, rsync, gpg | backup-compressao-e-criptografia.md |
| Ch. 10 Networking | 165-196 | protocols, ip/ifconfig/netstat, services, SSH, security | redes-servicos-..., seguranca-e-resposta-... |
| Ch. 11 Audio/video | 197-203 | ALSA, mplayer, VoIP | x-window-impressao-editores-e-audio.md |
| App. A, B, C | 204-211 | readings, DOS vs Linux, shell features | ambiente-do-shell-... (App. B/C) |
| Glossary | 212-223 | command index with cross-references | `scripts/linux_lookup.py cmd <name>` |

## When to open each file
| Trigger in the question | File |
|---|---|
| man, info, apropos, --help, "how to read the documentation", Bash shortcuts, root vs user | `ajuda-e-documentacao-do-sistema.md` |
| partitions, swap, mount, fstab, df, directory tree (/etc, /var...), inode | `filesystem-hierarquia-particoes-e-inodes.md` |
| ls, cp, mv, rm, find, locate, grep, PATH, which, symbolic/hard links | `arquivos-links-e-busca-de-arquivos.md` |
| chmod, umask, chown, groups, SUID/SGID/sticky | `permissoes-propriedade-e-modos-especiais.md` (+ `scripts/chmod_calc.py`) |
| ps, top, kill, signals, jobs, nice, load, "the system is slow" | `processos-jobs-sinais-e-desempenho-basico.md` |
| boot, GRUB, init, runlevels, shutdown | `boot-init-runlevels-e-shutdown-datado.md` [DATED] |
| at, cron, crontab, sleep, batch | `agendamento-at-cron-e-tarefas-periodicas.md` (+ `shell_lint.py --crontab`) |
| >, >>, <, 2>&1, pipe, tee, sort, uniq, grep -v | `redirecionamento-pipes-e-filtros.md` |
| environment variables, export, .bashrc, profile, PS1, "write a script", shebang | `ambiente-do-shell-variaveis-e-scripts.md` (+ `scripts/shell_lint.py`) |
| rpm, dpkg, apt-get, yum, install kernel, mount CD | `instalacao-de-software-e-pacotes-datado.md` [DATED] |
| tar, gzip, rsync, dd, backup, gpg | `backup-compressao-e-criptografia.md` |
| ip, ifconfig, netstat, ping, DNS, inetd, SSH, scp, telnet, proxy, PAM | `redes-servicos-e-acesso-remoto.md` |
| security, firewall, hacked, recovery, "what to close" | `seguranca-e-resposta-a-incidentes-basica.md` |
| X11, DISPLAY, vi/vim, printing, audio | `x-window-impressao-editores-e-audio.md` |
| "does the book cover X?", question about kernel/scheduling/memory, systemd, containers, cloud | `fronteira-conteudo-datado-e-encaminhamento.md` |
| terms | `glossario.md` · workflows: `procedimentos.md` · antipatterns: `casos-e-antipadroes.md` |

## Scripts (all in `scripts/`, read-only, no network; run with `python -I`)
- `linux_lookup.py`: query the index (`linux_index.json`): topics, commands (pages where they appear), `page N`, `--not-in-book`. Prints "NOT COVERED" when the collection does not cover the subject.
- `shell_lint.py`: MINIMAL static checker for shell scripts and crontabs, each finding with its origin and page; it does **not** replace shellcheck.
- `chmod_calc.py`: octal ↔ symbolic, umask (the book's subtraction vs bitwise), special modes.
- `tests/verify_citations.py` + `tests/citation-checks.json`: audit of the citations against the extracted text (166 positive, 58 negative terms in 29 groups).
