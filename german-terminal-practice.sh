#!/usr/bin/env bash

# UI colors and symbols
BLUE='\033[1;34m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
CYAN='\033[1;36m'
MAGENTA='\033[1;35m'
RED='\033[1;31m'
DIM='\033[2m'
RESET='\033[0m'

if [[ ! -t 1 || "${NO_COLOR:-}" == "1" ]]; then
  BLUE=''
  GREEN=''
  YELLOW=''
  CYAN=''
  MAGENTA=''
  RED=''
  DIM=''
  RESET=''
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="${GERMAN_PRACTICE_DATA_DIR:-$SCRIPT_DIR/data}"
CORPUS="${GERMAN_PRACTICE_CORPUS:-$DATA_DIR/sentences.tsv}"

SEPARABLE_VERB_FILE="${GERMAN_PRACTICE_SEPARABLE_VERBS:-$DATA_DIR/separable-verbs.tsv}"
INSEPARABLE_VERB_FILE="${GERMAN_PRACTICE_INSEPARABLE_VERBS:-$DATA_DIR/inseparable-verbs.tsv}"

if [[ ! -s "$SEPARABLE_VERB_FILE" ]]; then
  echo "Verb file not found or empty: $SEPARABLE_VERB_FILE"
  exit 1
fi

if [[ ! -s "$INSEPARABLE_VERB_FILE" ]]; then
  echo "Verb file not found or empty: $INSEPARABLE_VERB_FILE"
  exit 1
fi

mapfile -t SEPARABLE_VERBS < <(grep -vE '^(#|$)' "$SEPARABLE_VERB_FILE")
mapfile -t INSEPARABLE_VERBS < <(grep -vE '^(#|$)' "$INSEPARABLE_VERB_FILE")

clear_screen() {
  if [[ -t 1 && -t 0 && -n "${TERM:-}" && "$TERM" != dumb ]]; then
    clear
  else
    printf '\n'
  fi
}

print_banner() {
  local title="$1"
  local color="$2"
  local line="────────────────────────────────────────"
  printf '%b%s%b\n' "$color" "$line" "$RESET"
  printf '%b  %s%b\n' "$color" "$title" "$RESET"
  printf '%b%s%b\n' "$color" "$line" "$RESET"
}

print_footer() {
  printf '\n%b%s%b\n' "$DIM" "────────────────────────────────────────" "$RESET"
  printf '%b  q  Beenden   •   Strg+C  Sofort beenden%b\n' "$DIM" "$RESET"
}

print_status() {
  local label="$1"
  local value="$2"
  printf '%b  %-12s%b %s\n' "$DIM" "$label" "$RESET" "$value"
}

print_menu() {
  clear_screen
  echo
  print_banner "Deutsch-Lernprogramm" "$MAGENTA"
  echo
  printf '%bWähle einen Modus%b\n' "$CYAN" "$RESET"
  echo
  printf '  %b[1]%b  Satz übersetzen\n' "$GREEN" "$RESET"
  printf '  %b[2]%b  Trennbare Verben lernen\n' "$GREEN" "$RESET"
  printf '  %b[3]%b  Untrennbare Verben lernen\n' "$GREEN" "$RESET"
  printf '  %b[4]%b  Beenden\n' "$GREEN" "$RESET"
  echo
  print_status "Datenquelle" "$DATA_DIR"
  print_footer
}

show_sentence_mode() {
  if [[ ! -s "$CORPUS" ]]; then
    echo "Corpus file not found or empty: $CORPUS"
    exit 1
  fi

  while true; do
    line="$(shuf -n 1 "$CORPUS" 2>/dev/null)" || {
      echo "Could not pick a sentence from: $CORPUS"
      exit 1
    }

    english="${line%%$'\t'*}"
    german="${line#*$'\t'}"

    if [[ "$english" == "$german" ]]; then
      echo "Skipping invalid line without TAB separator:"
      echo "$line"
      echo
      continue
    fi

    clear_screen
    print_banner "Übersetzungsübung" "$BLUE"
    printf '%b  t  Übersetzung anzeigen   n  Nächster Satz   m  Hauptmenü%b\n' "$CYAN" "$RESET"
    echo
    printf "${YELLOW}🇬🇧  %s${RESET}\n\n" "$english"

    while true; do
      printf 'Befehl [t/n/m]: '
      IFS= read -rsn1 key
      printf '%s\n' "$key"

      case "$key" in
        t|T)
          printf "\n${GREEN}🇩🇪  %s${RESET}\n\n" "$german"
          ;;
        n|N)
          break
          ;;
        m|M)
          return 0
          ;;
        *)
          echo -e "${RED}Verwende t für Übersetzung, n für nächsten Satz, m für Menü oder Strg+C zum Beenden.${RESET}"
          ;;
      esac
    done
  done
}

run_verb_practice() {
  local mode="$1"
  local -a verb_bank=()
  local title=""

  if [[ "$mode" == "separable" ]]; then
    verb_bank=("${SEPARABLE_VERBS[@]}")
    title="Trennbare Präfixe"
  else
    verb_bank=("${INSEPARABLE_VERBS[@]}")
    title="Untrennbare Präfixe"
  fi

  while true; do
    local index=$((RANDOM % ${#verb_bank[@]}))
    local entry="${verb_bank[$index]}"
    IFS=$'\t' read -r german english example <<< "$entry"

    clear_screen
    print_banner "Verbtraining: $title" "$YELLOW"
    printf '%b  b  Bedeutung anzeigen   n  Nächstes Verb   m  Hauptmenü%b\n' "$CYAN" "$RESET"
    echo
    printf "${GREEN}🇩🇪  %s${RESET}\n\n" "$german"

    while true; do
      printf 'Befehl [b/n/m/e]: '
      IFS= read -rsn1 key
      printf '%s\n' "$key"

      case "$key" in
        b|B)
          echo
          echo -e "${GREEN}Bedeutung: $english${RESET}"
          echo
          echo "Beispiel: $example"
          echo
          continue
          ;;
        n|N)
          break
          ;;
        m|M)
          return 0
          ;;
        e|E)
          exit 0
          ;;
        *)
          echo -e "${RED}Verwende b für die Bedeutung, n für das nächste Verb, m für das Hauptmenü oder e zum Beenden.${RESET}"
          ;;
      esac
    done
  done
}

while true; do
  print_menu
  printf 'Wähle eine Option [1-4]: '
  IFS= read -r choice
  echo

  case "$choice" in
    1)
      show_sentence_mode
      ;;
    2)
      run_verb_practice "separable"
      ;;
    3)
      run_verb_practice "inseparable"
      ;;
    4|q|Q)
      echo -e "${MAGENTA}Auf Wiedersehen!${RESET}"
      exit 0
      ;;
    *)
      echo -e "${RED}Ungültige Auswahl. Bitte wähle 1, 2, 3 oder 4.${RESET}"
      echo
      ;;
  esac
done
