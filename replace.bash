#!/bin/bash

# Check if one argument is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 replacement_string"
    exit 1
fi

# Assign the user-provided replacement string to a variable
replacement_string=$1

# Check if the replacement string is a valid Python identifier
if ! [[ "$replacement_string" =~ ^[a-zA-Z_][a-zA-Z_0-9]*$ ]]; then
    echo "Error: The replacement string must be a valid Python identifier."
    exit 1
fi

# The original string to be replaced
original_string="mypackage"

# Detect OS (Linux or macOS)
OS=$(uname)

# Function to apply sed based on OS
apply_sed() {
    local file="$1"
    if [[ "$OS" == "Darwin" ]]; then
        sed -i '' "s/$original_string/$replacement_string/g" "$file"
    else
        sed -i "s/$original_string/$replacement_string/g" "$file"
    fi
    echo "Processed $file"
}

export -f apply_sed
export original_string
export replacement_string
export OS

# perform the find and replace with appropriate sed command for file contents
echo "Replacing '$original_string' in file contents..."
find . \( -name "*.py" -or -name "*.txt" \) -type f -exec bash -c 'apply_sed "$0"' {} \;

echo "File content replacement complete."


mv mypackage ${replacement_string}

# Find all files containing 'TODO' in capital and print a warning
echo "Searching for files containing 'TODO'..."
TODO_files=$(grep -rl "TODO" ./${replacement_string})

if [ -n "$TODO_files" ]; then
    echo "WARNING: The following files contain the text 'TODO'. Please review them:"
    echo "$TODO_files"
else
    echo "No files with 'TODO' found."
fi

