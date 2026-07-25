#!/bin/bash

# Ender 5 Pro Klipper Project Context Export
# Creates a snapshot for ChatGPT continuation

mkdir -p project/context
OUTPUT="project/context/Ender5_Project_Context_$(date +%Y%m%d_%H%M).txt"

echo "Generating Ender 5 project context..."

{
echo "================================================="
echo "ENDER 5 PRO KLIPPER PROJECT CONTEXT"
echo "$(date)"
echo "================================================="

echo
echo "================ GIT STATUS ====================="
git status

echo
echo "================ LAST COMMIT ===================="
git log -1 --oneline

echo
echo "================ PROJECT TREE ==================="

find . \
-not -path './.git/*' \
-not -name "*.gcode" \
-not -name "*.log" \
-type f | sort


echo
echo "================ DOCUMENTATION =================="

find . \
-name "*.md" \
-not -path './.git/*' \
| sort \
| while read file
do
    echo
    echo "-------------------------------------------------"
    echo "$file"
    echo "-------------------------------------------------"
    cat "$file"
done


echo
echo "================ KLIPPER CONFIG ================="

find . \
\( -name "*.cfg" -o -name "*.conf" \) \
-not -path './.git/*' \
| sort \
| while read file
do
    echo
    echo "-------------------------------------------------"
    echo "$file"
    echo "-------------------------------------------------"
    cat "$file"
done


echo
echo "================ END CONTEXT ===================="

} > "$OUTPUT"

echo
echo "Created:"
echo "$OUTPUT"
