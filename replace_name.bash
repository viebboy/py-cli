#!/bin/bash

# Check if one argument is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 new-name-for-your-package"
    exit 1
fi

replacement_string=$1

original_string="mypackage"

find . -type f -exec sed -i "s/$original_string/$replacement_string/g" {} +

echo "Replacement complete."

# find all instances of todo
echo "Searching for files containing 'TODO'..."
TODO_files=$(grep -rl "TODO" .)

if [ -n "$TODO_files" ]; then
    echo "WARNING: The following files contain the text 'TODO'. Please review them:"
    echo "$TODO_files"
else
    echo "No files with 'TODO' found."
fi
