#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
CLI_PATH="$PROJECT_DIR/src/PyRebuilderSharp.Cli/bin/Release/net10.0/PyRebuilderSharp.Cli"

COMPILED_DIR="$SCRIPT_DIR/compiled"
INPUT_DIR="$SCRIPT_DIR/input"
OUTPUT_DIR="/tmp/pyrebuilder_output"

LEVELS=("level0" "level1" "level2" "level3" "level4" "level5" "level6" "level7" "level8" "level9")
PY_VERSIONS=("2.7" "3.5" "3.6" "3.7" "3.8" "3.9" "3.10" "3.11" "3.12" "3.13" "3.14")

if [ ! -f "$CLI_PATH" ]; then
    echo "Building CLI..."
    cd "$PROJECT_DIR"
    dotnet build src/PyRebuilderSharp.Cli/PyRebuilderSharp.Cli.csproj -c Release
    if [ $? -ne 0 ]; then
        echo "Build failed!"
        exit 1
    fi
fi

rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

echo "Running baseline tests..."
echo "=" 70

for level in "${LEVELS[@]}"; do
    level_input="$INPUT_DIR/$level"
    level_output="$OUTPUT_DIR/$level"
    mkdir -p "$level_output"

    echo ""
    echo "=== Level: $level ==="
    echo ""

    if [ ! -d "$level_input" ]; then
        echo "  No input files for $level"
        continue
    fi

    test_files=()
    while IFS= read -r -d '' file; do
        test_files+=("$file")
    done < <(find "$level_input" -maxdepth 1 -name "*.py" -print0)

    total_success=0
    total_fail=0
    total_orphan=0
    total_instr_not_decompiled=0

    for py_file in "${test_files[@]}"; do
        py_name=$(basename "$py_file" .py)

        for py_ver in "${PY_VERSIONS[@]}"; do
            pyc_file="$COMPILED_DIR/${py_name}.${py_ver}.pyc"

            if [ ! -f "$pyc_file" ]; then
                continue
            fi

            output_file="$level_output/${py_name}.${py_ver}.py"

            echo -n "  ${py_name}.${py_ver}.pyc..."

            output=$("$CLI_PATH" "$pyc_file" -o "$output_file" --no-header 2>&1)
            
            if [ -f "$output_file" ]; then
                total_success=$((total_success + 1))
                
                if grep "\[ORPHAN\]" "$output_file" > /dev/null 2>&1; then
                    total_orphan=$((total_orphan + 1))
                fi
                
                warn_line=$(echo "$output" | grep "\[WARN\]" | head -1)
                if [ -n "$warn_line" ]; then
                    instr_not_decompiled=$(echo "$warn_line" | awk '{print $2}')
                else
                    instr_not_decompiled="0"
                fi
                
                total_instr_not_decompiled=$((total_instr_not_decompiled + instr_not_decompiled))
                echo " OK ($instr_not_decompiled not decompiled)"
            else
                total_fail=$((total_fail + 1))
                echo " FAILED"
            fi
        done
    done

    echo ""
    echo "  Level $level Summary:"
    echo "    Success: $total_success"
    echo "    Failed: $total_fail"
    echo "    With Orphans: $total_orphan"
    echo "    Instructions not decompiled: $total_instr_not_decompiled"
    echo "    Total: $((total_success + total_fail))"
    echo ""
done

echo "=" 70
echo "Baseline tests completed."
echo ""
echo "Output directory: $OUTPUT_DIR"
