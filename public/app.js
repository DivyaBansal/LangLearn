// German Learning App - JavaScript

// Data storage
let sentences = [];
let separableVerbs = [];
let inseparableVerbs = [];

// Current state
let currentMode = null;
let currentIndex = 0;

// DOM Elements
const views = {
  menu: document.getElementById('menu-view'),
  sentences: document.getElementById('sentences-view'),
  verb: document.getElementById('verb-view')
};

const elements = {
  sentenceEnglish: document.getElementById('sentence-english'),
  sentenceGerman: document.getElementById('sentence-german'),
  translationContainer: document.getElementById('translation-container'),
  translationText: document.querySelector('.translation-text'),
  showTranslationBtn: document.getElementById('show-translation-btn'),
  nextSentenceBtn: document.getElementById('next-sentence-btn'),

  verbGerman: document.getElementById('verb-german'),
  verbMeaning: document.getElementById('verb-meaning'),
  verbExample: document.getElementById('verb-example'),
  meaningContainer: document.getElementById('meaning-container'),
  meaningText: document.querySelector('.meaning-text'),
  showMeaningBtn: document.getElementById('show-meaning-btn'),
  nextVerbBtn: document.getElementById('next-verb-btn'),

  verbTitle: document.getElementById('verb-title')
};

// Load TSV file
async function loadTSV(url) {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Failed to load ${url}: ${response.status}`);
    }
    const text = await response.text();
    return parseTSV(text);
  } catch (error) {
    console.error(`Error loading ${url}:`, error);
    return [];
  }
}

// Parse TSV content
function parseTSV(text) {
  const lines = text.trim().split('\n');
  return lines
    .map(line => line.trim())
    .filter(line => line && !line.startsWith('#'))
    .map(line => line.split('\t'));
}

// Initialize data
async function initData() {
  try {
    const [sentencesData, separableData, inseparableData] = await Promise.all([
      loadTSV('data/sentences.tsv'),
      loadTSV('data/separable-verbs.tsv'),
      loadTSV('data/inseparable-verbs.tsv')
    ]);

    // Parse sentences: [index, english, german]
    sentences = sentencesData.filter(row => row.length >= 3)
      .map(row => ({
        english: row[1],
        german: row[2]
      }));

    // Parse separable verbs: [german, english, example]
    separableVerbs = separableData.filter(row => row.length >= 3)
      .map(row => ({
        german: row[0],
        english: row[1],
        example: row[2]
      }));

    // Parse inseparable verbs: [num, german, english, example]
    inseparableVerbs = inseparableData.filter(row => row.length >= 4)
      .map(row => ({
        german: row[2],
        english: row[3],
        example: row[4] || ''
      }));

    console.log('Data loaded:', {
      sentences: sentences.length,
      separableVerbs: separableVerbs.length,
      inseparableVerbs: inseparableVerbs.length
    });

    // Pick random starting items
    pickRandomSentence();
    pickRandomVerb();

  } catch (error) {
    console.error('Failed to initialize data:', error);
    showError('Failed to load data. Please make sure the data files are accessible.');
  }
}

// Show error message
function showError(message) {
  alert(message);
}

// ===== Sentence Mode =====

function pickRandomSentence() {
  if (sentences.length === 0) return;
  currentIndex = Math.floor(Math.random() * sentences.length);
  const sentence = sentences[currentIndex];

  elements.sentenceEnglish.textContent = sentence.english;
  elements.translationText.textContent = sentence.german;
  elements.translationContainer.classList.add('hidden');
  elements.showTranslationBtn.textContent = '🇩🇪 Translation anzeigen';
}

function showNextSentence() {
  if (sentences.length === 0) return;

  // Hide translation first
  elements.translationContainer.classList.add('hidden');
  elements.showTranslationBtn.textContent = '🇩🇪 Translation anzeigen';

  // Pick new random sentence
  do {
    currentIndex = Math.floor(Math.random() * sentences.length);
  } while (sentences.length > 1 && currentIndex === findCurrentSentenceIndex());

  const sentence = sentences[currentIndex];
  elements.sentenceEnglish.textContent = sentence.english;
  elements.translationText.textContent = sentence.german;
}

function findCurrentSentenceIndex() {
  return sentences.findIndex(s => s.english === elements.sentenceEnglish.textContent);
}

function toggleSentenceTranslation() {
  const isHidden = elements.translationContainer.classList.contains('hidden');
  if (isHidden) {
    elements.translationContainer.classList.remove('hidden');
    elements.showTranslationBtn.textContent = '🔒 Übersetzung ausblenden';
  } else {
    elements.translationContainer.classList.add('hidden');
    elements.showTranslationBtn.textContent = '🇩🇪 Translation anzeigen';
  }
}

// ===== Verb Mode =====

function pickRandomVerb() {
  const verbs = currentMode === 'separable' ? separableVerbs : inseparableVerbs;
  if (verbs.length === 0) return;

  currentIndex = Math.floor(Math.random() * verbs.length);
  const verb = verbs[currentIndex];

  elements.verbGerman.textContent = verb.german;
  elements.meaningText.textContent = verb.english;
  elements.verbExample.textContent = verb.example || '';
  elements.meaningContainer.classList.add('hidden');
  elements.showMeaningBtn.textContent = '📖 Bedeutung anzeigen';
}

function showNextVerb() {
  const verbs = currentMode === 'separable' ? separableVerbs : inseparableVerbs;
  if (verbs.length === 0) return;

  // Hide meaning first
  elements.meaningContainer.classList.add('hidden');
  elements.showMeaningBtn.textContent = '📖 Bedeutung anzeigen';

  // Pick new random verb
  do {
    currentIndex = Math.floor(Math.random() * verbs.length);
  } while (verbs.length > 1 && currentIndex === verbs.findIndex(v => v.german === elements.verbGerman.textContent));

  const verb = verbs[currentIndex];
  elements.verbGerman.textContent = verb.german;
  elements.meaningText.textContent = verb.english;
  elements.verbExample.textContent = verb.example || '';
}

function toggleVerbMeaning() {
  const isHidden = elements.meaningContainer.classList.contains('hidden');
  if (isHidden) {
    elements.meaningContainer.classList.remove('hidden');
    elements.showMeaningBtn.textContent = '🔒 Ausblenden';
  } else {
    elements.meaningContainer.classList.add('hidden');
    elements.showMeaningBtn.textContent = '📖 Bedeutung anzeigen';
  }
}

// ===== Navigation =====

function switchView(viewName) {
  // Hide all views
  Object.values(views).forEach(view => view.classList.remove('active'));

  // Show selected view
  if (viewName === 'menu') {
    views.menu.classList.add('active');
    currentMode = null;
  } else if (viewName === 'sentences') {
    views.sentences.classList.add('active');
    currentMode = 'sentences';
    pickRandomSentence();
  } else if (viewName === 'verb') {
    views.verb.classList.add('active');
    pickRandomVerb();
  }

  // Focus management
  document.activeElement.blur();
}

function setupEventListeners() {
  // Menu buttons
  document.querySelectorAll('.menu-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const mode = btn.dataset.mode;
      if (mode === 'sentences') {
        switchView('sentences');
      } else {
        currentMode = mode;
        elements.verbTitle.textContent = mode === 'separable'
          ? 'Trennbare Präfixe'
          : 'Untrennbare Präfixe';
        switchView('verb');
      }
    });
  });

  // Back buttons
  document.querySelectorAll('.back-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      switchView(btn.dataset.back);
    });
  });

  // Sentence controls
  elements.showTranslationBtn.addEventListener('click', toggleSentenceTranslation);
  elements.nextSentenceBtn.addEventListener('click', showNextSentence);

  // Verb controls
  elements.showMeaningBtn.addEventListener('click', toggleVerbMeaning);
  elements.nextVerbBtn.addEventListener('click', showNextVerb);

  // Keyboard shortcuts
  document.addEventListener('keydown', (e) => {
    // ESC - go to menu
    if (e.key === 'Escape') {
      e.preventDefault();
      switchView('menu');
      return;
    }

    // Skip navigation if typing in an input
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
      return;
    }

    // View-specific shortcuts
    if (views.sentences.classList.contains('active')) {
      switch (e.key.toLowerCase()) {
        case 't':
          e.preventDefault();
          toggleSentenceTranslation();
          break;
        case 'n':
          e.preventDefault();
          showNextSentence();
          break;
        case 'm':
          e.preventDefault();
          switchView('menu');
          break;
      }
    } else if (views.verb.classList.contains('active')) {
      switch (e.key.toLowerCase()) {
        case 'b':
          e.preventDefault();
          toggleVerbMeaning();
          break;
        case 'n':
          e.preventDefault();
          showNextVerb();
          break;
        case 'm':
          e.preventDefault();
          switchView('menu');
          break;
      }
    }

    // Arrow key navigation for menu
    if (views.menu.classList.contains('active')) {
      const menuButtons = Array.from(document.querySelectorAll('.menu-btn'));
      const activeIndex = menuButtons.findIndex(btn => btn === document.activeElement);

      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        e.preventDefault();
        let newIndex;
        if (e.key === 'ArrowDown') {
          newIndex = activeIndex < menuButtons.length - 1 ? activeIndex + 1 : 0;
        } else {
          newIndex = activeIndex > 0 ? activeIndex - 1 : menuButtons.length - 1;
        }
        menuButtons[newIndex].focus();
      }
    }
  });

  // Touch/swipe support for mobile
  let touchStartX = 0;
  let touchStartY = 0;

  document.addEventListener('touchstart', (e) => {
    touchStartX = e.touches[0].clientX;
    touchStartY = e.touches[0].clientY;
  }, { passive: true });

  document.addEventListener('touchend', (e) => {
    const touchEndX = e.changedTouches[0].clientX;
    const touchEndY = e.changedTouches[0].clientY;

    const diffX = touchEndX - touchStartX;
    const diffY = touchEndY - touchStartY;

    // Horizontal swipe for next item
    if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 50) {
      if (diffX < 0 && views.sentences.classList.contains('active')) {
        showNextSentence();
      } else if (diffX < 0 && views.verb.classList.contains('active')) {
        showNextVerb();
      }
    }

    // Vertical swipe to toggle
    if (Math.abs(diffY) > Math.abs(diffX) && Math.abs(diffY) > 50) {
      if (views.sentences.classList.contains('active') && diffY < 0) {
        toggleSentenceTranslation();
      } else if (views.verb.classList.contains('active') && diffY < 0) {
        toggleVerbMeaning();
      }
    }
  }, { passive: true });
}

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
  initData();
  setupEventListeners();
  console.log('Deutsch-Lernprogramm initialized');
});
