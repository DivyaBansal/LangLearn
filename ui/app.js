const modes = {
  sentences: {
    name: "Sätze übersetzen",
    title: "Was heißt das auf Deutsch?",
    source: "../data/sentences.tsv",
    promptLabel: "Englisch",
    answerLabel: "Deutsch",
  },
  separable: {
    name: "Trennbare Verben",
    title: "Was bedeutet dieses Verb?",
    source: "../data/separable-verbs.tsv",
    promptLabel: "Deutsch",
    answerLabel: "Bedeutung",
  },
  inseparable: {
    name: "Untrennbare Verben",
    title: "Was bedeutet dieses Verb?",
    source: "../data/inseparable-verbs.tsv",
    promptLabel: "Deutsch",
    answerLabel: "Bedeutung",
  },
};

const elements = {
  welcome: document.querySelector("#welcome"),
  practice: document.querySelector("#practice"),
  changeMode: document.querySelector("#change-mode"),
  modeName: document.querySelector("#mode-name"),
  title: document.querySelector("#practice-title"),
  promptLabel: document.querySelector("#prompt-label"),
  answerLabel: document.querySelector("#answer-label"),
  prompt: document.querySelector("#prompt"),
  answer: document.querySelector("#answer"),
  example: document.querySelector("#example"),
  answerPanel: document.querySelector("#answer-panel"),
  reveal: document.querySelector("#reveal"),
  next: document.querySelector("#next"),
  count: document.querySelector("#seen-count"),
  error: document.querySelector("#error"),
};

let activeMode = null;
let cards = [];
let currentIndex = -1;
let seen = 0;

function parseTsv(text) {
  return text
    .split(/\r?\n/)
    .filter((line) => line.trim() && !line.startsWith("#"))
    .map((line) => line.split("\t"))
    .filter((columns) => columns.length >= 2)
    .map(([prompt, answer, example = ""]) => ({ prompt, answer, example }));
}

function showError(message) {
  elements.error.textContent = message;
  elements.error.hidden = false;
}

function showCard() {
  if (!cards.length) return;

  let nextIndex = Math.floor(Math.random() * cards.length);
  if (cards.length > 1 && nextIndex === currentIndex) {
    nextIndex = (nextIndex + 1) % cards.length;
  }
  currentIndex = nextIndex;
  seen += 1;

  const card = cards[currentIndex];
  elements.prompt.textContent = card.prompt;
  elements.answer.textContent = card.answer;
  elements.example.textContent = card.example;
  elements.example.hidden = !card.example;
  elements.answerPanel.hidden = true;
  elements.reveal.hidden = false;
  elements.count.textContent = seen;
  elements.reveal.focus();
}

function revealAnswer() {
  if (!activeMode || !elements.answerPanel.hidden) return;
  elements.answerPanel.hidden = false;
  elements.reveal.hidden = true;
  elements.next.focus();
}

async function startMode(modeKey) {
  const mode = modes[modeKey];
  if (!mode) return;

  activeMode = modeKey;
  seen = 0;
  currentIndex = -1;
  elements.error.hidden = true;
  elements.modeName.textContent = mode.name;
  elements.title.textContent = mode.title;
  elements.promptLabel.textContent = mode.promptLabel;
  elements.answerLabel.textContent = mode.answerLabel;

  try {
    const response = await fetch(mode.source);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    cards = parseTsv(await response.text());
    if (!cards.length) throw new Error("no usable cards");

    elements.welcome.hidden = true;
    elements.practice.hidden = false;
    elements.changeMode.hidden = false;
    showCard();
  } catch (error) {
    activeMode = null;
    showError("Die Übungsdaten konnten nicht geladen werden. Starte die App mit ./start-ui.sh und lade die Seite erneut.");
    elements.welcome.hidden = true;
    elements.practice.hidden = false;
    elements.changeMode.hidden = false;
    console.error(error);
  }
}

function showMenu() {
  activeMode = null;
  cards = [];
  elements.practice.hidden = true;
  elements.changeMode.hidden = true;
  elements.welcome.hidden = false;
  document.querySelector("[data-mode]").focus();
}

document.querySelectorAll("[data-mode]").forEach((button) => {
  button.addEventListener("click", () => startMode(button.dataset.mode));
});

elements.reveal.addEventListener("click", revealAnswer);
elements.next.addEventListener("click", showCard);
elements.changeMode.addEventListener("click", showMenu);

document.addEventListener("keydown", (event) => {
  if (!activeMode || event.ctrlKey || event.metaKey || event.altKey) return;
  if (event.key === " " && elements.answerPanel.hidden) {
    event.preventDefault();
    revealAnswer();
  } else if (event.key.toLowerCase() === "n") {
    showCard();
  } else if (event.key === "Escape") {
    showMenu();
  }
});
