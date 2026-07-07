#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INPUT_DIR="$SCRIPT_DIR/input"
COMPILED_DIR="$SCRIPT_DIR/compiled"

PY_VERSIONS=("3.12" "3.14")

for level in level0 level1 level2 level3 level4 level5 level6 level7 level8 level9; do
    level_input="$INPUT_DIR/$level"
    if [ ! -d "$level_input" ]; then
        continue
    fi

    for py_file in "$level_input"/*.py; do
        py_name=$(basename "$py_file" .py)

        for py_ver in "${PY_VERSIONS[@]}"; do
            pyc_file="$COMPILED_DIR/${py_name}.${py_ver}.pyc"
            
            if [ -f "$pyc_file" ]; then
                echo "Skipping (exists): ${py_name}.${py_ver}.pyc"
                continue
            fi

            python_cmd="python${py_ver}"
            if ! command -v "$python_cmd" &> /dev/null; then
                echo "Python $py_ver not available, skipping"
                continue
            fi

            echo "Compiling: ${py_name}.${py_ver}.pyc"
            "$python_cmd" -c "import py_compile; py_compile.compile('$py_file', '$pyc_file', doraise=True)" 2>&1 || echo "  Failed"
        done
    done
done

echo ""
echo "Compilation completed."
