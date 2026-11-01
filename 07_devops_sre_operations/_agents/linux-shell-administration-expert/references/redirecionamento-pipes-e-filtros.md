# Redirection, pipes, tee and filters (Ch. 5)

Pages = PDF (printed + 8). Abbreviation TLDP. Support: `scripts/shell_lint.py` (rules SH005-SH007, SH012, SH013).

## Concepts
- Commands read **stdin** (keyboard by default) and write to **stdout** (screen); the error output is **stderr**; descriptors: 0, 1 and 2 [from source] (TLDP p.105, 108).
- Redirecting output is done with `>` (file) or `|` (another command's input) [from source] (TLDP p.105).

## Operators
- `>` **creates or overwrites** the file; be careful. In Bash, `set -o noclobber` (in .bashrc) protects against accidental overwriting [from source] (TLDP p.105-106).
- `> file` without a command **truncates** the file to 0 bytes (or creates it empty) [from source] (TLDP p.106, 120).
- `<` feeds the input (`mail mike@host < to_do`); the book calls the form `cat file | mail someone` the "beginner's version" and considers `<` more elegant [from source] (TLDP p.106-107).
- `>>` **appends** to the file (`date >> wishlist`) (TLDP p.107-108).
- Combinations: `spell < text.txt > error.log`; pipes chain as many commands as you like, as long as they read stdin and write stdout; some commands have an option to behave this way (TLDP p.107).

## Descriptors and stderr
- Without a number, `<` is descriptor 0 and `>` is 1 [from source] (TLDP p.108).
- `ls > dirlist 2>&1` sends **stdout and stderr** to the file; `ls 2>&1 > dirlist` sends **only stdout** (stderr was pointed to where stdout was before) [from source] (TLDP p.108). **Order matters**.
- The `&` in `2>&1` is not "background": it indicates that what follows is a descriptor, not a file; **there must be no space** between the number and `>` (`ls 2 > tmp` redirects stdout to the file `tmp` and treats `2` as an argument) [from source] (TLDP p.108).
- Uses: `command 2>&1 | less` to study errors (`make all 2>&1 | less`); `make all 2> /dev/pts/7` sends errors to another terminal (find the tty with `tty`) [from source] (TLDP p.109).
- `tee` copies to the screen **and** to files (`date | tee file1 file2`; `-a` appends) [from source] (TLDP p.109).

## Filters
- **grep**: shows matching lines; `-v` inverts, `-i` ignores case, `-r` recursive, `--colour`, `--after-context`; regular expressions: start with the grep documentation (Info) [from source] (TLDP p.110).
- **sort**: alphabetical order by default; `ls -la | sort -nk 5` sorts by size; `sort +4n` is the old syntax [from source] (TLDP p.110).
- **uniq** (or `sort -u`) filters duplicate entries; the book shows `sort itemlist | uniq` [from source] (TLDP p.110-111). That `uniq` only removes *adjacent* repetitions (which is why one sorts first) is `[extrapolation]`.
- Book examples: `grep pattern1 file | grep -v pattern2`, `ls -la | less`, `ls -l | grep part_of_name` (TLDP p.106).
- Exercise: why does `tail testfile > testfile` not work? Because the shell opens and truncates the output file before `tail` reads it (the book presents the question, TLDP p.143, and the mechanics of truncation on p.106).

## Common mistakes
1. Reading and writing the same file in the same command (`sort f > f`): empty file (rule SH005).
2. `2>&1 > file` in the wrong order (SH006).
3. `2 > file` with a space (SH007).
4. `ps | grep x` listing grep itself: `pgrep` (SH012; TLDP p.82).
5. `cat f | cmd` when `cmd < f` will do (SH013).

## Outside the book
Here-doc/here-string, process substitution, `exec` with descriptors, `mkfifo`, `&>>`, `set -o pipefail`, `sed`/`awk` in depth (awk only in the glossary), `xargs -0`. `[extrapolation]`.
