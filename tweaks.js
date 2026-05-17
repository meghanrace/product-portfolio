// Persist palette across pages and expose the Tweaks panel.
(function () {
  const STORAGE_KEY = "mr_palette";
  const TYPE_KEY = "mr_typeface";
  const palette = localStorage.getItem(STORAGE_KEY) || "marsh";
  const typeface = localStorage.getItem(TYPE_KEY) || "instrument";
  document.documentElement.setAttribute("data-palette", palette);
  document.documentElement.setAttribute("data-typeface", typeface);

  // Typeface swaps applied via CSS variable on root
  const TYPE_MAP = {
    instrument: { serif: '"Instrument Serif", Georgia, serif', sans: '"Geist", system-ui, sans-serif' },
    cormorant:  { serif: '"Cormorant Garamond", Georgia, serif', sans: '"Geist", system-ui, sans-serif' },
    newsreader: { serif: '"Newsreader", Georgia, serif', sans: '"Inter Tight", system-ui, sans-serif' },
  };

  function applyType(name) {
    const t = TYPE_MAP[name] || TYPE_MAP.instrument;
    // Override on the body via a style tag we keep updating
    let s = document.getElementById("__type-override");
    if (!s) { s = document.createElement("style"); s.id = "__type-override"; document.head.appendChild(s); }
    s.textContent = `
      .serif, h1, h2, h3, h4, .h-display, .h-section, .h-card, .pull, .nav-brand, .footer .sig { font-family: ${t.serif} !important; }
    `;
    // Inject Google Fonts for non-default
    const id = "__type-fonts-" + name;
    if (!document.getElementById(id)) {
      const link = document.createElement("link");
      link.id = id; link.rel = "stylesheet";
      if (name === "cormorant") link.href = "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&display=swap";
      else if (name === "newsreader") link.href = "https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,8..60,400;0,8..60,500;1,8..60,400&family=Inter+Tight:wght@300..600&display=swap";
      else return;
      document.head.appendChild(link);
    }
  }
  if (typeface !== "instrument") applyType(typeface);

  // === Tweaks panel ===
  let panelEl = null;
  function buildPanel() {
    if (panelEl) return panelEl;
    panelEl = document.createElement("div");
    panelEl.id = "tweaks-panel";
    panelEl.innerHTML = `
      <style>
        #tweaks-panel { position: fixed; right: 24px; bottom: 24px; width: 296px; z-index: 300;
          background: var(--bg); color: var(--ink); border: 1px solid var(--rule);
          border-radius: 8px; box-shadow: 0 30px 60px -20px rgba(0,0,0,0.35); font-family: "Geist", system-ui, sans-serif;
          overflow: hidden; }
        #tweaks-panel header { display: flex; align-items: center; justify-content: space-between;
          padding: 14px 16px; border-bottom: 1px solid var(--rule);
          font-family: "Instrument Serif", serif; font-size: 22px; }
        #tweaks-panel header em { color: var(--accent); font-style: italic; }
        #tweaks-panel .close { background: none; border: 0; color: var(--ink-soft); cursor: pointer;
          font-family: "Geist Mono", monospace; font-size: 14px; padding: 4px 8px; }
        #tweaks-panel .body { padding: 16px; display: grid; gap: 18px; }
        #tweaks-panel label { font-family: "Geist Mono", monospace; font-size: 10px;
          letter-spacing: 0.12em; text-transform: uppercase; color: var(--ink-faint);
          display: block; margin-bottom: 8px; }
        .swatches { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; }
        .swatch { cursor: pointer; border: 1px solid var(--rule); border-radius: 6px; padding: 10px 10px 12px;
          background: transparent; text-align: left; font-family: "Geist", sans-serif;
          color: var(--ink); font-size: 12px; transition: border-color .15s, transform .15s; }
        .swatch:hover { transform: translateY(-1px); }
        .swatch[aria-pressed="true"] { border-color: var(--accent); box-shadow: inset 0 0 0 1px var(--accent); }
        .swatch .chips { display: flex; gap: 3px; margin-bottom: 8px; }
        .swatch .chip { width: 18px; height: 18px; border-radius: 4px; border: 1px solid rgba(0,0,0,0.08); }
        .swatch .name { font-weight: 500; }
        .type-row { display: grid; gap: 6px; }
        .type-row button { background: transparent; border: 1px solid var(--rule); padding: 10px 12px;
          border-radius: 6px; color: var(--ink); text-align: left; cursor: pointer;
          font-family: inherit; transition: border-color .15s; display: flex; justify-content: space-between; align-items: baseline; }
        .type-row button[aria-pressed="true"] { border-color: var(--accent); box-shadow: inset 0 0 0 1px var(--accent); }
        .type-row .preview { font-size: 22px; line-height: 1; }
        .type-row .preview.instrument { font-family: "Instrument Serif", serif; }
        .type-row .preview.cormorant  { font-family: "Cormorant Garamond", serif; }
        .type-row .preview.newsreader { font-family: "Newsreader", serif; }
        .type-row .lbl { font-family: "Geist Mono", monospace; font-size: 10px; color: var(--ink-faint);
          letter-spacing: 0.1em; text-transform: uppercase; }
      </style>
      <header>
        <div>Tweaks <em>·</em> palette</div>
        <button class="close" aria-label="Close">×</button>
      </header>
      <div class="body">
        <div>
          <label>Palette — inspired by the paintings</label>
          <div class="swatches">
            <button class="swatch" data-pal="marsh">
              <div class="chips">
                <span class="chip" style="background:#f4ecd8"></span>
                <span class="chip" style="background:#c9a14a"></span>
                <span class="chip" style="background:#8d4a2a"></span>
              </div>
              <div class="name">Marsh</div>
            </button>
            <button class="swatch" data-pal="drape">
              <div class="chips">
                <span class="chip" style="background:#1a1721"></span>
                <span class="chip" style="background:#7e6b88"></span>
                <span class="chip" style="background:#c2a85f"></span>
              </div>
              <div class="name">Drape</div>
            </button>
            <button class="swatch" data-pal="birch">
              <div class="chips">
                <span class="chip" style="background:#f5f1e8"></span>
                <span class="chip" style="background:#14110d"></span>
                <span class="chip" style="background:#4a4439"></span>
              </div>
              <div class="name">Birch</div>
            </button>
          </div>
        </div>
        <div>
          <label>Display typeface</label>
          <div class="type-row">
            <button data-type="instrument"><span class="preview instrument">Meghan Race</span><span class="lbl">Instrument</span></button>
            <button data-type="cormorant"><span class="preview cormorant">Meghan Race</span><span class="lbl">Cormorant</span></button>
            <button data-type="newsreader"><span class="preview newsreader">Meghan Race</span><span class="lbl">Newsreader</span></button>
          </div>
        </div>
      </div>
    `;
    document.body.appendChild(panelEl);
    syncPressed();

    panelEl.querySelector(".close").addEventListener("click", () => {
      hidePanel();
      try { window.parent.postMessage({ type: "__edit_mode_dismissed" }, "*"); } catch(e) {}
    });
    panelEl.querySelectorAll(".swatch").forEach(b => {
      b.addEventListener("click", () => {
        const pal = b.dataset.pal;
        document.documentElement.setAttribute("data-palette", pal);
        localStorage.setItem(STORAGE_KEY, pal);
        syncPressed();
        try { window.parent.postMessage({ type: "__edit_mode_set_keys", edits: { palette: pal } }, "*"); } catch(e) {}
      });
    });
    panelEl.querySelectorAll(".type-row button").forEach(b => {
      b.addEventListener("click", () => {
        const t = b.dataset.type;
        document.documentElement.setAttribute("data-typeface", t);
        localStorage.setItem(TYPE_KEY, t);
        applyType(t);
        syncPressed();
        try { window.parent.postMessage({ type: "__edit_mode_set_keys", edits: { typeface: t } }, "*"); } catch(e) {}
      });
    });
    return panelEl;
  }
  function syncPressed() {
    const pal = document.documentElement.getAttribute("data-palette");
    const ty = document.documentElement.getAttribute("data-typeface");
    panelEl?.querySelectorAll(".swatch").forEach(b => b.setAttribute("aria-pressed", b.dataset.pal === pal));
    panelEl?.querySelectorAll(".type-row button").forEach(b => b.setAttribute("aria-pressed", b.dataset.type === ty));
  }
  function showPanel() { buildPanel(); panelEl.style.display = "block"; }
  function hidePanel() { if (panelEl) panelEl.style.display = "none"; }

  // Register listener BEFORE announcing availability
  window.addEventListener("message", (e) => {
    const d = e.data;
    if (!d || typeof d !== "object") return;
    if (d.type === "__activate_edit_mode") showPanel();
    if (d.type === "__deactivate_edit_mode") hidePanel();
  });
  try { window.parent.postMessage({ type: "__edit_mode_available" }, "*"); } catch(e) {}
})();
