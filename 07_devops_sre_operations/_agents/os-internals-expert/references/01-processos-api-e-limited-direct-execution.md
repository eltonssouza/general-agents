# 01. Processes, process API and Limited Direct Execution (ch. 2, 4, 5, 6)

Page convention: `p.N` = PDF page ("=== PAGE N ===" marker of the extracted text). PDF pages of this chapter group: ch.2 = p.271-289; ch.4 = p.30-42; ch.5 = p.106-120; ch.6 = p.182-197. Printed page within the chapter = PDF p. − start + 1.

Open this file when the question is: what is a process, states, fork/exec/wait, shell redirection, trap/syscall, timer interrupt, context switch, user/kernel mode.

## 1. Core ideas

- **[from source]** The OS virtualizes resources (CPU, memory, disk), turning them into virtual forms that are easier to use; that is why it is called a "virtual machine", a "standard library" (hundreds of system calls) and a "resource manager" (OSTEP p.272). The central question is *how* (mechanisms and policies), not *why* (p.272).
- **[from source]** Process = running program; illusion of many CPUs through **time sharing** (cost: each one runs more slowly); the opposite is **space sharing** (disk) (OSTEP p.30-31).
- **[from source]** **Mechanism** answers "how" (e.g., context switch); **policy** answers "which" (e.g., scheduling); separating the two gives modularity (OSTEP p.31-32).
- **[from source]** Machine state of a process: memory (address space), registers (PC, stack pointer, frame pointer) and I/O information (open files) (OSTEP p.31-32).
- **[from source]** Generic process API: create, destroy, wait, miscellaneous controls (suspend/resume), status (OSTEP p.32).

## 2. Process creation and states

- **[from source]** Creating a process: load code and static data (in old OSes all at once, "eager"; in modern ones on demand, "lazy"), allocate the stack (with argc/argv) and possibly the heap, initialize I/O (three standard descriptors: input, output, error) and jump to main() (OSTEP p.33-34).
- **[from source]** States: **Running**, **Ready**, **Blocked**; transitions scheduled/descheduled and I/O initiate/done (Fig.4.2); when I/O starts the process blocks and another one uses the CPU (OSTEP p.34-36).
- **[from source]** Structures: process list and **PCB** (process control block, also process descriptor); xv6 has extra states (UNUSED, EMBRYO, SLEEPING, RUNNABLE, RUNNING, ZOMBIE); **zombie** = finished, not yet cleaned up; the parent reads the return code with wait() (OSTEP p.36-38).
- **[from source]** Chapter simulator: `process-run.py` (flags -l, -S SWITCH_ON_IO/SWITCH_ON_END, -I IO_RUN_LATER/IO_RUN_IMMEDIATE) (OSTEP p.41-42).

## 3. UNIX API: fork, wait, exec, shell

- **[from source]** `fork()` creates a child that is an almost exact copy of the parent (own address space, registers, PC); the parent receives the child's PID, the child receives 0; execution order is nondeterministic (scheduler) (OSTEP p.107-109).
- **[from source]** `wait()`/`waitpid()` blocks the parent until the child finishes and makes the output deterministic; there are cases where wait returns before the child finishes (OSTEP p.109 and note 2).
- **[from source]** `exec()` loads another executable, overwriting code and static data; heap/stack are reinitialized; it **does not create a new process**; a successful exec does not return; Linux has six variants (execl, execlp, execle, execv, execvp, execvpe) (OSTEP p.109-111).
- **[from source]** Why separate fork and exec: the shell runs code between the two (in the child) to change the environment. Redirection (`wc p3.c > newfile.txt`): closes stdout, opens the file (UNIX looks for the lowest free fd starting from 0) and runs; open descriptors survive exec (OSTEP p.111-113). Pipes use `pipe()` (queue in the kernel) (OSTEP p.112).
- **[from source]** Signals: `kill()`, ctrl-c = SIGINT, ctrl-z = SIGTSTP, `signal()` to handle them; a user only controls their own processes; superuser/root controls all (OSTEP p.113-115). Tools: ps, top, kill, killall (p.114-115).
- **[from source]** The authors cite a critique of fork (a paper arguing for `spawn()`) and remind readers that their views are opinionated (OSTEP p.115).
- **[extrapolation]** Copy-on-write in fork appears in ch.23 (p.729-730), not in this chapter.

## 4. Limited Direct Execution (LDE)

- **[from source]** Two challenges: performance and control; solution "limited direct execution": run directly on the CPU, but with limits (OSTEP p.182-183).
- **[from source]** Restricted operations: **user mode** (I/O raises an exception) and **kernel mode**; system call = **trap** instruction + **return-from-trap**; libc packs the syscall number and arguments and executes the trap; the hardware saves PC/flags/registers on a per-process **kernel stack**; the kernel sets up the **trap table** at boot (privileged instruction); the user never chooses the jump address, only the syscall number (OSTEP p.184-187). The kernel must validate arguments coming from the user (OSTEP p.187).
- **[from source]** Switching between processes: **cooperative** approach (syscalls, yield, illegal actions; an infinite loop requires a reboot) versus **non-cooperative** with a **timer interrupt** programmed at boot (privileged) (OSTEP p.188-190).
- **[from source]** **Context switch**: the scheduler decides; low-level code saves the current process's registers and restores the next one's, switching the kernel stack; two kinds of save/restore: implicit (hardware, user regs → kernel stack) and explicit (OS, kernel regs → process structure) (OSTEP p.190-193).
- **[from source]** Reboot is a legitimate robustness tool (OSTEP p.191). Concurrency inside the kernel: disable interrupts for short periods and use internal locks (OSTEP p.192-193).
- **[DATED]** 1996 measurements (syscall ~4 µs, context switch ~6 µs on a P6 200 MHz); modern systems are sub-microsecond (OSTEP p.194).
- **[inference]** The practical cost of a context switch also includes cold caches/TLB (ch.7 says a switch flushes state in caches, TLBs and branch predictors, p.297).

## 5. Pitfalls

- Confusing exec with fork: exec does not create a process (p.111).
- Forgetting that `wait()` is not mandatory for ordering, but is the book's tool for making the output deterministic (p.109).
- Assuming `fork` physically copies memory: the book only says "almost a copy" here; the COW optimization is in ch.23 (p.729-730).
