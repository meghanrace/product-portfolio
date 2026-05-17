// tweaks.jsx — palette + density controls for Meghan's portfolio
// Adjusts data-palette on <html>, swaps colors live.

const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
  "palette": "marsh",
  "showHeroPainting": true,
  "serifTitles": true
}/*EDITMODE-END*/;

function TweaksApp() {
  const [t, setTweak] = useTweaks(TWEAK_DEFAULTS);

  // Apply palette to <html>
  React.useEffect(() => {
    document.documentElement.setAttribute('data-palette', t.palette);
  }, [t.palette]);

  // Show/hide the hero painting frame on index
  React.useEffect(() => {
    document.querySelectorAll('.hero-painting').forEach(el => {
      el.style.display = t.showHeroPainting ? '' : 'none';
    });
  }, [t.showHeroPainting]);

  // Swap display font family
  React.useEffect(() => {
    const stack = t.serifTitles
      ? "'Instrument Serif', 'Cormorant Garamond', 'Times New Roman', serif"
      : "'Geist', ui-sans-serif, system-ui, sans-serif";
    document.documentElement.style.setProperty('--f-display', stack);
  }, [t.serifTitles]);

  return (
    <TweaksPanel>
      <TweakSection label="Palette" />
      <TweakColor
        label="Theme"
        value={paletteSwatch(t.palette)}
        options={[
          ['#d8a85b', '#a85a3a', '#7b8a52'],   // marsh
          ['#b9a3c1', '#9c5a64', '#7c8aa3'],   // drape
          ['#8a6238', '#46563b', '#1a1810']    // birch
        ]}
        onChange={(v) => setTweak('palette', swatchToPalette(v))}
      />
      <TweakRadio
        label="Mood"
        value={t.palette}
        options={['marsh', 'drape', 'birch']}
        onChange={(v) => setTweak('palette', v)}
      />
      <TweakSection label="Display" />
      <TweakToggle
        label="Serif titles"
        value={t.serifTitles}
        onChange={(v) => setTweak('serifTitles', v)}
      />
      <TweakToggle
        label="Hero painting"
        value={t.showHeroPainting}
        onChange={(v) => setTweak('showHeroPainting', v)}
      />
    </TweaksPanel>
  );
}

function paletteSwatch(p) {
  return ({
    marsh: ['#d8a85b', '#a85a3a', '#7b8a52'],
    drape: ['#b9a3c1', '#9c5a64', '#7c8aa3'],
    birch: ['#8a6238', '#46563b', '#1a1810']
  })[p] || ['#d8a85b', '#a85a3a', '#7b8a52'];
}
function swatchToPalette(arr) {
  if (!Array.isArray(arr)) return 'marsh';
  if (arr[0] === '#b9a3c1') return 'drape';
  if (arr[0] === '#8a6238') return 'birch';
  return 'marsh';
}

// Mount
const tweaksRoot = document.createElement('div');
tweaksRoot.id = 'tweaks-root';
document.body.appendChild(tweaksRoot);
ReactDOM.createRoot(tweaksRoot).render(<TweaksApp />);
