// Data storage (will be populated from TSV files)
let sentences = [];
let separableVerbs = [];
let inseparableVerbs = [];

// State
let currentMode = 'menu';
let currentItem = null;
let showTranslation = false;

// DOM elements
const app = document.getElementById('app');

// Initialize
async function init() {
  try {
    await loadData();
    render();
  } catch (error) {
    console.error('Failed to load data:', error);
    app.innerHTML = '<div class="app-container"><div class="banner"><h1 class="banner-title">Error loading data</h1></div></div>';
  }
}

// Load data from TSV files
async function loadData() {
  const loadTSV = async (url) => {
    const response = await fetch(url);
    const text = await response.text();
    return text.split('\n').filter(line => line.trim() && !line.startsWith('#'));
  };

  [sentences, separableVerbs, inseparableVerbs] = await Promise.all([
    loadTSV('data/sentences.tsv'),
    loadTSV('data/separable-verbs.tsv'),
    loadTSV('data/inseparable-verbs.tsv')
  ]);
}

// Random item picker
function pickRandom(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

// Parse TSV line
function parseLine(line, separator = '\t') {
  const parts = line.split(separator);
  return parts.map(p => p.trim());
}

// Render main menu
function renderMenu() {
  app.innerHTML = `
    <div class="app-container">
      <div class="banner" style="background: var(--color-magenta);">
        <h1 class="banner-title">Deutsch-Lernprogramm</h1>
      </div>
      <h2 class="section-title" style="color: var(--color-cyan);">Wähle einen Modus:</h2>
      <div class="menu">
        <button class="menu-btn" onclick="enterMode('translate')"><span class="number">1.</span>Satz übersetzen</button>
        <button class="menu-btn" onclick="enterMode('separable')"><span class="number">2.</span>Trennbare Verben lernen</button>
        <button class="menu-btn" onclick="enterMode('inseparable')"><span class="number">3.</span>Untrennbare Verben lernen</button>
        <button class="menu-btn" style="background: var(--color-red);" onclick="exitApp()"><span class="number">4.</span>Beenden</button>
      </div>
    </div>
  `;
}

// Render sentence translation mode
function renderSentenceMode() {
  const sentence = currentItem;
  const [english, german] = parseLine(sentence);

  app.innerHTML = `
    <div class="app-container">
      <button class="back-btn" onclick="backToMenu()">← Zurück zum Menü</button>
      <div class="banner" style="background: var(--color-blue);">
        <h1 class="banner-title">Übersetzungsübung</h1>
      </div>
      <div class="card">
        <div class="text-de">🇬🇧 ${english}</div>
        ${showTranslation ? `<div class="text-en">🇩🇪 ${german}</div>` : '<p style="color: var(--color-yellow);">Drücke "Zeigen" um die Übersetzung zu sehen</p>'}
      </div>
      <div class="controls">
        <button class="control-btn primary" onclick="toggleTranslation()">Zeigen (t)</button>
        <button class="control-btn" onclick="nextSentence()">Nächster Satz (n)</button>
      </div>
      <p style="text-align: center; margin-top: 15px; color: var(--color-cyan);">
        Drücke m für Hauptmenü oder Strg+W um zu schließen
      </p>
    </div>
  `;
}

// Render verb practice mode
function renderVerbMode(mode) {
  const verb = currentItem;
  const [german, english, example] = parseLine(verb);
  const title = mode === 'separable' ? 'Trennbare Präfixe' : 'Untrennbare Präfixe';
  const color = mode === 'separable' ? 'var(--color-yellow)' : 'var(--color-cyan)';

  app.innerHTML = `
    <div class="app-container">
      <button class="back-btn" onclick="backToMenu()">← Zurück zum Menü</button>
      <div class="banner" style="background: ${color};">
        <h1 class="banner-title">Verbtraining: ${title}</h1>
      </div>
      <div class="card">
        <div class="text-de">🇩🇪 ${german}</div>
        ${showTranslation ? `
          <div class="text-en">Bedeutung: ${english}</div>
          <div class="example">Beispiel: ${example}</div>
        ` : '<p style="color: var(--color-yellow);">Drücke "Bedeutung" um die Erklärung zu sehen</p>'}
      </div>
      <div class="controls">
        <button class="control-btn primary" onclick="toggleTranslation()">Bedeutung (b)</button>
        <button class="control-btn" onclick="nextVerb()">Nächstes Verb (n)</button>
      </div>
      <p style="text-align: center; margin-top: 15px; color: var(--color-cyan);">
        Drücke m für Hauptmenü oder e zum Beenden
      </p>
    </div>
  `;
}

// Mode transitions
function enterMode(mode) {
  currentMode = mode;
  showTranslation = false;
  
  if (mode === 'translate') {
    nextSentence();
  } else {
    nextVerb();
  }
}

function backToMenu() {
  currentMode = 'menu';
  showTranslation = false;
  renderMenu();
}

function exitApp() {
  document.body.innerHTML = `
    <div style="text-align: center; padding: 50px;">
      <h1 style="color: var(--color-magenta);">Auf Wiedersehen!</h1>
      <p style="color: var(--color-text);">Danke für das Lernen 🇩🇪</p>
    </div>
  `;
}

function nextSentence() {
  currentItem = pickRandom(sentences);
  showTranslation = false;
  renderSentenceMode();
}

function nextVerb() {
  currentItem = pickRandom(currentMode === 'separable' ? separableVerbs : inseparableVerbs);
  showTranslation = false;
  renderVerbMode(currentMode);
}

function toggleTranslation() {
  showTranslation = true;
  if (currentMode === 'translate') {
    renderSentenceMode();
  } else {
    renderVerbMode(currentMode);
  }
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
  if (currentMode === 'menu') {
    if (e.key === '1') enterMode('translate');
    else if (e.key === '2') enterMode('separable');
    else if (e.key === '3') enterMode('inseparable');
    else if (e.key === '4' || e.key === 'q') exitApp();
  } else if (currentMode === 'translate') {
    if (e.key === 't' || e.key === 'T') toggleTranslation();
    else if (e.key === 'n' || e.key === 'N') nextSentence();
    else if (e.key === 'm' || e.key === 'M') backToMenu();
    else if (e.key === 'w' && e.ctrlKey) exitApp();
  } else if (currentMode === 'separable' || currentMode === 'inseparable') {
    if (e.key === 'b' || e.key === 'B') toggleTranslation();
    else if (e.key === 'n' || e.key === 'N') nextVerb();
    else if (e.key === 'm' || e.key === 'M') backToMenu();
    else if (e.key === 'e' || e.key === 'E') exitApp();
  }
});

// Start the app
init();
