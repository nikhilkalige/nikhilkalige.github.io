#!/bin/bash -e

message="$1"
size=${#message}

if [ -z "$message" ] || [ $size -lt 6 ]; then
    echo "Enter valid message"
    exit 1
fi

git checkout master
# reset to clean
git reset --hard
# remove untracked files
git clean -fdx
git checkout develop output/
git commit -m "$message"
