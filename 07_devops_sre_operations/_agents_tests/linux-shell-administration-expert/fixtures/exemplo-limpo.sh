#!/bin/bash
# copies regular files to .old
for f in ./*; do
    [ -f "$f" ] && cp -- "$f" "$f.old"
done
case "$1" in
  start) echo "starting" ;;
  *) echo "Usage: $0 {start}"; exit 1 ;;
esac
tail -5 wishlist > newlist && mv newlist wishlist
make all > build.log 2>&1
pgrep httpd
sort < data.txt | uniq > /var/tmp/data.uniq
exit 0
