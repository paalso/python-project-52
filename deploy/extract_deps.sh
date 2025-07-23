#!/bin/bash

# Function to display help message
show_help() {
  echo "Usage: $0 [OPTIONS]"
  echo "Extracts dependencies from a specified pyproject.toml and saves them to requirements.txt"
  echo "in the same directory as the pyproject.toml file."
  echo ""
  echo "Options:"
  echo "  -p, --path <file>   Specify the path to the pyproject.toml file (required)."
  echo "  -h, --help          Display this help message."
}

# Initialize variable for pyproject.toml path
PYPROJECT_PATH=""

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
  case $1 in
    -p|--path)
      if [ -n "$2" ] && [ "${2:0:1}" != "-" ]; then # Check if next arg exists and isn't another option
        PYPROJECT_PATH="$2"
        shift # Move to the next argument after the path
      else
        echo "Error: --path requires a file path argument."
        show_help
        exit 1
      fi
      ;;
    -h|--help)
      show_help
      exit 0
      ;;
    *)
      echo "Error: Unknown option: $1"
      show_help
      exit 1
      ;;
  esac
  shift # Move to the next argument
done

# ---
# Validate the provided pyproject.toml path
# ---

# Check if a path was provided
if [ -z "$PYPROJECT_PATH" ]; then
  echo "Error: No pyproject.toml path provided. Use -p or --path."
  show_help
  exit 1
fi

# Check if the file exists
if [ ! -f "$PYPROJECT_PATH" ]; then
  echo "Error: pyproject.toml not found at '$PYPROJECT_PATH'."
  exit 1
fi

# Get the directory of the pyproject.toml file
# This is where requirements.txt will be saved
PYPROJECT_DIR=$(dirname "$PYPROJECT_PATH")

# Define the output file path
OUTPUT_FILE="$PYPROJECT_DIR/requirements.txt"

# ---
# Extract dependencies using awk
# ---

echo "Extracting dependencies from '$PYPROJECT_PATH'..."
awk '
  /\[project\]/ { in_project_section=1; }
  /dependencies = \[/ { if (in_project_section) { in_dependencies_section=1; next; } }
  in_dependencies_section {
    # Check for the end of the list (starts with ']') or end of the section (empty line or new section)
    if ($0 ~ /\]$/ || $0 ~ /^\s*$/ || $0 ~ /^\[.*\]/) {
      in_dependencies_section=0;
      next;
    }
    # Print the dependency, removing leading/trailing quotes and commas, and trimming whitespace
    gsub(/"/, "", $0);
    gsub(/,$/, "", $0);
    print $0;
  }
' "$PYPROJECT_PATH" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//;/^$/d' > "$OUTPUT_FILE"

# ---
# Final check
# ---

# Check if the requirements.txt file was created and has content
if [ -s "$OUTPUT_FILE" ]; then
  echo "Dependencies successfully extracted to '$OUTPUT_FILE'"
else
  echo "No dependencies found or extraction failed. '$OUTPUT_FILE' might be empty."
  exit 1 # Indicate an error if no dependencies were written
fi
