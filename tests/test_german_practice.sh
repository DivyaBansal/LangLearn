#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
script="$script_dir/german-terminal-practice.sh"

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

edit_dir="$(mktemp -d)"
trap 'rm -rf "$edit_dir"' EXIT
printf 'old question\told answer\n' > "$edit_dir/sentences.tsv"
printf 'gehen\tgo\tIch gehe.\n' > "$edit_dir/separable-verbs.tsv"
printf 'kommen\tcome\tIch komme.\n' > "$edit_dir/inseparable-verbs.tsv"

printf '1\ne\nq\nnew question\nm\n4\n' |
  GERMAN_PRACTICE_CORPUS="$edit_dir/sentences.tsv" \
  GERMAN_PRACTICE_SEPARABLE_VERBS="$edit_dir/separable-verbs.tsv" \
  GERMAN_PRACTICE_INSEPARABLE_VERBS="$edit_dir/inseparable-verbs.tsv" \
  TERM=xterm bash "$script" >/dev/null 2>&1

if [[ "$(<"$edit_dir/sentences.tsv")" != $'new question\told answer' ]]; then
  echo "Expected the sentence question to be editable."
  exit 1
fi

printf '2\ne\na\nnew meaning\nm\n4\n' |
  GERMAN_PRACTICE_CORPUS="$edit_dir/sentences.tsv" \
  GERMAN_PRACTICE_SEPARABLE_VERBS="$edit_dir/separable-verbs.tsv" \
  GERMAN_PRACTICE_INSEPARABLE_VERBS="$edit_dir/inseparable-verbs.tsv" \
  TERM=xterm bash "$script" >/dev/null 2>&1

if [[ "$(<"$edit_dir/separable-verbs.tsv")" != $'gehen\tnew meaning\tIch gehe.' ]]; then
  echo "Expected the verb answer to be editable without losing the example."
  exit 1
fi

echo "Menu test passed"
echo "Verb practice test passed"
echo "Edit test passed"
