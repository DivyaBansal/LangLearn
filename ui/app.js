const DATA_PATHS = {
  sentence: '../data/sentences.tsv',
  separable: '../data/separable-verbs.tsv',
  inseparable: '../data/inseparable-verbs.tsv',
};

const MODE_TITLES = {
  sentence: 'Übersetzungsübung',
  separable: 'Verbtraining: Trennbare Präfixe',
  inseparable: 'Verbtraining: Untrennbare Präfixe',
};

const menu = document.getElementById('menu');
const practice = document.getElementById('practice');
const practiceTitle = document.getElementById('practiceTitle');
const promptText = document.getElementById('promptText');
const revealBox = document.getElementById('revealBox');
const revealText = document.getElementById('revealText');
const exampleText = document.getElementById('exampleText');
const revealBtn = document.getElementById('revealBtn');
const nextBtn = document.getElementById('nextBtn');
const backBtn = document.getElementById('backBtn');
const statusText = document.getElementById('statusText');

const cache = {};
let currentMode = null;
let currentItem = null;

function parseTsv(raw) {
  return raw
    .split('\n')
    .map((line) => line.replace(/\r$/, ''))
    .filter((line) => line.trim() !== '' && !line.startsWith('#'));
}

function parseSentenceLine(line) {
  const tabIndex = line.indexOf('\t');
  if (tabIndex === -1) return null;
  const english = line.slice(0, tabIndex);
  const german = line.slice(tabIndex + 1);
  if (!english || !german) return null;
  return { prompt: english, answer: german, example: '' };
}

function parseVerbLine(line) {
  let fields = line.split('\t');
  // Some verb files have a leading numeric index column; drop it if present.
  if (fields.length === 4 && /^\d+$/.test(fields[0])) {
    fields = fields.slice(1);
  }
  const [german, english, example] = fields;
  if (!german || !english) return null;
  return { prompt: german, answer: english, example: example || '' };
}

async function loadMode(mode) {
  if (cache[mode]) return cache[mode];
  const res = await fetch(DATA_PATHS[mode]);
  if (!res.ok) {
    throw new Error(`Konnte Daten nicht laden: ${DATA_PATHS[mode]} (${res.status})`);
  }
  const raw = await res.text();
  const lines = parseTsv(raw);
  const parser = mode === 'sentence' ? parseSentenceLine : parseVerbLine;
  const items = lines.map(parser).filter(Boolean);
  cache[mode] = items;
  return items;
}

function pickRandom(items) {
  return items[Math.floor(Math.random() * items.length)];
}

function showNextItem() {
  const items = cache[currentMode];
  if (!items || items.length === 0) {
    statusText.textContent = 'Keine Daten für diesen Modus gefunden.';
    return;
  }
  currentItem = pickRandom(items);
  promptText.textContent = currentMode === 'sentence' ? `🇬🇧 ${currentItem.prompt}` : `🇩🇪 ${currentItem.prompt}`;
  revealBox.hidden = true;
  statusText.textContent = '';
}

function showReveal() {
  if (!currentItem) return;
  revealText.textContent = currentMode === 'sentence'
    ? `🇩🇪 ${currentItem.answer}`
    : `Bedeutung: ${currentItem.answer}`;
  exampleText.textContent = currentItem.example ? `Beispiel: ${currentItem.example}` : '';
  revealBox.hidden = false;
}

async function startMode(mode) {
  statusText.textContent = '';
  currentMode = mode;
  practiceTitle.textContent = MODE_TITLES[mode];
  revealBtn.textContent = mode === 'sentence' ? 'Übersetzung anzeigen' : 'Bedeutung anzeigen';
  menu.hidden = true;
  practice.hidden = false;

  try {
    await loadMode(mode);
    showNextItem();
  } catch (err) {
    statusText.textContent = err.message;
  }
}

function returnToMenu() {
  practice.hidden = true;
  menu.hidden = false;
  currentMode = null;
  currentItem = null;
}

menu.addEventListener('click', (event) => {
  const btn = event.target.closest('.menu-btn');
  if (!btn) return;
  startMode(btn.dataset.mode);
});

revealBtn.addEventListener('click', showReveal);
nextBtn.addEventListener('click', showNextItem);
backBtn.addEventListener('click', returnToMenu);
