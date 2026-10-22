(function () {
  "use strict";

  const MODES = {
    sentence: { title: "Übersetzungsübung", items: "sentences" },
    separable: { title: "Verbtraining: Trennbare Präfixe", items: "separableVerbs" },
    inseparable: { title: "Verbtraining: Untrennbare Präfixe", items: "inseparableVerbs" },
  };

  const els = {
    status: document.getElementById("status"),
    menu: document.getElementById("menu"),
    practice: document.getElementById("practice"),
    title: document.getElementById("mode-title"),
    prompt: document.getElementById("prompt"),
    answer: document.getElementById("answer"),
    reveal: document.getElementById("reveal"),
    next: document.getElementById("next"),
    home: document.getElementById("home"),
    hint: document.getElementById("hint"),
  };

  let data = null;
  let mode = null;
  let current = null;
  let lastIndex = -1;

  function showError(message) {
    els.status.textContent = message;
    els.status.classList.add("error");
  }

  function pickItem() {
    const items = data[MODES[mode].items];
    if (items.length === 0) return null;
    // Avoid showing the same item twice in a row when there is a choice.
    let index = Math.floor(Math.random() * items.length);
    if (items.length > 1 && index === lastIndex) {
      index = (index + 1 + Math.floor(Math.random() * (items.length - 1))) % items.length;
    }
    lastIndex = index;
    return items[index];
  }

  function hideAnswer() {
    els.answer.hidden = true;
    els.answer.replaceChildren();
    els.reveal.textContent = mode === "sentence" ? "Übersetzung (t)" : "Bedeutung (b)";
  }

  function renderAnswer() {
    const lines = [];
    if (mode === "sentence") {
      lines.push(["label", "Deutsch"], ["text", current.german]);
    } else {
      lines.push(["label", "Bedeutung"], ["text", current.english]);
      if (current.example) {
        lines.push(["label", "Beispiel"], ["text", current.example]);
      }
    }
    const nodes = lines.map(([kind, text]) => {
      const p = document.createElement("p");
      p.className = kind;
      p.textContent = text;
      return p;
    });
    els.answer.replaceChildren(...nodes);
    els.answer.hidden = false;
    els.reveal.textContent = "Ausblenden";
  }

  function showCurrent() {
    current = pickItem();
    hideAnswer();
    if (!current) {
      els.prompt.textContent = "Keine Einträge gefunden.";
      return;
    }
    els.prompt.textContent = mode === "sentence" ? current.english : current.german;
    els.prompt.className = "prompt " + (mode === "sentence" ? "sentence" : "verb");
    els.hint.textContent = mode === "sentence"
      ? "t = Übersetzung · n = nächster Satz · m = Hauptmenü"
      : "b = Bedeutung · n = nächstes Verb · m = Hauptmenü";
  }

  function toggleAnswer() {
    if (!current) return;
    if (els.answer.hidden) {
      renderAnswer();
    } else {
      hideAnswer();
    }
  }

  function setMenuSelection(selected) {
    for (const button of els.menu.querySelectorAll("button")) {
      button.setAttribute("aria-current", String(button.dataset.mode === selected));
    }
  }

  function startMode(selected) {
    mode = selected;
    setMenuSelection(selected);
    els.title.textContent = MODES[selected].title;
    els.practice.hidden = false;
    els.status.textContent = "";
    showCurrent();
  }

  function goHome() {
    mode = null;
    current = null;
    setMenuSelection(null);
    els.practice.hidden = true;
    els.status.textContent = "Wähle einen Modus.";
  }

  els.menu.addEventListener("click", (event) => {
    const button = event.target.closest("button[data-mode]");
    if (button && data) startMode(button.dataset.mode);
  });

  els.reveal.addEventListener("click", toggleAnswer);
  els.next.addEventListener("click", showCurrent);
  els.home.addEventListener("click", goHome);

  // Same keys as the terminal app: t/b reveal, n next, m main menu.
  document.addEventListener("keydown", (event) => {
    if (!mode || event.ctrlKey || event.metaKey || event.altKey) return;
    if (event.target.closest && event.target.closest("button")) return;
    const key = event.key.toLowerCase();
    if (key === "t" || key === "b") toggleAnswer();
    else if (key === "n") showCurrent();
    else if (key === "m") goHome();
  });

  fetch("/api/data", { cache: "no-store" })
    .then((response) => {
      if (!response.ok) throw new Error("HTTP " + response.status);
      return response.json();
    })
    .then((payload) => {
      data = payload;
      els.status.textContent = "Wähle einen Modus.";
      els.status.classList.remove("error");
    })
    .catch((error) => {
      showError("Daten konnten nicht geladen werden: " + error.message);
    });
})();
