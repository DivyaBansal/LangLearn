# German practice

Practice German translations and verbs in the terminal or in a browser.

## Terminal

```sh
./german-terminal-practice.sh
```

The original terminal workflow remains dependency-free.

## Browser UI

```sh
./start-ui.sh
```

Then open <http://localhost:8000/ui/>. Set `GERMAN_PRACTICE_UI_PORT` to use a different port.
The browser UI reads the same TSV files in `data/` as the terminal app. Use Space to reveal an
answer, `N` for the next card, and Escape to return to the mode menu.
