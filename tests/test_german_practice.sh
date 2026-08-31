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

echo "Menu test passed"
echo "Verb practice test passed"

practice_data="$(mktemp)"
trap 'rm -f "$practice_data"' EXIT
printf 'aufstehen\tget up\tI get up.\tIch stehe auf.\n' > "$practice_data"

split_output="$(printf '5\nIch stehe auf.\nm\n4\n' | GERMAN_PRACTICE_SEPARABLE_PRACTICE="$practice_data" timeout 3s bash "$script" 2>&1)"
if [[ "$split_output" != *"Richtig!"* ]]; then
  echo "Expected a correctly split separable verb to be accepted."
  exit 1
fi

unsplit_output="$(printf '5\nIch aufstehe.\nm\n4\n' | GERMAN_PRACTICE_SEPARABLE_PRACTICE="$practice_data" timeout 3s bash "$script" 2>&1)"
if [[ "$unsplit_output" == *"Richtig!"* ]] || [[ "$unsplit_output" != *"Noch nicht."* ]]; then
  echo "Expected an unsplit separable verb to be rejected."
  exit 1
fi

echo "Separable verb drill test passed"
