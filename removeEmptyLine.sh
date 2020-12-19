#!/bin/bash


OUTPUT=OUTPUTnew/
mkdir -p $OUTPUT
# m=( $(find /home/d/__PRODUCTION/indexer_sqlite3_fts5/patxt/ -type f ;))
for i in  /home/d/__PRODUCTION/indexer_sqlite3_fts5/patxt/*.txt; do
    echo "$i"
    # k=$OUTPUT$i
    # mkdir -p "$(dirname "$k")"
    # cat "$i" | grep "\S" > "${OUTPUT}""${i}".txt

done
