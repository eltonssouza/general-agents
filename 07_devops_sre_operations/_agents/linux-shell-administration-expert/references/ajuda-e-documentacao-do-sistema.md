# Help, system documentation, session and Bash shortcuts (Ch. 2)

Pages = PDF (printed + 8). Abbreviation TLDP.

## The book's stance
- The book treats reading the documentation as a core habit: GNU/Linux is about becoming self-sufficient; asking for help without having tried man/info/--help is usually poorly received [from source] (TLDP p.30, 31, 36).
- It presents the shell as "the control panel"; the terminal (xterm) is opened from the graphical environment [from source] (TLDP p.27).

## Session and root account
- Avoid logging in as root, especially in graphical mode: the graphical session runs many extra programs with too many permissions [from source] (TLDP p.26).
- In text mode, use root only for what requires privilege (creating users, installing packages, configuring the network) and log out of the account afterwards; some systems, such as Ubuntu, force sudo [from source] (TLDP p.28).
- The preferred way to obtain privilege is to switch user (su), not to keep a root session [from source] (TLDP p.30). The book returns to the subject in security: sudo is better than su for running only the necessary command (TLDP p.194).
- In text mode the typed password shows no echo; this is normal and is for security [from source] (TLDP p.28).
- Shutting down with the power button is equivalent to the halt procedure only on new systems; on old systems it can cause damage [from source] (TLDP p.28) [DATED].

## Initial commands and anatomy of a command
- Table 2-1: ls, cd, passwd, file, cat, pwd, exit/logout, man, info, apropos [from source] (TLDP p.29).
- Options with one dash (-a); GNU long options with two (--all); arguments say what the command acts on; `.` and `..` are special directories; the directory separator is `/` [from source] (TLDP p.29).

## Bash shortcuts (table 2-2)
Ctrl+A/Ctrl+E (start/end of line), Ctrl+C (ends the program), Ctrl+D (exits the shell), Ctrl+L (clears), Ctrl+R (history search), Ctrl+Z (suspends), arrows (history), Tab (completes) and Tab Tab (lists possibilities) [from source] (TLDP p.30-31). Completion of command and file names works for any argument (TLDP p.31).

## Where to look for help
1. **man**: pages in numbered sections; the lowest-numbered one appears first; `man 5 passwd` chooses a section; `man -a passwd` shows all; navigate with space and `b`, quit with `q`; the pager is usually less [from source] (TLDP p.31-33). Typical sections of a page: name, synopsis (brackets = optional), description, options, environment, "SEE ALSO", bugs (TLDP p.32-33).
2. **info**: usually more recent and easier to use; `info info` teaches how to navigate [from source] (TLDP p.33-34). The book states that HOWTOs, FAQs and man pages are being incorporated into Info pages [from source] (TLDP p.60) [DATED: today man remains the primary source].
3. **whatis / apropos**: short name+description index; `apropos browser` lists candidates; a section (1) page points to a command to try as a user [from source] (TLDP p.34).
4. **--help**: usage and options summary of GNU commands [from source] (TLDP p.34-35).
5. **Exceptions**: shell built-in commands (cd, exit, logout, pwd) have no page of their own, consult the shell's; if the man pages "disappeared", check MANPATH; some packages only have documents in `/usr/share/doc`; if the documentation was removed, reinstall the package [from source] (TLDP p.36).
6. Graphical help (Konqueror `man:ls`/`info:info`, gnome-help, nautilus) [from source] (TLDP p.35-36) [DATED].

## Limits
The book does not cover tldr, cheat sheets, searching forums as a structured method, container/cloud documentation or modern help tools `[extrapolation]` if the user asks.
