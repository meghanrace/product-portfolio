"""
Port the two guides into meghanrace-site as full HTML pages.

The guides are authored here as Claude artifact body fragments: no
doctype, html, head or body tag. This wraps each one in a real document
with meta, OG/Twitter tags, favicon and GA4, adds site nav and footer
built from the guide's own design tokens, and rewrites the cross-links
between the two to real site paths.

The guides deliberately do not load the site's styles.css. Their .shell
and .brand rules collide with it, and the type systems differ.

Run it after editing a guide in this folder, from anywhere:

    python3 _guides/port-to-site.py

Then verify in a browser and commit. The generated pages in resources/
are overwritten every run, so never edit those directly.
"""

import os, re

# Paths are derived from this file's own location, so the script runs from
# anywhere: the authored guides sit beside it, the generated pages go into
# the site's resources/ directory one level up.
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = HERE
DST = os.path.join(os.path.dirname(HERE), "resources")

def strip_block(css, opener):
    """Remove a brace-balanced CSS block, given the exact text that opens it."""
    i = css.find(opener)
    if i == -1:
        return css
    depth = 0
    for j in range(i + len(opener) - 1, len(css)):
        if css[j] == '{':
            depth += 1
        elif css[j] == '}':
            depth -= 1
            if depth == 0:
                return css[:i] + css[j + 1:]
    return css


GA = '''<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XETS41340P"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-XETS41340P');
</script>'''

SITE_CSS = """
<style>
  /* ---------- SITE CHROME ----------
     Lifted from the site's own nav and footer rules so the header reads as
     part of meghanrace.com. Tokens are prefixed --s-* because the guide
     already owns --bg, --ink and friends with entirely different values;
     values match styles.css (warm paper, slate ink, magenta / turquoise
     pigments) so the guides' header and footer read as the same site.
     The document body is restyled by GUIDE_THEME below. */
  :root{
    --s-bg:#f4efe4;--s-bg-2:#ece5d6;
    --s-ink:#262b34;--s-ink-2:#4a505b;--s-ink-3:#747985;
    --s-rule:#d5cbb6;--s-accent-2:#b8246b;--s-turq:#08847d;--s-gold:#e8b324;--s-on:#fbf6ec;
    --s-display:'Bricolage Grotesque',ui-sans-serif,system-ui,sans-serif;
    --s-body:'Bricolage Grotesque',ui-sans-serif,system-ui,-apple-system,'Helvetica Neue',Arial,sans-serif;
    --s-mono:'Spline Sans Mono',ui-monospace,'SF Mono',Menlo,Consolas,monospace;
    --s-brush:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 600 100' preserveAspectRatio='none'%3E%3Cfilter id='f' x='-5%25' y='-30%25' width='110%25' height='160%25'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.012 0.09' numOctaves='3' seed='4' result='n'/%3E%3CfeDisplacementMap in='SourceGraphic' in2='n' scale='26' xChannelSelector='R' yChannelSelector='G' result='d'/%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.003 0.42' numOctaves='2' seed='9' result='s'/%3E%3CfeColorMatrix in='s' type='matrix' values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 -0.9 0 0 0 1.55' result='a'/%3E%3CfeComposite in='d' in2='a' operator='in'/%3E%3C/filter%3E%3Crect x='16' y='18' width='568' height='64' rx='10' filter='url(%23f)'/%3E%3C/svg%3E");
  }

  /* Sticky, like every other page on the site, so Resources is always one
     click away from inside a guide.

     The site nav and the guide's own bar live in ONE sticky wrapper rather
     than two stacked sticky elements offset by a measured height. A measured
     offset can latch onto a transient value (a mid-transition menu, a
     pre-webfont layout) and then has no way to correct itself, which showed
     up on mobile as the doc bar detaching and floating below the nav. Inside
     a single wrapper the two bars cannot separate: there is no number to get
     wrong. Both are static; the wrapper does the sticking.

     z-index sits above the doc bar but below the mobile TOC drawer (60) and
     its scrim (55), which are meant to cover everything. */
  :root{--stickh:132px}
  .stickytop{position:sticky;top:0;z-index:45}
  /* The nav paints above the doc bar so the mobile menu can drop over it
     rather than shoving it down the page. */
  .nav{position:relative;z-index:2;
    background:color-mix(in oklab,var(--s-bg) 92%,transparent);
    backdrop-filter:saturate(140%) blur(14px);-webkit-backdrop-filter:saturate(140%) blur(14px);
    border-bottom:1px solid color-mix(in oklab,var(--s-rule) 50%,transparent);font-family:var(--s-body)}
  .topbar{position:static;top:auto;z-index:1}
  /* Jump links land below the whole sticky header, not just the doc bar.
     The guides' own 74px offset is sized for the artifact's single bar. */
  section,.anchor-h{scroll-margin-top:calc(var(--stickh) + 16px)}
  /* Only the TOC rail still needs a number, and being a few px off there just
     nudges the rail; it cannot break the header. A ResizeObserver keeps it
     honest through breakpoints, webfont swap and the menu opening. */
  @media (min-width:901px){
    .sidebar{top:calc(var(--stickh) + 4px);max-height:calc(100vh - var(--stickh) - 4px)}
  }
  .nav-row{width:min(100% - clamp(40px,8vw,128px),1480px);margin-inline:auto;
    display:flex;align-items:center;justify-content:space-between;padding-block:18px;gap:24px;position:relative}
  .nav a{color:inherit;text-decoration:none}
  .nav a:hover{text-decoration:none}
  .sitebrand{display:inline-flex;align-items:center;gap:12px;font-family:var(--s-display);
    font-weight:720;font-stretch:84%;font-size:22px;letter-spacing:-0.02em;color:var(--s-ink);border:0}
  .sitebrand-mark{width:32px;height:32px;border-radius:50%;
    background:url("/assets/meghan-headshot.png") center 18% / cover no-repeat var(--s-bg-2);
    flex:none}
  .nav-links{display:flex;align-items:center;gap:26px;font-family:var(--s-mono);font-size:13px;letter-spacing:0.04em}
  .nav-links a{color:var(--s-ink-2);position:relative;padding-block:4px}
  .nav-links a:hover{color:var(--s-ink)}
  .nav-links a.active{color:var(--s-ink)}
  .nav-links a.active::after{content:"";position:absolute;left:0;right:0;bottom:-3px;height:2px;background:var(--s-accent-2)}
  @media (max-width:760px){.nav-links{gap:16px;font-size:13px}}

  /* Desktop dropdown of the four guides. The trigger stays a real link to the
     index; the panel is absolute so it lays over the page. .nav-item's padding
     grows the hover target down to the nav's bottom edge and the negative
     margin gives that space back, so there is no dead gap under the trigger. */
  .nav-item{position:relative;display:inline-flex;align-items:center;padding-block:16px;margin-block:-16px}
  .nav-item::after{content:"";width:5px;height:5px;margin-left:7px;
    border-right:1.2px solid currentColor;border-bottom:1.2px solid currentColor;
    transform:translateY(-2px) rotate(45deg);color:var(--s-ink-3);
    transition:transform 180ms ease,color 180ms ease}
  .nav-item:hover::after,.nav-item:focus-within::after{transform:translateY(1px) rotate(-135deg);color:var(--s-ink)}
  .nav-menu{position:absolute;top:100%;left:-12px;z-index:5;min-width:250px;
    display:flex;flex-direction:column;padding:8px;background:var(--s-bg);
    border:1px solid var(--s-rule);border-radius:12px;
    box-shadow:0 26px 50px -30px color-mix(in oklab,var(--s-ink) 55%,transparent);
    opacity:0;visibility:hidden;transform:translateY(-6px);
    transition:opacity 170ms ease,transform 170ms ease,visibility 170ms}
  .nav-item:hover .nav-menu,.nav-item:focus-within .nav-menu{opacity:1;visibility:visible;transform:translateY(0)}
  .nav-links .nav-menu a{padding:9px 12px;border-radius:8px;color:var(--s-ink-2);white-space:nowrap;
    transition:background 140ms ease,color 140ms ease}
  .nav-links .nav-menu a:hover{background:var(--s-bg-2);color:var(--s-ink)}
  .nav-links .nav-menu a.active::after{display:none}
  /* Below ~1000px a left-anchored panel runs off the right edge and gets
     clipped rather than scrolled. Hang it from the right instead. */
  @media (max-width:1000px){.nav-menu{left:auto;right:-12px}}
  @media (prefers-reduced-motion:reduce){.nav-menu,.nav-item::after{transition:none}}

  /* mobile caret nav — checkbox toggle, no JS, same as the rest of the site */
  .nav-toggle-input{position:absolute;width:1px;height:1px;opacity:0;pointer-events:none}
  .nav-toggle{display:none;align-items:center;gap:8px;cursor:pointer;user-select:none;
    font-family:var(--s-mono);font-size:12px;letter-spacing:0.12em;text-transform:uppercase;
    color:var(--s-ink);padding:6px 0;border:0;background:transparent}
  .nav-toggle:hover{color:var(--s-ink)}
  .nav-toggle-caret{display:inline-block;width:8px;height:8px;
    border-right:1.5px solid currentColor;border-bottom:1.5px solid currentColor;
    transform:translateY(-2px) rotate(45deg);transition:transform 200ms ease}
  .nav-toggle-input:checked ~ .nav-toggle .nav-toggle-caret{transform:translateY(1px) rotate(-135deg)}
  @media (max-width:700px){
    .nav-row{flex-wrap:wrap;row-gap:0;padding-block:16px;column-gap:16px}
    .sitebrand{flex:1 1 auto;min-width:0;font-size:24px}
    .sitebrand-mark{width:36px;height:36px}
    .nav-toggle{display:inline-flex;flex:0 0 auto}
    /* Static row so the absolute menu below anchors to the full-width nav,
       not to the inset content column. */
    .nav-row{position:static}
    .nav-links{position:absolute;top:100%;left:0;right:0;
      flex-direction:column;align-items:flex-start;gap:0;font-size:16px;
      padding-inline:calc(clamp(40px,8vw,128px) / 2);
      background:var(--s-bg);
      border-top:1px solid color-mix(in oklab,var(--s-rule) 60%,transparent);
      border-bottom:1px solid color-mix(in oklab,var(--s-rule) 60%,transparent);
      box-shadow:0 14px 24px color-mix(in oklab,var(--s-ink) 10%,transparent);
      max-height:0;overflow:hidden;opacity:0;visibility:hidden;
      transition:max-height 260ms ease,opacity 200ms ease,padding 200ms ease}
    .nav-toggle-input:checked ~ .nav-links{max-height:70vh;opacity:1;visibility:visible;
      padding-block:6px 10px}
    .nav-links a{padding-block:12px;width:100%}
    .nav-links a.active::after{display:none}
    .nav-links a.active{color:var(--s-accent-2)}
    /* The hover menu is a desktop affordance; on a phone Resources is just a
       link to the index, which lists all four anyway. */
    .nav-item{display:block;width:100%;padding-block:0;margin-block:0}
    /* Blockified or its row padding collapses and Resources sits tighter
       than every other item in the list. */
    .nav-item > a{display:block}
    .nav-item::after{display:none}
    .nav-menu{display:none}
  }

  /* footer: a turquoise field whose top edge is a brush stroke, with a
     magenta and a gold stroke laid over it, same as the rest of the site */
  footer.sitefoot{--s-ink:var(--s-on);--s-ink-2:color-mix(in srgb,var(--s-on) 90%,var(--s-turq));
    --s-ink-3:color-mix(in srgb,var(--s-on) 82%,var(--s-turq));
    position:relative;margin-top:64px;padding-block:clamp(64px,8vw,104px) 40px;
    color:var(--s-ink-2);font-size:14px;font-family:var(--s-body);background:var(--s-turq)}
  footer.sitefoot::before{content:"";position:absolute;left:-2%;right:-2%;top:-38px;height:76px;background:var(--s-turq);
    -webkit-mask:var(--s-brush) center/100% 100% no-repeat;mask:var(--s-brush) center/100% 100% no-repeat;pointer-events:none}
  footer.sitefoot::after{content:"";position:absolute;right:-40px;top:12%;width:min(26vw,380px);height:clamp(60px,7vw,100px);
    background:var(--s-accent-2);-webkit-mask:var(--s-brush) center/100% 100% no-repeat;mask:var(--s-brush) center/100% 100% no-repeat;
    transform:rotate(-3deg);pointer-events:none}
  footer.sitefoot > *{position:relative}
  @media (max-width:700px){footer.sitefoot::after{display:none}}
  .sitefoot-in{width:min(100% - clamp(40px,8vw,128px),1480px);margin-inline:auto;
    display:flex;flex-wrap:wrap;gap:32px;justify-content:space-between;align-items:end}
  .sitefoot .display{font-family:var(--s-display);font-weight:700;font-stretch:86%;font-size:clamp(36px,4.4vw,64px);line-height:0.9;letter-spacing:-0.022em;color:var(--s-ink)}
  .sitefoot .role{font-family:var(--s-mono);font-size:12px;letter-spacing:0.1em;
    text-transform:uppercase;color:var(--s-ink-3);margin-top:8px}
  .sitefoot .links{display:flex;flex-wrap:wrap;gap:8px 20px;font-family:var(--s-mono);font-size:13px}
  .sitefoot .links a{color:var(--s-ink);text-decoration:none}
  .sitefoot .links a:hover{color:var(--s-ink);text-decoration:underline;text-underline-offset:4px}
  .sitefoot-legal{width:min(100% - clamp(40px,8vw,128px),1480px);margin-inline:auto;margin-top:32px;
    font-family:var(--s-mono);font-size:11px;letter-spacing:0.1em;text-transform:uppercase;
    color:var(--s-ink-3);display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
</style>"""

SITE_BAR = """
<header class="nav">
  <nav class="nav-row" aria-label="Primary">
    <a class="sitebrand" href="/">
      <span class="sitebrand-mark" aria-hidden="true"></span>
      <span>Meghan Race</span>
    </a>
    <input id="nav-open" type="checkbox" class="nav-toggle-input" aria-hidden="true" />
    <label for="nav-open" class="nav-toggle" aria-label="Toggle navigation menu">
      <span class="nav-toggle-text">Menu</span>
      <span class="nav-toggle-caret" aria-hidden="true"></span>
    </label>
    <div class="nav-links">
      <a href="/">Home</a>
      <a href="/work">Work</a>
      <a href="/claude">Claude</a>
      <div class="nav-item">
        <a href="/resources/" class="active">Resources</a>
        <div class="nav-menu">
          <a href="/resources/claude-101/">Claude 101</a>
          <a href="/resources/claude-playbook/">The Claude Playbook</a>
          <a href="/resources/claude-code-pm-training-guide">Claude Code for PMs</a>
          <a href="/resources/llm-context-export">Export your LLM context</a>
        </div>
      </div>
      <a href="/art">Art</a>
      <a href="/connect">Connect</a>
    </div>
  </nav>
</header>"""

NAV_SCRIPT = """
<script>
(function(){
  var bar = document.querySelector('.stickytop');
  if (!bar) return;
  function sync(){
    document.documentElement.style.setProperty(
      '--stickh', Math.round(bar.getBoundingClientRect().height) + 'px');
  }
  sync();
  // Several triggers on purpose: ResizeObserver is the precise one, but it is
  // delivered on a rendering step and can be throttled in a backgrounded or
  // hidden view. resize and load cover the breakpoint change and late layout;
  // fonts.ready covers the webfont swap changing the bar's height.
  if (window.ResizeObserver) new ResizeObserver(sync).observe(bar);
  window.addEventListener('resize', sync);
  window.addEventListener('orientationchange', sync);
  window.addEventListener('load', sync);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(sync);
})();
</script>"""

SITE_FOOT = """
<footer class="sitefoot">
  <div class="sitefoot-in">
    <div>
      <div class="display">Meghan Race</div>
      <div class="role">Product Manager · Arvada, CO</div>
    </div>
    <div class="links">
      <a href="mailto:meghan.race@gmail.com">Email</a>
      <a href="https://www.linkedin.com/in/meghan-race" target="_blank" rel="noopener">LinkedIn</a>
      <a href="/resources/">All resources</a>
      <a href="/claude">Claude</a>
      <a href="/work">Work</a>
      <a href="/art">Art</a>
    </div>
  </div>
  <div class="sitefoot-legal">
    <span>Meghan Race · Paintings are her own.</span>
    <span>Made with Claude<span class="site-updated"></span></span>
    <script>
      // GitHub Pages sends Last-Modified as the deploy time, so this is the
      // date the site was last pushed. No stamping step to forget.
      (function () {
        var d = new Date(document.lastModified);
        if (isNaN(d)) return;
        document.querySelector('.site-updated').textContent = ' · Site last updated ' +
          d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
      })();
    </script>
  </div>
</footer>"""

# The guides' own design system (Fraunces + IBM Plex, terracotta accent) is
# swapped for the site's "pigment" look on the website copy only. The authored
# files keep their original look for the Artifact copies. This works because
# every guide component reads its colours from a handful of tokens: override
# the tokens and the fonts, then add the brush strokes and the oil glaze.
# The brush masks are read out of styles.css so there is one copy of each.
_css = open(os.path.join(os.path.dirname(HERE), "styles.css"), encoding="utf-8").read()
BRUSH = re.search(r'--brush:\s*(url\(".*?"\));', _css).group(1)
BRUSH_DENSE = re.search(r'--brush-dense:\s*(url\(".*?"\));', _css).group(1)

FONT_SWAP = {
    '"Fraunces"': '"Bricolage Grotesque"',
    '"IBM Plex Sans"': '"Bricolage Grotesque"',
    '"IBM Plex Mono"': '"Spline Sans Mono"',
}

GUIDE_THEME = """
<style>
  /* ---------- PIGMENT THEME (site copy only) ---------- */
  :root{
    --bg:#f4efe4;--surface:#fbf7ef;--surface-2:#ece5d6;--inset:#efe8da;
    --ink:#262b34;--ink-soft:#3a404b;--muted:#5d6370;--faint:#868a94;
    --line:#ddd3bf;--line-strong:#cbbfa6;
    --accent:#b8246b;--accent-ink:#9c1c5a;--accent-soft:rgba(184,36,107,0.08);--accent-line:rgba(184,36,107,0.3);
    --good:#0b7f78;--good-soft:rgba(16,157,148,0.11);--bad:#c2452a;--bad-soft:rgba(194,69,42,0.09);
    --l1:#109d94;--l2:#1f47a3;--l3:#b8246b;
    --gold:#e8b324;--on:#fbf6ec;
    --shadow:0 18px 40px -28px rgba(38,43,52,0.45);--shadow-soft:none;
    --radius:4px;--radius-sm:3px;
    --brush:%s;
    --brush-dense:%s;
  }
  /* clip, not hidden: hidden would break the sticky header (see CLAUDE.md) */
  html,body{overflow-x:clip}
  body{background:var(--bg);font-size:17.5px}
  h1,h2,h3,h4{font-weight:700;font-stretch:86%%;letter-spacing:-0.02em}
  h4{font-stretch:92%%}
  .docbrand{font-weight:700;font-stretch:86%%;font-size:1.1rem}
  ::selection{background:color-mix(in srgb,var(--gold) 45%%,transparent)}
  a{color:var(--accent-ink);text-decoration:underline;text-decoration-color:var(--accent-line);text-underline-offset:3px}
  a:hover{text-decoration-color:currentColor}
  nav.toc a,a.pairnav,a.companion,.toc-toggle{text-decoration:none}

  /* hero: the key word painted over, an oil glaze drifting behind */
  main{position:relative}
  .hero{position:relative;isolation:isolate;padding-top:64px}
  .hero::before{content:"";position:absolute;z-index:-1;pointer-events:none;right:-58%%;top:2%%;width:82%%;height:96%%;
    background:color-mix(in srgb,var(--glaze) 17%%,transparent);
    -webkit-mask:var(--brush) center/100%% 100%% no-repeat;mask:var(--brush) center/100%% 100%% no-repeat;
    filter:blur(18px);transform:rotate(-8deg);animation:glaze-drift 18s ease-in-out infinite}
  @keyframes glaze-drift{0%%,100%%{transform:rotate(-8deg) translate(0,0) scale(1)}50%%{transform:rotate(-4deg) translate(-4%%,3%%) scale(1.06)}}
  .hero h1{font-size:clamp(2.6rem,6vw,4.2rem);line-height:0.98;letter-spacing:-0.03em}
  .hero h1 em{position:relative;display:inline-block;isolation:isolate;padding:0 0.14em;margin-left:0.04em;font-style:normal;color:var(--on)}
  .hero h1 em::before{content:"";position:absolute;z-index:-1;inset:0.06em -0.08em -0.04em;background:var(--stroke);
    -webkit-mask:var(--brush-dense) center/100%% 100%% no-repeat;mask:var(--brush-dense) center/100%% 100%% no-repeat;
    animation:paint-in 900ms cubic-bezier(.6,.05,.2,1) 250ms both}
  @keyframes paint-in{from{clip-path:inset(0 100%% 0 0)}to{clip-path:inset(0 0 0 0)}}
  .hero p{color:var(--muted)}

  /* small mono labels carry the site's magenta chip */
  .hero .kicker,.eyebrow{display:inline-flex;align-items:center;gap:10px;color:var(--ink-soft);font-weight:500}
  .hero .kicker::before,.eyebrow::before{content:"";width:8px;height:8px;flex:none;background:var(--accent)}

  /* each section heading gets a short stroke underneath, cycling the four pigments */
  h2.sec::after{content:"";display:block;width:96px;height:14px;margin-top:5px;background:var(--accent);
    -webkit-mask:var(--brush) center/100%% 100%% no-repeat;mask:var(--brush) center/100%% 100%% no-repeat}
  main section:nth-of-type(4n+2) h2.sec::after{background:var(--l1)}
  main section:nth-of-type(4n+3) h2.sec::after{background:var(--l2)}
  main section:nth-of-type(4n) h2.sec::after{background:var(--gold)}

  /* the contents rail: active item marked with a painted dab */
  nav.toc a{border-left:0;position:relative}
  nav.toc a.active{background:transparent;color:var(--ink)}
  nav.toc a.active::before{content:"";position:absolute;z-index:-1;left:4px;right:6px;top:3px;bottom:3px;
    background:color-mix(in srgb,var(--accent) 16%%,transparent);
    -webkit-mask:var(--brush) center/100%% 100%% no-repeat;mask:var(--brush) center/100%% 100%% no-repeat}
  nav.toc{position:relative;isolation:isolate}

  /* boxes: flat paper, hairline edges, coloured left rule */
  .callout{border-left-width:4px;background:var(--surface)}
  .callout.rule{border-left-color:var(--l2)}
  .tldr{background:color-mix(in srgb,var(--gold) 14%%,var(--bg));border-color:color-mix(in srgb,var(--gold) 40%%,var(--line))}
  .rung.r1 .lvl{background:var(--l1)}
  ol.steps>li::before{background:var(--accent);border-color:var(--accent);color:var(--on)}

  /* buttons are brush strokes, same as the site's calls to action */
  a.pairnav{background:color-mix(in srgb,var(--l1) 9%%,var(--bg));border-color:color-mix(in srgb,var(--l1) 35%%,transparent)}
  a.pairnav:hover{border-color:var(--l1)}
  .pairnav .pn-btn{position:relative;isolation:isolate;background:transparent;border-radius:0;padding:12px 22px;color:var(--on);font-weight:700}
  .pairnav .pn-btn::before{content:"";position:absolute;inset:0;z-index:-1;background:var(--accent);
    -webkit-mask:var(--brush-dense) center/100%% 100%% no-repeat;mask:var(--brush-dense) center/100%% 100%% no-repeat;transition:background 200ms ease}
  a.pairnav:hover .pn-btn::before{background:var(--l2)}

  @media (max-width:900px){.hero::before{right:-70%%;width:120%%;opacity:0.6}}
  @media (prefers-reduced-motion:reduce){.hero::before,.hero h1 em::before{animation:none}}
</style>""" % (BRUSH, BRUSH_DENSE)

GUIDE_VARS = {
    # hero glaze and the stroke on the hero's key word, per guide
    "claude-101": ("var(--l2)", "var(--l1)"),
    "claude-playbook": ("var(--accent)", "var(--l2)"),
}

# Published artifact URLs -> site paths. The authored guides cross-link by
# artifact URL; keep this in sync if either is ever republished at a new link.
LINKMAP = {
    "https://claude.ai/code/artifact/56cbcaf5-f3ae-492f-9574-c15953fe5f7f": "/resources/claude-101/",
    "https://claude.ai/code/artifact/efe58bf5-8673-4bdf-95c1-a0e6c0fe459e": "/resources/claude-playbook/",
    # legacy relative filenames, in case an older copy is ported
    "claude-field-guide.html": "/resources/claude-101/",
    "claude-playbook.html": "/resources/claude-playbook/",
}

DOCS = [
  dict(src="claude-field-guide.html", slug="claude-101",
       title="Claude 101 · A Practical Handbook · Meghan Race",
       ogtitle="Claude 101 — Meghan Race",
       desc="A plain-English handbook for getting genuinely good at working with Claude. How it actually works, what separates a good prompt from a bad one, Projects, Skills, Connectors, and choosing a model. No technical background required."),
  dict(src="claude-playbook.html", slug="claude-playbook",
       title="The Claude Playbook · Real Recipes · Meghan Race",
       ogtitle="The Claude Playbook — Meghan Race",
       desc="The companion to Claude 101. Real, copyable workflows: automate a recurring chore, pull a report from many tools, produce a standardized deliverable every time, and build your own in five steps."),
]

for d in DOCS:
    raw = open(os.path.join(SRC, d["src"]), encoding="utf-8").read()
    i = raw.index("</style>") + len("</style>")
    head_part, body_part = raw[:i], raw[i:]

    # The guide's own .brand (its doc title chip) collides with the site
    # nav's .brand. Rename the guide's copy; the site header keeps the name.
    head_part = re.sub(r'\.brand\b', '.docbrand', head_part)
    body_part = body_part.replace('class="brand"', 'class="docbrand"')

    # The site has no dark mode: three palettes, all chosen explicitly, with
    # light marsh as the default. Strip the guide's theme machinery so these
    # pages follow the site instead of the reader's OS setting.
    n_media = len(re.findall(r'@media \(prefers-color-scheme:dark\)\{', head_part))
    head_part = strip_block(head_part, '@media (prefers-color-scheme:dark){')
    head_part = strip_block(head_part, ':root[data-theme="dark"]{')
    assert n_media == 1, "expected one prefers-color-scheme block, found %d" % n_media

    # ...and the now-orphaned rules that styled the toggle
    head_part = re.sub(r'\n\s*\.theme-toggle[^{\n]*\{[^}]*\}', '', head_part)

    before = body_part
    body_part = re.sub(r'\s*<button class="theme-toggle".*?</button>', '', body_part, flags=re.S)
    assert body_part != before, "theme toggle button not found"

    # The theme code and the TOC code share one IIFE, so cut only the theme
    # half: from its first line up to where the sidebar code begins.
    before = body_part
    body_part = re.sub(
        r"\n\s*var root=document\.documentElement, icon=document\.getElementById\('themeIcon'\)"
        r".*?(?=\n\s*var sb=document\.getElementById\('sidebar'\))",
        "", body_part, count=1, flags=re.S)
    assert body_part != before, "theme script not found"

    # Swap the guide's fonts for the site's, and drop its font stylesheet:
    # the real <head> loads Bricolage and Spline instead.
    for a, b in FONT_SWAP.items():
        head_part = head_part.replace(a, b)
    head_part = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]*>\s*', '', head_part)
    head_part = re.sub(r'<link rel="preconnect"[^>]*>\s*', '', head_part)

    # Drop the artifact <title>; a full <title> goes in the real <head>.
    head_part = re.sub(r"^<title>.*?</title>\s*", "", head_part, flags=re.S)

    # Cross-links: the authored copies point at the published artifact URLs
    # so they work from inside the artifact sandbox. On the site they must be
    # site-relative. Match without the closing quote so section deep-links
    # (…#skills) carry their anchor across.
    for src_href, dst_href in LINKMAP.items():
        body_part = body_part.replace('href="%s' % src_href, 'href="%s' % dst_href)

    # Those artifact links carry target="_blank" rel="noopener". Same-site
    # navigation should not open a new tab, so strip it from our own links.
    def strip_target(m):
        attrs = m.group(2)
        attrs = re.sub(r'\s*target="_blank"', '', attrs)
        attrs = re.sub(r'\s*rel="noopener"', '', attrs)
        return '<a %s%s>' % (m.group(1), attrs)
    body_part = re.sub(r'<a ([^>]*href="/resources/[^"]*")([^>]*)>', strip_target, body_part)

    # Pull the guide's own bar out so it can share one sticky wrapper with
    # the site nav (see .stickytop above). Done last, so the bar has already
    # had its cross-links rewritten and its theme toggle removed.
    split = body_part.index('<div class="scrim"')
    topbar_html, body_part = body_part[:split].strip(), body_part[split:]
    assert topbar_html.startswith('<div class="topbar">'), "topbar not where expected"
    assert 'claude.ai/code/artifact' not in topbar_html, "topbar cross-link not rewritten"
    assert 'theme-toggle' not in topbar_html, "topbar theme toggle not removed"

    url = "https://www.meghanrace.com/resources/%s/" % d["slug"]
    out = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{d["title"]}</title>
<meta name="description" content="{d["desc"]}" />
<meta property="og:type"        content="article" />
<meta property="og:url"         content="{url}" />
<meta property="og:title"       content="{d["ogtitle"]}" />
<meta property="og:description" content="{d["desc"]}" />
<meta property="og:image"       content="https://www.meghanrace.com/assets/og-image.jpg" />
<meta name="twitter:card"       content="summary_large_image" />
<meta name="twitter:title"      content="{d["ogtitle"]}" />
<meta name="twitter:description" content="{d["desc"]}" />
<meta name="twitter:image"      content="https://www.meghanrace.com/assets/og-image.jpg" />
<link rel="canonical" href="{url}" />
<link rel="icon" type="image/svg+xml" href="/favicon.svg" />
{GA}
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,300..800&family=Spline+Sans+Mono:wght@400;500;600&display=swap">
{head_part.strip()}
{GUIDE_THEME}
<style>:root{{--glaze:{GUIDE_VARS[d["slug"]][0]};--stroke:{GUIDE_VARS[d["slug"]][1]}}}</style>
{SITE_CSS}
</head>
<body>
<div class="stickytop">
{SITE_BAR}
{topbar_html}
</div>
{NAV_SCRIPT}
{body_part.strip()}
{SITE_FOOT}
</body>
</html>
'''
    outdir = os.path.join(DST, d["slug"])
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, "index.html")
    open(p, "w", encoding="utf-8").write(out)
    print("wrote", p, len(out), "bytes")
