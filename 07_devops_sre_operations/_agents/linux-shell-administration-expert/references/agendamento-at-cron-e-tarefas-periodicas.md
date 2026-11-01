# Scheduling: sleep, at, batch, cron and crontab (Ch. 4, 4.4)

Pages = PDF (printed + 8). Abbreviation TLDP. Support: `python -I scripts/shell_lint.py --crontab file [--system]`.

## Three kinds of deferred execution [from source] (TLDP p.99)
1. `sleep`: waits N seconds (default) and continues; the time depends on when you submitted it.
2. `at`: runs at a set time (depends on the system clock, not on the moment of submission).
3. `cron`: periodic (hourly, daily, weekly, monthly).

## sleep
It only waits; useful for reminders `(sleep 1800; echo "Lunch time..") &`, for postponing a job when `at` is not available and for spacing out large print jobs; programmers use it to pause scripts. When leaving a job like this running, remember to lock/log out carefully or run it in `screen` [from source] (TLDP p.99-100).

## at, atq, atrm, batch
- `at tomorrow + 2 days` or `at 0237` opens a prompt for the commands (Ctrl+D ends it, showing EOT); the job uses, in order, `$SHELL`, the login shell or `/bin/sh` [from source] (TLDP p.100).
- `-m` sends an e-mail when finished (or explains why it did not run); `atq` lists the pending jobs, `atrm` removes them [from source] (TLDP p.100).
- **Choose "odd" times**: system jobs run at round hours (for example 01:00 for the locate index), so scheduling `0100` can make the load worse [from source] (TLDP p.100).
- `batch` queues the work and hands it to the system in a balanced way, avoiding peaks; by default, the queue waits for the load to drop below 0.8 [from source] (TLDP p.81, 100).

## cron and crontab
- The **cron** daemon reads the system and user crontabs: on start it looks in `/var/spool/cron/` (files named after the accounts), `/etc/cron.d/` and `/etc/crontab`, and every **minute** it checks whether there is something to do; it runs as the crontab's **owner** and e-mails the output to the owner [from source] (TLDP p.100).
- Only root can access the system crontabs; on some systems not all users may use cron (p.100).
- **Format**: 5 time fields, minute (0-59), hour (0-23), day of month (1-31), month (1-12), day of week (0-7, **0 and 7 are Sunday**); `*` = the whole range; lists `1,3,5` and ranges `1-5` [from source] (TLDP p.101). In `/etc/crontab` (cited as one of the files read, p.100) there is a sixth column with the **user** that runs the command (example on p.101); in a user's `crontab -e` no user is given (p.102).
- Variables at the top of the file (`SHELL`, `PATH`, `MAILTO`, `HOME`) [from source] (TLDP p.101, Vixie cron example).
- Vixie cron: hourly, daily, weekly and monthly jobs live in separate directories (`/etc/cron.hourly`, `.daily`, `.weekly`, `.monthly`) run via `run-parts`; the jobs are shell scripts (example: updating the locate database) [from source] (TLDP p.101).
- Editing: **`crontab -e`** (opens the editor, vi by default; avoids opening two copies); `crontab -l` lists; on saving the system reports that it installed the new crontab; **there is no need to restart** cron [from source] (TLDP p.101-102).
- The commands' output goes by e-mail to the owner (if there is no mail service, it may be in `/var/spool/mail/<user>`) [from source] (TLDP p.102).
- Book exercise: an error in the crontab (nonexistent command `coppy`) shows what happens at execution (TLDP p.104).

## Review checklist for a cron line (use `shell_lint.py --crontab`)
- 5 time fields (6 in /etc/crontab) and values within the ranges → CR001/CR002 [from source] (TLDP p.101).
- Output: without redirection, it becomes an e-mail to the owner; to silence or log it, redirect (`> /var/log/x 2>&1`) [from source p.102 for the e-mail; the redirection technique follows Ch. 5] .
- PATH: the book shows a crontab defining PATH; using absolute paths is `[inference]`.
- Top-of-the-hour schedule (minute 0): by analogy with `at`, it is worth choosing "odd" minutes `[inference]` (TLDP p.100).
- `%` in the command is a special character in cron `[extrapolation]`.

## Outside the book
systemd timers, anacron in depth (only in the glossary, p.212), cronie/fcron, `@reboot`, `*/5` steps, month/day names, flock to avoid overlap, job monitoring. If the user asks, label it `[extrapolation]`.
