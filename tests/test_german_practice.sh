#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
script="$script_dir/german-terminal-practice.sh"
separable_verbs="$script_dir/data/separable-verbs.tsv"

if ! awk -F '\t' '
  NF != 3 || $1 == "" || $2 == "" || $3 == "" { exit 1 }
' "$separable_verbs"; then
  echo "Expected every separable verb row to have three populated TSV columns."
  exit 1
fi

if [[ "$(cut -f1 "$separable_verbs" | sort | uniq -d)" != "" ]]; then
  echo "Expected every separable verb infinitive to be unique."
  exit 1
fi

set +e
output="$(timeout 3s bash "$script" <<< "4" 2>&1)"
status=$?
set -e

if [[ $status -eq 124 ]]; then
  echo "Expected the script to exit when the user chooses the exit option."
  exit 1
fi

if [[ "$output" != *"Wähle einen Modus"* ]]; then
  echo "Expected the script to show the main menu."
  exit 1
fi

if [[ "$output" != *"Beenden"* ]]; then
  echo "Expected the exit option to be listed in the menu."
  exit 1
fi

set +e
verb_output="$(printf '2\nb\nm\n4\n' | timeout 3s bash "$script" 2>&1)"
verb_status=$?
set -e

if [[ $verb_status -eq 124 ]]; then
  echo "Expected the verb practice mode to respond to b and return to the menu."
  exit 1
fi

if [[ "$verb_output" != *"Bedeutung:"* ]]; then
  echo "Expected the verb practice mode to show the meaning when b is pressed."
  exit 1
fi

echo "Menu test passed"
echo "Verb practice test passed"
echo "Separable verb data test passed"
