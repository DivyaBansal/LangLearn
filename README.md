# LangLearn - German Language Practice

A terminal and web-based application for practicing German language skills.

## Features

- **Satz übersetzen** (Sentence Translation): Practice translating English sentences to German
- **Trennbare Verben** (Separable Verbs): Learn German separable verb prefixes
- **Untrennbare Verben** (Inseparable Verbs): Learn German inseparable verb prefixes

## Usage

### Terminal Version

```bash
./german-terminal-practice.sh
```

### Web Version

```bash
python3 server.py
# Then open http://localhost:8080 in your browser
```

## Keyboard Shortcuts (Web Version)

- `ESC` - Return to main menu
- `t` - Show/hide translation (sentence mode)
- `b` - Show/hide meaning (verb mode)
- `n` - Next item
- `m` - Return to menu
- Arrow keys - Navigate menu options

## Data Files

Data files are located in the `data/` directory:
- `sentences.tsv` - Bilingual sentences for translation practice
- `separable-verbs.tsv` - Separable verbs with examples
- `inseparable-verbs.tsv` - Inseparable verbs with examples

## Customization

You can customize the data directory using environment variables:

```bash
export GERMAN_PRACTICE_DATA_DIR=/path/to/data
./german-terminal-practice.sh
```
