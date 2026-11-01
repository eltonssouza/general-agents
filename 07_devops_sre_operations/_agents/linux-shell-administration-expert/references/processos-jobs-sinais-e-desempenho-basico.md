# Processes, jobs, signals and basic performance (Ch. 4, 4.1 and 4.3)

Pages = PDF (printed + 8). Abbreviation TLDP. **Boundary:** the book treats processes from the USER/ADMIN point of view (commands and habits). Scheduling, virtual memory, concurrency and kernel internals belong to the `os-internals` agent (OSTEP); refer onward.

## Process types
- **Interactive** (started and controlled by a terminal; in the foreground they occupy the terminal, in the background they free it), **automatic/batch** (no terminal, FIFO queue: `at` by date/time, `batch` when the load is low, by default below 0.8) and **daemons** (continuous servers started at boot, e.g. xinetd) [from source] (TLDP p.79-81).
- Running in the background only makes sense for programs that do not need input from the shell (p.80).

## Job control (table 4-1)
`cmd &` (background, shows `[1] PID`), `jobs`, Ctrl+Z (suspends), Ctrl+C (interrupts), `%n` to reference, `bg`, `fg`, `kill` [from source] (TLDP p.80). `screen` keeps sessions that continue after leaving the shell and can be resumed later (p.80). The book does not mention nohup/disown/tmux `[extrapolation]`.

## Attributes
PID, PPID, nice, TTY, real and effective UID (RUID/EUID), real and effective GID (RGID/EGID); the EUID determines access to resources, and the EGID differs from the real one when the file has SGID [from source] (TLDP p.81).

## Viewing processes
- `ps` without options shows only the current shell; `ps -ef | grep user` or `ps auxw | grep bash`; grep itself may appear, **use `pgrep`** to avoid it; login shells appear with `-` in front [from source] (TLDP p.82).
- `ps` is a snapshot; `top` refreshes the list (heaviest processes, memory/swap, CPU state) by reading `/proc`; the first line of top is the same as `uptime` (load average); data also in `/var/run/utmp` and `/proc/loadavg`; `pstree` shows the relationships [from source] (TLDP p.82-84).

## Life cycle
- **fork + exec**: the process creates a copy of itself (child with the same environment, another PID) and replaces it with another program; the environment (input/output, variables, priority) is inherited; the first process, `init` (PID 1), is created at boot [from source] (TLDP p.84).
- Figure 4-1 (seen as an image, TLDP p.85) shows the chain: `init` (PID 1) forks and execs down to `getty` → `login` → `sh`, and that `sh` forks and execs `grep` with another PID [from source] (TLDP p.85).
- "Detached" daemons come to have init as their parent; the window manager does this with xterm, allowing a change of window manager without closing applications (p.85). **Zombie**: a process that ended without its parent reaping it (p.85).
- Normal termination returns an **exit status**; 0 means success (`true`); other values are specific to each program and are in the man pages. The book states that `grep` returns -1 when nothing matches [from source] (TLDP p.85) [DATED/error]: in practice `grep` returns 1 `[extrapolation]`.

## Signals (table 4-2)
`kill -l` lists them; **SIGTERM 15** ends in an orderly way; **SIGINT 2** interrupts (can be ignored); **SIGKILL 9** cannot be ignored; **SIGHUP 1** makes daemons reread their configuration; `man 7 signal` gives details [from source] (TLDP p.86).
- Book procedure: if one of your processes consumes too many resources, either make it "nicer" (nice/renice) or end it; try `kill -15` first, then SIGINT, and finally `kill -9`; confirm with `ps -ef | grep PID` [from source] (TLDP p.98). Shells are deliberately hard to kill (Ctrl+C is SIGINT) (p.98). `xkill` sends SIGKILL: only for hung applications (p.99).
- An ordinary user only affects their own processes (p.98).

## Basic performance
- `time` (Bash built-in) shows real/user/sys; GNU `/usr/bin/time` shows more, including the exit status [from source] (TLDP p.93-94).
- **Load**: what is normal depends on the machine (0 on an old firewall, 67 on a multiprocessor); measure regularly to know your normal; without that only the "feeling" of slowness remains [from source] (TLDP p.94).
- Performance depends on many things: a badly written program, disks, network, number of users, time of day (p.94). A large environment (many variables, long PATH) and heavy desktops cost time (p.94-95).
- **Priority**: a high *nice* number = "nice" process (less important); only matters for processes that use a lot of CPU; I/O processes are rewarded automatically; `nice` at start, `renice` while running; do **not** use it on interactive/foreground processes [from source] (TLDP p.95). The renice 20 example as "1/5 of the CPU" (p.98) is imprecise [DATED/extrapolation: modern range -20..19].
- **CPU**: run heavy jobs when the load is low, stop unnecessary daemons, prefer `locate` to a heavy `find`, use low priority [from source] (TLDP p.95).
- **Memory**: when RAM runs short, the system pages/swaps to disk (it does not crash, but becomes much slower); use `top`; memusage on systems with glibc; kill/stop/renice whoever uses a lot or add memory [from source] (TLDP p.95-96).
- **I/O**: weak tools at the time (ps, vmstat, top, netstat, iostat); typical bottlenecks are network and disk bandwidth; on disk, low per-process or aggregate rate; RAID, buses/controllers and checking connections [from source] (TLDP p.96).
- User profiles (many small jobs, few large ones, little long CPU) (p.97). Graphical tools (Gnome System Monitor, xload) (p.97-98) [DATED].

## Outside the book
systemd-cgls/cgroups, perf, strace, sar, PSI, OOM killer, SIGSTOP/SIGCONT, pkill/killall, modern observability metrics (other agents cover that). The book does not explain *why* the scheduler behaves this way: `os-internals`.
