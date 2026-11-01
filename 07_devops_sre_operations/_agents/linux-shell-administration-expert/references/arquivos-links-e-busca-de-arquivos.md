# Files: PATH, ls, create/move/remove, search, viewing and links (Ch. 3, 3.2-3.3)

Pages = PDF (printed + 8). Abbreviation TLDP.

## PATH, paths and home
- The shell looks for the executable in the `$PATH` directories in order and **stops at the first hit**; so "command not found" is usually an incomplete PATH, and a personal program in ~/bin can shadow another with the same name (the homemade `wc` example) [from source] (TLDP p.48-49).
- `which` diagnoses the problem; `which -a` lists all occurrences and shows aliases (TLDP p.48, 62).
- `export PATH=...` is valid only for the session; to persist, use the shell's setup files (See `ambiente-do-shell-variaveis-e-scripts.md`) [from source] (TLDP p.49). To put the personal directory last: `export PATH=...:$HOME/bin` (p.49). To append: `export PATH=$PATH:/opt/acroread/bin` (p.62).
- A path that starts with `/` is absolute; without a slash it is relative; `./configure` runs the program in the current directory [from source] (TLDP p.49).
- `su - user` opens a shell in another user's environment [from source] (TLDP p.48).
- Home: variable HOME, shortcut `~`; `quota -v` shows limits (no quota, no limitation) [from source] (TLDP p.51-52).

## Listing and identifying
- `ls -a` shows hidden files (names with a dot); `.` and `..` exist in every directory; `ls -l` shows permissions, links, owner, size, date; `ls -ltr` puts the most recent last; `ls -ld dir` describes the directory itself [from source] (TLDP p.56). Colors (table 3-5) and suffixes (table 3-6) indicate type (p.56-57).
- `file` tries to guess the format by tests and magic numbers; it is only a guess and **can be fooled**; check before using text tools, which can "break" the terminal with binaries [from source] (TLDP p.57-58).

## Create, copy, move, remove
- `mkdir -p` creates the whole chain; without `-p`, it fails if the parent does not exist [from source] (TLDP p.59-60). Names: case-sensitive, no two identical in the same directory; avoid characters special to the shell (p.60).
- `mv` renames and moves (only the name changes; other properties stay) (p.60). `cp -R source destination` copies recursively (p.60-61).
- `rm` removes files, `rmdir` only empty directories; **there is no trash in the shell**: removed is lost, only recoverable from backup; `-i` on rm, cp and mv asks for confirmation; the options that remove whole trees are "rather dangerous" (the book's words) [from source] (TLDP p.61).
- The book never writes `rm -rf` anywhere; the specific warning about `rm -rf` with an empty variable is `[extrapolation]`.

## Search
- **Globbing**: `*`, `?`, `[a-z]` are expanded by the shell before the command (`mv ../report[1-4].doc dest/`); Tab completes names (TLDP p.60-62).
- **find**: `find <path> -name <pattern>` searches by **name**, not by content; size (`-size +5000k`) and date criteria; actions with `-exec` (p.62-63). `find . -name "*.tmp" -exec rm {} \;` runs rm once per file; `find ... | xargs rm` is more economical; test the selection before deleting [from source] (TLDP p.63).
- **locate/slocate**: uses an index updated once a day (fast, may be stale); slocate respects permissions [from source] (TLDP p.63).
- **grep**: filters lines by pattern (`grep -a find .bash_history`, `grep -i`, `grep -r`, `-v` inverts), also works for lists such as `/etc/passwd`; **Ctrl+R** does reverse search in the history (`.bash_history` is written when the session ends) [from source] (TLDP p.64-65, 110).
- **Escape**: the backslash removes the special meaning: `less \*`, `cat This\ File` [from source] (TLDP p.65).

## Viewing
- `cat` dumps; `more` and `less` page (less is the GNU version, with search and backward scrolling); `head`/`tail` show the start/end (`tail -10`); **`tail -f`** follows a growing file, used on logs [from source] (TLDP p.65-66).
- Before opening binary files with these tools, run `file` (p.65). Accent problems are an encoding issue, not the command's (p.65-66; see `ambiente-do-shell-variaveis-e-scripts.md`).

## Links
- **Hard link**: two or more names for the same inode; they share data and **do not cross partitions** (inodes are per partition); every regular file is, in principle, a hard link [from source] (TLDP p.66-67).
- **Symlink**: a small file with the target's path; it crosses partitions; if the target disappears, the link becomes useless; `ln -s target name` (p.67-68).
- Figure 3-2 (seen as an image, TLDP p.67) shows `file` and `hlink` pointing to the same inode (N1) and data, while `slink` points to another inode (N2) whose data is the target's path (visual observation of the figure) [from source] (TLDP p.67).
- Symlinks are always small; hard links have the size of the original (p.68). Uses: saving space, satisfying installations that expect the file elsewhere, moving /home to another disk with `/home -> /disk2/home` (p.68).
- The book also mentions "user-space links" (.desktop shortcuts) that only the graphical manager interprets (p.67).

## Not covered
`find -print0`/`xargs -0` (names with spaces), fd/ripgrep, stat, tree, lsattr, mktemp, bind mounts, links on directories: `[extrapolation]` if the user asks.
