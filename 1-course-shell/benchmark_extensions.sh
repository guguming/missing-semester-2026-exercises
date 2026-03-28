#!/usr/bin/env bash

set -euo pipefail

# Benchmark the five pipelines from exercise 13 as written in the notebook.
# They are not perfectly equivalent semantically; this compares runtime only.

target_dir="${1:-$HOME}"
runs="${2:-5}"

if [[ ! -d "$target_dir" ]]; then
    echo "Directory not found: $target_dir" >&2
    exit 1
fi

if ! [[ "$runs" =~ ^[0-9]+$ ]] || (( runs < 1 )); then
    echo "Runs must be a positive integer: $runs" >&2
    exit 1
fi

format_ns() {
    awk -v ns="$1" 'BEGIN { printf "%.3f ms", ns / 1000000 }'
}

run_benchmark() {
    local label="$1"
    local command="$2"
    local total_ns=0
    local min_ns=0
    local max_ns=0
    local elapsed_ns
    local start_ns
    local end_ns
    local status
    local i

    for ((i = 1; i <= runs; i++)); do
        start_ns=$(date +%s%N)
        TARGET_DIR="$target_dir" bash -lc "$command" >/dev/null 2>/dev/null
        status=$?
        end_ns=$(date +%s%N)

        if (( status != 0 )); then
            echo "Command failed for $label" >&2
            exit "$status"
        fi

        elapsed_ns=$((end_ns - start_ns))
        total_ns=$((total_ns + elapsed_ns))

        if (( i == 1 || elapsed_ns < min_ns )); then
            min_ns=$elapsed_ns
        fi

        if (( i == 1 || elapsed_ns > max_ns )); then
            max_ns=$elapsed_ns
        fi
    done

    local avg_ns=$((total_ns / runs))
    printf "%-24s avg=%12s  min=%12s  max=%12s\n" \
        "$label" \
        "$(format_ns "$avg_ns")" \
        "$(format_ns "$min_ns")" \
        "$(format_ns "$max_ns")"

    printf "%s\t%s\n" "$avg_ns" "$label" >>"$rank_file"
}

commands=(
    'find "$TARGET_DIR" -type f | grep -E '"'"'\.[^.]+$'"'"' | sed '"'"'s/.*\.//'"'"' | sort | uniq -c | sort -nr | head -5'
    'find "$TARGET_DIR" -type f | sed '"'"'s/.*\.//'"'"' | sort | uniq -c | sort -nr | head -5'
    'find "$TARGET_DIR" -type f | awk -F. '"'"'{print $NF}'"'"' | sort | uniq -c | sort -nr | head -5'
    'find "$TARGET_DIR" -type f | rev | cut -d. -f1 | rev | sort | uniq -c | sort -nr | head -5'
    'find "$TARGET_DIR" -type f -printf '"'"'%f\n'"'"' | sed '"'"'s/.*\.//'"'"' | sort | uniq -c | sort -nr | head -5'
)

labels=(
    'Method 1: grep + sed'
    'Method 2: sed'
    'Method 3: awk -F.'
    'Method 4: rev + cut'
    'Method 5: find -printf'
)

rank_file="$(mktemp)"
trap 'rm -f "$rank_file"' EXIT

echo "Target directory: $target_dir"
echo "Runs per method: $runs"
echo

for ((i = 0; i < ${#commands[@]}; i++)); do
    run_benchmark "${labels[i]}" "${commands[i]}"
done

echo
echo "Ranking by average runtime:"
rank=1
while IFS=$'\t' read -r avg_ns label; do
    printf "%d. %-24s %s\n" "$rank" "$label" "$(format_ns "$avg_ns")"
    rank=$((rank + 1))
done < <(sort -n "$rank_file")
