# Wortweise

A small German practice app with both terminal and browser interfaces. Both use the same TSV data in `data/`.

## Browser UI

From the repository root, start any static file server:

```bash
python3 -m http.server 8000
```

Then open [http://localhost:8000](http://localhost:8000). Choose sentence translation, separable verbs, or inseparable verbs. The interface also supports keyboard navigation: `1`–`3` chooses a mode, `Space` reveals an answer, `N` advances, and `Escape` returns home.

## Terminal UI

The original terminal experience is unchanged:

```bash
./german-terminal-practice.sh
```

Run its test with:

```bash
bash tests/test_german_practice.sh
```
