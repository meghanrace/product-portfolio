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
     values are the marsh palette, which is the site default.
     The document body below keeps its own type system untouched. */
  :root{
    --s-bg:oklch(0.962 0.012 85);--s-bg-2:oklch(0.925 0.020 80);
    --s-ink:oklch(0.22 0.015 55);--s-ink-2:oklch(0.42 0.022 55);--s-ink-3:oklch(0.60 0.025 60);
    --s-rule:oklch(0.80 0.025 70);--s-accent-2:oklch(0.46 0.135 32);
    --s-display:'Instrument Serif','Cormorant Garamond','Times New Roman',serif;
    --s-body:'Geist',ui-sans-serif,system-ui,-apple-system,'Helvetica Neue',Arial,sans-serif;
    --s-mono:'Geist Mono',ui-monospace,'SF Mono',Menlo,Consolas,monospace;
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
    font-size:22px;letter-spacing:-0.005em;color:var(--s-ink);border:0}
  .sitebrand-mark{width:32px;height:32px;border-radius:50%;
    background:url("/assets/meghan-headshot.png") center 18% / cover no-repeat var(--s-bg-2);
    box-shadow:inset 0 0 0 1px color-mix(in oklab,var(--s-ink) 25%,transparent);flex:none}
  .nav-links{display:flex;align-items:center;gap:28px;font-size:14px}
  .nav-links a{color:var(--s-ink-2);position:relative;padding-block:4px}
  .nav-links a:hover{color:var(--s-ink)}
  .nav-links a.active{color:var(--s-ink)}
  .nav-links a.active::after{content:"";position:absolute;left:0;right:0;bottom:-2px;height:2px;background:var(--s-accent-2)}
  @media (max-width:760px){.nav-links{gap:16px;font-size:13px}}

  /* mobile caret nav — checkbox toggle, no JS, same as the rest of the site */
  .nav-toggle-input{position:absolute;width:1px;height:1px;opacity:0;pointer-events:none}
  .nav-toggle{display:none;align-items:center;gap:8px;cursor:pointer;user-select:none;
    font-family:var(--s-mono);font-size:12px;letter-spacing:0.12em;text-transform:uppercase;
    color:var(--s-ink-2);padding:6px 10px;border:1px solid var(--s-rule);border-radius:999px;background:var(--s-bg)}
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
  }

  footer.sitefoot{border-top:1px solid var(--s-rule);padding-block:64px;margin-top:8px;
    color:var(--s-ink-2);font-size:14px;font-family:var(--s-body);background:var(--s-bg)}
  .sitefoot-in{width:min(100% - clamp(40px,8vw,128px),1480px);margin-inline:auto;
    display:flex;flex-wrap:wrap;gap:32px;justify-content:space-between;align-items:end}
  .sitefoot .display{font-family:var(--s-display);font-size:clamp(40px,6vw,64px);line-height:1;color:var(--s-ink)}
  .sitefoot .role{font-family:var(--s-mono);font-size:12px;letter-spacing:0.1em;
    text-transform:uppercase;color:var(--s-ink-3);margin-top:8px}
  .sitefoot .links{display:flex;flex-wrap:wrap;gap:20px}
  .sitefoot .links a{color:var(--s-ink-2);text-decoration:none}
  .sitefoot .links a:hover{color:var(--s-ink)}
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
      <a href="/resources/" class="active">Resources</a>
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
    <span>Made with Claude</span>
  </div>
</footer>"""

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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist:wght@300;400;500;600&family=Geist+Mono:wght@400;500&display=swap">
{head_part.strip()}
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
