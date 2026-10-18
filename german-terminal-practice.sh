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
  print_banner "Deutsch-Lernprogramm" "$MAGENTA"
  echo -e "${CYAN}Wähle einen Modus:${RESET}"
  echo
  echo -e "${GREEN}1.${RESET} Satz übersetzen"
  echo -e "${GREEN}2.${RESET} Trennbare Verben lernen"
  echo -e "${GREEN}3.${RESET} Untrennbare Verben lernen"
  echo -e "${GREEN}4.${RESET} Beenden"
  echo
}

discard_pending_input() {
  local pending
  IFS= read -r -t 0.01 pending || true
}

edit_tsv_entry() {
  local file="$1"
  local entry="$2"
  local question_label="$3"
  local answer_label="$4"
  local question answer extra choice replacement column tmp updated line new_line

  IFS=$'\t' read -r question answer extra <<< "$entry"
  echo
  echo "Was möchtest du bearbeiten?"
  echo "q = Frage ($question_label): $question"
  echo "a = Antwort ($answer_label): $answer"
  printf 'Auswahl [q/a]: '
  IFS= read -r choice

  case "$choice" in
    q|Q|1)
      column=1
      printf 'Neue Frage: '
      ;;
    a|A|2)
      column=2
      printf 'Neue Antwort: '
      ;;
    *)
      echo -e "${RED}Ungültige Auswahl. Der Eintrag wurde nicht geändert.${RESET}"
      return 0
      ;;
  esac

  IFS= read -r replacement
  if [[ -z "$replacement" || "$replacement" == *$'\t'* ]]; then
    echo -e "${RED}Die Eingabe darf nicht leer sein und kein TAB enthalten.${RESET}"
    return 0
  fi

  tmp="$(mktemp "${file}.tmp.XXXXXX")" || {
    echo "Konnte keine temporäre Datei für $file erstellen."
    return 1
  }
  updated=false
  while IFS= read -r line || [[ -n "$line" ]]; do
    if [[ "$updated" == false && "$line" == "$entry" ]]; then
      if [[ "$column" == 1 ]]; then
        new_line="${replacement}"$'\t'"${answer}"
      else
        new_line="${question}"$'\t'"${replacement}"
      fi
      [[ -n "$extra" ]] && new_line+=$'\t'"${extra}"
      printf '%s\n' "$new_line" >> "$tmp"
      updated=true
    else
      printf '%s\n' "$line" >> "$tmp"
    fi
  done < "$file"

  if [[ "$updated" != true ]]; then
    rm -f -- "$tmp"
    echo "Der ausgewählte Eintrag wurde nicht gefunden."
    return 1
  fi

  mv -- "$tmp" "$file"
  echo -e "${GREEN}Eintrag gespeichert.${RESET}"
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
    print_banner "Übersetzungsübung" "$BLUE"
    echo -e "${CYAN}Drücke t = deutsche Übersetzung anzeigen${RESET}"
    echo -e "${CYAN}Drücke n = nächsten englischen Satz${RESET}"
    echo -e "${CYAN}Drücke e = Frage oder Antwort bearbeiten${RESET}"
    echo -e "${CYAN}Drücke m = Hauptmenü${RESET}"
    echo -e "${CYAN}Drücke Strg+C = beenden${RESET}"
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
        e|E)
          discard_pending_input
          edit_tsv_entry "$CORPUS" "$line" "englischer Satz" "deutsche Übersetzung"
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

    clear
    print_banner "Verbtraining: $title" "$YELLOW"
    echo -e "${CYAN}Drücke b = Bedeutung anzeigen${RESET}"
    echo -e "${CYAN}Drücke n = nächstes Verb${RESET}"
    echo -e "${CYAN}Drücke e = Frage oder Antwort bearbeiten${RESET}"
    echo -e "${CYAN}Drücke m = Hauptmenü${RESET}"
    echo -e "${CYAN}Drücke x = beenden${RESET}"
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
          discard_pending_input
          edit_tsv_entry "$([[ "$mode" == "separable" ]] && echo "$SEPARABLE_VERB_FILE" || echo "$INSEPARABLE_VERB_FILE")" \
            "$entry" "deutsches Verb" "englische Bedeutung"
          ;;
        x|X)
          exit 0
          ;;
        *)
          echo -e "${RED}Verwende b für die Bedeutung, n für das nächste Verb, e zum Bearbeiten, m für das Hauptmenü oder x zum Beenden.${RESET}"
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
