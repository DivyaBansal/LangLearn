const modes = {
  sentences: {
    file: "data/sentences.tsv",
    label: "Sentence practice",
    promptLabel: "Translate into German",
    answerLabel: "Auf Deutsch",
  },
  separable: {
    file: "data/separable-verbs.tsv",
    label: "Separable verbs",
    promptLabel: "What does this verb mean?",
    answerLabel: "Meaning",
  },
  inseparable: {
    file: "data/inseparable-verbs.tsv",
    label: "Inseparable verbs",
    promptLabel: "What does this verb mean?",
    answerLabel: "Meaning",
  },
};

const state = { mode: null, items: [], currentIndex: -1, lastIndex: -1 };
const elements = {
  home: document.querySelector("#home-view"),
  practice: document.querySelector("#practice-view"),
  error: document.querySelector("#error-view"),
  modeLabel: document.querySelector("#mode-label"),
  promptLabel: document.querySelector("#prompt-label"),
  prompt: document.querySelector("#prompt"),
  itemCount: document.querySelector("#item-count"),
  answerPanel: document.querySelector("#answer-panel"),
  answerLabel: document.querySelector("#answer-label"),
  answer: document.querySelector("#answer"),
  example: document.querySelector("#example"),
  reveal: document.querySelector("#reveal-button"),
  errorMessage: document.querySelector("#error-message"),
};

function parseTsv(text, mode) {
  return text.split(/\r?\n/).filter(line => line.trim() && !line.startsWith("#")).map(line => {
    const fields = line.split("\t");
    if (mode === "sentences") return { prompt: fields[0], answer: fields[1] };
    const offset = fields.length >= 4 && /^\d+$/.test(fields[0]) ? 1 : 0;
    return { prompt: fields[offset], answer: fields[offset + 1], example: fields[offset + 2] };
  }).filter(item => item.prompt && item.answer);
}

function showView(name) {
  [elements.home, elements.practice, elements.error].forEach(view => { view.hidden = true; });
  elements[name].hidden = false;
  document.querySelector("main").focus({ preventScroll: true });
}

async function startMode(mode) {
  const config = modes[mode];
  try {
    const response = await fetch(config.file);
    if (!response.ok) throw new Error(`The server returned ${response.status}.`);
    state.items = parseTsv(await response.text(), mode);
    if (!state.items.length) throw new Error("The data file contained no usable entries.");
    state.mode = mode;
    state.currentIndex = -1;
    state.lastIndex = -1;
    elements.modeLabel.textContent = config.label;
    elements.promptLabel.textContent = config.promptLabel;
    elements.answerLabel.textContent = config.answerLabel;
    showView("practice");
    nextItem();
  } catch (error) {
    elements.errorMessage.textContent = `${error.message} Start the app with a local web server (for example, “python3 -m http.server”) and try again.`;
    showView("error");
  }
}

function nextItem() {
  if (!state.items.length) return;
  let index;
  do index = Math.floor(Math.random() * state.items.length);
  while (state.items.length > 1 && index === state.lastIndex);
  state.currentIndex = index;
  state.lastIndex = index;
  const item = state.items[index];
  elements.prompt.textContent = item.prompt;
  elements.answer.textContent = item.answer;
  elements.example.textContent = item.example ? `Example: ${item.example}` : "";
  elements.example.hidden = !item.example;
  elements.itemCount.textContent = `${state.items.length.toLocaleString()} in this set`;
  elements.answerPanel.hidden = true;
  elements.reveal.hidden = false;
}

function revealAnswer() {
  if (elements.practice.hidden || !elements.answerPanel.hidden) return;
  elements.answerPanel.hidden = false;
  elements.reveal.hidden = true;
}

function goHome() {
  state.mode = null;
  showView("home");
}

document.addEventListener("click", event => {
  const modeButton = event.target.closest("[data-mode]");
  const actionButton = event.target.closest("[data-action]");
  if (modeButton) startMode(modeButton.dataset.mode);
  if (!actionButton) return;
  if (actionButton.dataset.action === "home") goHome();
  if (actionButton.dataset.action === "reveal") revealAnswer();
  if (actionButton.dataset.action === "next") nextItem();
});

document.addEventListener("keydown", event => {
  if (!elements.home.hidden && ["1", "2", "3"].includes(event.key)) {
    startMode(["sentences", "separable", "inseparable"][Number(event.key) - 1]);
  } else if (!elements.practice.hidden && event.key === " ") {
    event.preventDefault();
    revealAnswer();
  } else if (!elements.practice.hidden && (event.key === "n" || event.key === "ArrowRight")) {
    nextItem();
  } else if (!elements.practice.hidden && event.key === "Escape") {
    goHome();
  }
});
