"use strict";

// Front-end for german-terminal-practice.sh. Mirrors the terminal modes and
// keys: 1-3 pick a mode in the menu, t/b reveal, n goes to the next item and
// m returns to the menu.

const $ = (id) => document.getElementById(id);

const state = {
  data: null,
  view: "menu",
  verbMode: null,
  verbIndex: -1,
};

function pickRandom(items) {
  return items[Math.floor(Math.random() * items.length)];
}

function showMessage(text) {
  $("message").textContent = text || "";
}

function showView(view) {
  state.view = view;
  for (const id of ["menu", "sentence", "verb"]) {
    $(id).hidden = id !== view;
  }
  $("nav").hidden = view === "menu";
  showMessage("");
}

function goToMenu() {
  showView("menu");
}

function startSentence() {
  if (!state.data.sentences.length) {
    showMessage("Keine Sätze gefunden.");
    return;
  }
  showView("sentence");
  nextSentence();
}

function nextSentence() {
  const pair = pickRandom(state.data.sentences);
  $("sentence-en").textContent = pair.english;
  $("sentence-de").textContent = pair.german;
  $("sentence-de").hidden = true;
  $("sentence").querySelector('[data-action="toggle-translation"]').textContent =
    "Übersetzung anzeigen";
}

function revealTranslation() {
  $("sentence-de").hidden = false;
  $("sentence").querySelector('[data-action="toggle-translation"]').textContent =
    "Übersetzung verbergen";
}

function startVerbs(mode) {
  const bank = state.data[mode];
  if (!bank.length) {
    showMessage("Keine Verben gefunden.");
    return;
  }
  state.verbMode = mode;
  showView("verb");
  $("verb-title").textContent =
    mode === "separable" ? "Verbtraining: Trennbare Präfixe" : "Verbtraining: Untrennbare Präfixe";
  nextVerb();
}

function nextVerb() {
  const bank = state.data[state.verbMode];
  let index = Math.floor(Math.random() * bank.length);
  // Avoid showing the same verb twice in a row when there is a choice.
  if (bank.length > 1 && index === state.verbIndex) {
    index = (index + 1) % bank.length;
  }
  state.verbIndex = index;
  const verb = bank[index];

  $("verb-de").textContent = verb.german;
  $("verb-en").textContent = verb.english;
  $("verb-example").textContent = verb.example ? `Beispiel: ${verb.example}` : "";
  $("verb-answer").hidden = true;
  $("verb").querySelector('[data-action="toggle-meaning"]').textContent = "Bedeutung anzeigen";
}

function revealMeaning() {
  $("verb-answer").hidden = false;
  $("verb").querySelector('[data-action="toggle-meaning"]').textContent = "Bedeutung verbergen";
}

function toggleVerbMeaning() {
  if ($("verb-answer").hidden) {
    revealMeaning();
  } else {
    $("verb-answer").hidden = true;
    $("verb").querySelector('[data-action="toggle-meaning"]').textContent = "Bedeutung anzeigen";
  }
}

function toggleSentenceTranslation() {
  if ($("sentence-de").hidden) {
    revealTranslation();
  } else {
    $("sentence-de").hidden = true;
    $("sentence").querySelector('[data-action="toggle-translation"]').textContent =
      "Übersetzung anzeigen";
  }
}

function handleMenuChoice(choice) {
  if (choice === "sentence") startSentence();
  else if (choice === "separable" || choice === "inseparable") startVerbs(choice);
}

const actions = {
  menu: goToMenu,
  "toggle-translation": toggleSentenceTranslation,
  "next-sentence": nextSentence,
  "toggle-meaning": toggleVerbMeaning,
  "next-verb": nextVerb,
};

const menuKeys = { 1: "sentence", 2: "separable", 3: "inseparable" };

document.addEventListener("click", (event) => {
  const button = event.target.closest("button");
  if (!button) return;
  if (button.dataset.mode) {
    handleMenuChoice(button.dataset.mode);
  } else if (button.dataset.action) {
    actions[button.dataset.action]();
  }
});

document.addEventListener("keydown", (event) => {
  if (event.ctrlKey || event.metaKey || event.altKey || !state.data) return;

  const key = event.key.toLowerCase();
  // Enter and Space on a focused button should only activate that button.
  if (event.target.tagName === "BUTTON" && (key === "enter" || key === " ")) return;

  if (state.view === "menu") {
    if (menuKeys[key]) handleMenuChoice(menuKeys[key]);
    return;
  }

  if (key === "m") {
    goToMenu();
    return;
  }

  if (key === "n") {
    if (state.view === "sentence") nextSentence();
    else if (state.view === "verb") nextVerb();
    return;
  }

  if (state.view === "sentence" && key === "t") {
    revealTranslation();
  } else if (state.view === "verb" && key === "b") {
    revealMeaning();
  }
});

async function load() {
  try {
    const response = await fetch("/api/data", { cache: "no-store" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    state.data = await response.json();
    $("status").textContent = `${state.data.sentences.length} Sätze · ${state.data.separable.length} trennbare · ${state.data.inseparable.length} untrennbare Verben`;
    $("menu").hidden = false;
  } catch (error) {
    $("status").textContent = `Daten konnten nicht geladen werden: ${error.message}`;
  }
}

load();
