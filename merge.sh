#!/bin/bash -e

message="$1"
size=${#message}

if [ -z "$message" ] || [ $size -lt 6 ]; then
    echo "Enter valid message"
    exit 1
fi

git checkout master
git stash clear
git add output
git stash
# reset to clean
git reset --hard
# remove untracked files
git clean -fd
# git checkout develop output/
# git mv -f output/* .
git stash pop
rsync -a output/ .
rm -r output
git add -A
git reset -- plugins
git commit -m "$message"
