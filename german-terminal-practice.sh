#!/usr/bin/env bash

# Colors
BLUE='\033[1;34m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
CYAN='\033[1;36m'
MAGENTA='\033[1;35m'
RED='\033[1;31m'
RESET='\033[0m'

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

print_header() {
  local text="$1"
  local color="$2"
  local width=46
  local padding=$(( (width - ${#text}) / 2 ))
  local left_padding=""
  local right_padding=""

  for ((i=0; i<padding; i++)); do left_padding+=" "; done
  for ((i=0; i<width-padding-${#text}; i++)); do right_padding+=" "; done

  echo -e "${color}╔════════════════════════════════════════════╗${RESET}"
  echo -e "${color}║${left_padding}${text}${right_padding}║${RESET}"
  echo -e "${color}╚════════════════════════════════════════════╝${RESET}"
}

print_banner() {
  local title="$1"
  local color="$2"
  local line="════════════════════════════════════════"
  echo -e "${color}${line}${RESET}"
  echo -e "${color}${title}${RESET}"
  echo -e "${color}${line}${RESET}"
}

print_menu() {
  clear
  echo
  print_header "Deutsch-Lernprogramm" "$MAGENTA"
  echo
  echo -e "${CYAN}┌ Wähle einen Modus: ${RESET}"
  echo -e "${CYAN}├─────────────────────────────────────────────${RESET}"
  echo -e "${CYAN}│${RESET}"
  echo -e "${CYAN}│  ${GREEN}1${RESET}  Satz übersetzen"
  echo -e "${CYAN}│  ${GREEN}2${RESET}  Trennbare Verben lernen"
  echo -e "${CYAN}│  ${GREEN}3${RESET}  Untrennbare Verben lernen"
  echo -e "${CYAN}│  ${GREEN}4${RESET}  Beenden"
  echo -e "${CYAN}│${RESET}"
  echo -e "${CYAN}└─────────────────────────────────────────────${RESET}"
  echo
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

    clear
    print_header "Übersetzungsübung" "$BLUE"
    echo
    echo -e "${CYAN}┌ Befehle: ${RESET}"
    echo -e "${CYAN}├─────────────────────────────────────────────${RESET}"
    echo -e "${CYAN}│  ${GREEN}t${RESET}  Deutsche Übersetzung anzeigen"
    echo -e "${CYAN}│  ${GREEN}n${RESET}  Nächsten englischen Satz"
    echo -e "${CYAN}│  ${GREEN}m${RESET}  Hauptmenü"
    echo -e "${CYAN}│  ${GREEN}C${RESET}  Beenden (Strg+C)"
    echo -e "${CYAN}└─────────────────────────────────────────────${RESET}"
    echo
    echo -e "${YELLOW}┌─ Englisch ${RESET}"
    echo -e "${YELLOW}│${RESET}"
    printf "${YELLOW}│  🇬🇧  %s${RESET}\n" "$english"
    echo -e "${YELLOW}│${RESET}"
    echo -e "${YELLOW}└─────────────────────────────────────────────${RESET}"
    echo

    while true; do
      printf 'Befehl [t/n/m]: '
      IFS= read -rsn1 key
      printf '%s\n' "$key"

      case "$key" in
        t|T)
          echo
          echo -e "${GREEN}┌─ Deutsch ${RESET}"
          echo -e "${GREEN}│${RESET}"
          printf "${GREEN}│  🇩🇪  %s${RESET}\n" "$german"
          echo -e "${GREEN}│${RESET}"
          echo -e "${GREEN}└─────────────────────────────────────────────${RESET}"
          echo
          ;;
        n|N)
          break
          ;;
        m|M)
          return 0
          ;;
        *)
          echo -e "${RED}✗ Ungültige Eingabe. Nutze t, n oder m.${RESET}"
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

    clear
    print_header "Verbtraining: $title" "$YELLOW"
    echo
    echo -e "${CYAN}┌ Befehle: ${RESET}"
    echo -e "${CYAN}├─────────────────────────────────────────────${RESET}"
    echo -e "${CYAN}│  ${GREEN}b${RESET}  Bedeutung anzeigen"
    echo -e "${CYAN}│  ${GREEN}n${RESET}  Nächstes Verb"
    echo -e "${CYAN}│  ${GREEN}m${RESET}  Hauptmenü"
    echo -e "${CYAN}│  ${GREEN}e${RESET}  Beenden"
    echo -e "${CYAN}└─────────────────────────────────────────────${RESET}"
    echo
    echo -e "${GREEN}┌─ Verb ${RESET}"
    echo -e "${GREEN}│${RESET}"
    printf "${GREEN}│  🇩🇪  %s${RESET}\n" "$german"
    echo -e "${GREEN}│${RESET}"
    echo -e "${GREEN}└─────────────────────────────────────────────${RESET}"
    echo

    while true; do
      printf 'Befehl [b/n/m/e]: '
      IFS= read -rsn1 key
      printf '%s\n' "$key"

      case "$key" in
        b|B)
          echo
          echo -e "${CYAN}┌─ Bedeutung ${RESET}"
          echo -e "${CYAN}│  $english${RESET}"
          echo -e "${CYAN}└─────────────────────────────────────────────${RESET}"
          echo
          echo -e "${MAGENTA}┌─ Beispiel ${RESET}"
          echo -e "${MAGENTA}│  $example${RESET}"
          echo -e "${MAGENTA}└─────────────────────────────────────────────${RESET}"
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
          echo -e "${RED}✗ Ungültige Eingabe. Nutze b, n, m oder e.${RESET}"
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
      clear
      print_header "Auf Wiedersehen!" "$MAGENTA"
      echo
      exit 0
      ;;
    *)
      echo -e "${RED}Ungültige Auswahl. Bitte wähle 1, 2, 3 oder 4.${RESET}"
      echo
      ;;
  esac
done
