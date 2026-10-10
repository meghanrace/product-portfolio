# meghanrace-site — Claude context

Personal portfolio site for Meghan Race, PM at Exclusive Resorts. Static HTML/CSS, no build step, no framework. Edited via Claude Code.

---

## Site map

Clean URLs throughout: every page is `<dir>/index.html` and is linked as `/<dir>/` or `/<dir>`. There are no `.html` paths in links any more, and adding one will 404.

| File | URL | Purpose |
|------|-----|---------|
| `index.html` | `/` | Home: hero, about, stats, Claude strip, resources strip |
| `work/index.html` | `/work` | Case study index + portal screenshot |
| `claude/index.html` | `/claude` | How I use Claude day-to-day (practice only) |
| `resources/index.html` | `/resources/` | Guide library, grouped by audience |
| `art/index.html` | `/art` | Mural sections + oil paintings gallery |
| `connect/index.html` | `/connect` | Contact page |
| `work/<slug>/index.html` | `/work/<slug>` | Five case studies |
| `resources/<slug>/index.html` | `/resources/<slug>` | Four guides (see below) |

### The resources library

`/resources/` is the entry point and groups the four guides by who they are for:

| Guide | URL | Audience |
|-------|-----|----------|
| Claude 101 | `/resources/claude-101/` | Everyone. Part 1 of 2 |
| The Claude Playbook | `/resources/claude-playbook/` | Everyone. Part 2 of 2 |
| Claude Code for PMs | `/resources/claude-code-pm-training-guide` | PMs |
| Export your LLM context | `/resources/llm-context-export` | PMs |

Claude Code for PMs and Export your LLM context are hand-authored and share `resources/article.css`. Both use the doc layout: a `.page-hero.doc-hero` (back link, eyebrow, h1 with a `.stroke` and an `.h1-sub` line, lede, `.doc-meta`), then `.shell-wide.doc`, a grid of a sticky `.doc-toc` contents rail and the `.article` reading column. Each `h2` in the article has an `id` that the rail links to; add a section by adding both. `resources/doc.js` marks the section in view. Below 900px the rail becomes a static contents list above the article.

`/resources/cowork-for-pms/` is a noindex redirect stub to `/resources/`. The Cowork guide was retired in October 2026 when Cowork folded into Chat; the stub keeps old shared links working. Point readers to scheduled tasks in Chat, not Cowork.

**Claude 101 and The Claude Playbook are generated, not authored, in `resources/`.** Every other page on this site you edit directly. These two you never touch there: the pages in `resources/claude-101/` and `resources/claude-playbook/` are output, overwritten on every port.

## `_guides/` — source of truth for the two Claude guides

```
_guides/
  claude-field-guide.html    Claude 101, authored here
  claude-playbook.html       The Claude Playbook, authored here
  port-to-site.py            generates the two pages in resources/
```

The leading underscore is load-bearing: this site runs Jekyll on GitHub Pages (there is no `.nojekyll`), and Jekyll skips underscore-prefixed directories when it builds. So `_guides/` is versioned and backed up with the rest of the repo but is never served as a web page. Renaming it to `guides/` would publish the raw source at `meghanrace.com/guides/...`.

### Editing a guide

Edit the file in `_guides/`, then from anywhere in the repo:

```
python3 _guides/port-to-site.py
```

Verify in a browser, then commit. Both the source and the regenerated pages belong in the same commit.

### What the port actually does

It is a transform, not a copy, and parts of it are lossy. The authored files are **artifact body fragments**: no `<!doctype>`, `<html>`, `<head>` or `<body>`, opening straight into `<title>`, font links and a `<style>` block. That is the format the Artifact publisher expects, which is how they were written. The port:

- wraps each fragment in a full HTML document with meta, OG/Twitter, canonical, favicon and GA4
- adds the site nav and footer, built from the site's real nav rules but with `--s-*` prefixed tokens so they cannot clobber the guides' own `--bg` / `--ink`
- renames the guides' `.brand` to `.docbrand`, clearing a collision with the site nav's `.brand`
- strips dark mode entirely: the theme toggle, its script, and the dark CSS blocks, because the site has one light palette and no dark mode
- rewrites the cross-links between the two guides from artifact URLs to site paths, and drops `target="_blank"` from them

Because dark mode is deleted rather than hidden, **the website copy cannot be used to regenerate the artifact copy.** The file in `_guides/` is the only complete version.

The generated pages deliberately do not load `styles.css`: the guides' `.shell` and `.brand` rules collide with the site's. They keep their own layout (sidebar TOC with scroll-spy, callouts, cards) but wear the site's pigment look on the website copy only. `GUIDE_THEME` in the port overrides the guides' colour tokens, swaps Fraunces and IBM Plex for Bricolage and Spline (`FONT_SWAP`), paints the hero's `<em>` word as a brush stroke over a drifting oil glaze, and adds a short pigment stroke under each section heading. `GUIDE_VARS` sets the glaze and stroke colours per guide. The brush masks are read out of `styles.css` at port time, so a change to `--brush` there needs a re-port to reach the guides.

The authored files in `_guides/` keep the original Fraunces and terracotta look, so the Artifact copies are unchanged by this.

### Published as Artifacts too

Both guides are also published as shareable Claude Artifacts, from the `_guides/` source directly. Private by default; shared via the share menu on the page.

| Doc | Artifact URL |
|-----|--------------|
| Claude 101 | https://claude.ai/code/artifact/56cbcaf5-f3ae-492f-9574-c15953fe5f7f |
| The Claude Playbook | https://claude.ai/code/artifact/efe58bf5-8673-4bdf-95c1-a0e6c0fe459e |

Republishing from a conversation that did not create them requires passing the URL, or you get a duplicate artifact at a new link. The cross-links inside the authored files point at these artifact URLs, which is correct for the artifact copy; the port rewrites them for the site copy. If either is ever republished at a new URL, update `LINKMAP` at the top of `port-to-site.py`.

A guide edit therefore has three destinations: `_guides/` (source), the website (re-port and push), and the Artifact (republish at the same URL). They do not update each other.

### Section IDs

Claude 101: `how` · `basics` · `threads` · `surfaces` · `projects` · `skills` · `voice` · `connectors` · `models` · `recap`

The Playbook: `mindset` · `anatomy` · `chore` · `report` · `template` · `routine` · `todo` · `build` · `recap`

### Shared class vocabulary

`sec` section wrapper · `shell` content column · `prose` body text · `lead` intro paragraph · `eyebrow` small caps label · `callout` / `tip` / `warn` boxed asides · `good` / `bad` prompt comparison pairs · `steps` numbered list · `levels` / `lv` the three-tier ladder · `tldr` recap block · `toc` sidebar nav · `companion` cross-doc link · `mini` small muted aside.

Playbook-only: `jobs` / `job` task menu, `flow` / `node` workflow diagrams, `promptbox` copyable prompt blocks, `qgrid` / `qcard` question cards, `ladder` / `rung` the Ask → Delegate → Automate visual.

### Conventions for the guides

- Version stamps live in the top bar. Claude 101 is at v1.2, the Playbook at v1.1. Bump on material change.
- The guides use a spaced hyphen ` - ` throughout rather than em-dashes, matching the root voice rules.
- Check both light and dark in the artifact copy, and under 900px where the TOC collapses to a drawer.
- A structural change to one guide should usually be mirrored in the other. They are a matched pair and readers move between them.

## Key copy locations

### index.html
`<body class="home">`. The home page's layout CSS lives in its own inline `<style>` block.
- **Hero h1** — "From managing service leaders / to managing digital products." in `.hero2.page-hero`. "digital products." is a `.stroke`.
- **Hero facts** — `.facts` / `.fact`: 4 yrs in product, $200M+, ~25K, 6 certifications. They count up on load (`motion.js`).
- **About section** — lede + 4 paragraphs in `.ab-body` inside `data-screen-label="02 About"`. The heading and portrait (`.ab-left`) stay pinned while the text scrolls.
- **What I do now** — heading "What owning it means", the five numbered statements in `.wd-list .bullets`. Left column pinned the same way.
- **Claude teaser** — three `.cl` columns, each with a `.cl-swatch` stroke.
- **Resources** — `.toc` ruled list of guides.
- **Certifications** — moved to `/work` (Credentials section); one sentence in About.
- **Experience** — `.gx` career timeline: one row per role, each bar a brush stroke positioned by `--a` / `--b` (percent of 2007–2027). Add a role by adding a row and computing its two percentages.
- **Closing** — "I'd rather have the conversation than the email thread." pull quote, `.x-cta` brush-stroke button. The stat ticker runs along the top of the home footer.

### work/index.html
- **Hero lede** — `.lede` paragraph under the h1. Describes the Member Portal and five case studies.
- **Case index** — `<ol class="case-index">` with five list items linking to subpages. Update here when adding/removing cases.
- **Portal screenshot caption** — figcaption under `assets/work/portal-home.png`.

### claude/index.html
- **Hero lede** — The main paragraph describing how Claude Code changed what a PM can own.
- **On this page** — `<ol class="case-index three-up">`: Setup, Workflow, Hard-won tips. Update if you add or remove a section.
- **Body sections** — `#setup`, `#workflow`, `#tips`, then the CTA and colophon. The teaching content that used to live here is now `/resources/`.
- **Colophon** — the five-step pipeline list. Step 04 is GitHub Pages, which is what actually hosts this site.

### art/index.html
- **Hero lede** — Studio intro paragraph.
- **Mural body copy** — Inside `.mural-body` div in the aspen stairwell section.
- **Oil paintings lede** — Under "From the studio years." heading — describes landscapes + fabric series.
- **Artist note** — `data-screen-label` not set; the pull quote + two paragraphs near the bottom.

### Case study subpages (work/<slug>/index.html)
Each has a cols-2 layout at the top:
- Left column: eyebrow ("Case 01"), h2 title, chips
- Right column: stats div + 2–3 lede/body paragraphs
The body paragraphs are the main case study copy.

---

## Voice and style rules

Universal rules (no em-dashes, concrete language, forward-facing tone, no trailing summaries, etc.) now live in the root `CLAUDE.md` one level up and apply here too. Nothing site-specific to add beyond that currently.

---

## Tech and CSS conventions

### Sticky nav

The nav is `position: sticky` on every page, which is how you get back to `/resources/` from inside a guide.

This only works because `html` and `body` use `overflow-x: clip` rather than `overflow-x: hidden`. `hidden` forces `overflow-y` to compute as `auto`, which turns the element into a scroll container and silently breaks `position: sticky` on every descendant. The nav had been declared sticky for a long time without ever sticking. If horizontal overflow reappears, fix the element causing it: do not put `overflow-x: hidden` back on `html` or `body`.

On the two Claude guides the site nav and the guide's own doc bar sit inside a single `.stickytop` wrapper. Both are `position: static`; the wrapper does the sticking. They are not two stacked sticky bars joined by a measured offset: that version latched onto a transient height on mobile and left the doc bar floating in the middle of the page with no way to correct itself. Inside one wrapper there is no number to get wrong. z-index is wrapper 45, nav 2, doc bar 1, TOC scrim 55, TOC drawer 60, so the mobile drawer still covers everything.

`--stickh` is still measured at runtime, but only the TOC rail reads it. Being a few pixels off there nudges the rail and cannot break the header.

### After editing any .css — stamp it

```
python3 _tools/stamp-css.py
```

Every stylesheet link carries a content hash (`/styles.css?v=5c42b8fa`). Run this after touching a `.css` file and before committing; it rewrites the hash on all 14 pages that link one. It is idempotent, so running it when nothing changed is a no-op.

This is not optional polish. Browsers cache stylesheets hard and GitHub Pages gives no control over cache headers, so without a version on the URL a returning visitor keeps their old `styles.css` against freshly deployed HTML. On 2026-08-30 that shipped a genuinely broken page: a phone holding the previous stylesheet had no `.nav-menu` rules at all, so the new dropdown markup rendered as five links of raw text dumped into the mobile menu, and the mobile menu went back to pushing the page down. The site looked correct on every machine that had never cached it, which is exactly why it was easy to miss.

The two Claude guides inline all their CSS, so they are immune and the stamper skips them.

### Nav menu behavior

Both behaviors below live in `styles.css` and are mirrored in `port-to-site.py`'s `SITE_CSS` with `--s-*` tokens. Change one, change the other.

**Mobile menu (max-width 700px)** is an overlay: `.nav-links` is `position: absolute; top: 100%` so opening it lays the menu over the page instead of pushing the hero down. Two things it depends on. `.nav-row` drops to `position: static` at this breakpoint so the menu anchors to the full-bleed `.nav` rather than the inset content column. And `.nav-links` needs its own opaque `background: var(--bg)`, because the nav's is translucent and the page would show through.

**Desktop dropdown** under Resources lists all four guides. The trigger stays a real link, so Resources still opens the index. `.nav-item` carries `padding-block: 16px; margin-block: -16px` — the padding grows the hover target down to the nav's bottom edge, the negative margin gives the space back to the layout, and the panel at `top: 100%` then adjoins the trigger with no dead gap for the pointer to fall through. Below 1000px the panel flips to `right: -12px`, because a left anchor runs past the right edge and `overflow-x: clip` would silently cut it off rather than let it scroll. Below 700px the panel is hidden and `.nav-item > a` is blockified so Resources keeps the same row height as every other item.

Adding a fifth guide means editing the `.nav-menu` block in all 14 hand-authored pages plus `SITE_BAR` in the port script.

**The guide-to-guide link** (`.companion` in the doc bar: "Playbook →" / "← Claude 101") lives in the authored guides, not the port. Below 620px it swaps to a short label via `.c-full` / `.c-short` and the version stamp next to the doc title is hidden, which is what buys the room. It used to be `display: none` at that breakpoint, so on a phone the only route between the two guides was a link buried in the body copy.

### Footer "last updated" date

Every footer, including the port's `SITE_FOOT`, carries a `.site-updated` span filled by a small inline script from `document.lastModified`. GitHub Pages sends `Last-Modified` as the deploy time, so the date updates itself on every push. Nothing to stamp. Opened locally it shows the file's mtime.

### Design system: "pigment" (October 2026)
Warm primed paper, slate ink, and four pigments from the paintings, laid down as brush strokes. Everything below lives in `styles.css` unless noted.

**Colour tokens** (`:root`): `--paper` cream, `--key` slate ink, `--magenta`, `--turq` (and `--turq-ink` for text, `--turq-deep` for the footer), `--ultra` ultramarine, `--gold`. `--on-color` is the light type used on a pigment. The older names (`--accent`, `--accent-2`, `--accent-3`, `--bg-2`, `--rule`, `--ink-2`, `--ink-3`) still exist and are remapped onto these, so older page markup keeps working. `data-palette` and the tweaks panel no longer change anything visible.

**Type**: Bricolage Grotesque (display and body, condensed via `font-stretch`) and Spline Sans Mono for labels. Bricolage has no italic, so emphasis inside headings is an upright colour change. `--f-display` carries `!important` because `tweaks.jsx` writes an inline value at load.

**Brush strokes**: `--brush` and `--brush-dense` are SVG masks (displaced rectangle plus bristle streaks). Anything painted is a pigment background seen through one:
- `.stroke` — a word in a heading painted over. Set `--c` for the colour. Text stays ink until the stroke has painted in.
- `.paint` — any shape painted with `--c`. Used for the loose hero swatches, timeline bars, card swatches.

**Oil glazes** (the page background): large translucent pigment washes, brush-edged and blurred, behind sections. `.page-hero::before` drifts on an 18s loop. On home each section is targeted by `data-screen-label`; every other page cycles magenta, gold, turquoise, magenta-into-blue on `body:not(.home) > section:nth-of-type(…)`, alternating sides. Case studies and `.article` pages use fixed-size glazes kept to the margins.

**Page heroes**: the first section on a page gets `.page-hero` (entrance animation, drifting glaze, `.stroke` on the key phrase). Each top-level page has a body class that varies the hero while keeping the feel:

| Page | Body class | Glaze | Strokes |
|---|---|---|---|
| Home | `.home` | ultramarine | `.swatch-a/b/c` loose swatches |
| 404 | `.p-404` | gold into magenta | three roadmap-lane `.hs` strokes with a magenta strike through them |
| Work | `.p-work` | turquoise | five stacked `.hs` strokes, a project board |
| Claude | `.p-claude` | magenta | stepped `.hs` strokes, a file tree (`--ind` indent) |
| Art | `.p-art` | gold | angled `.hs` dabs, a palette |
| Connect | `.p-connect` | magenta into blue | two `.hs` strokes overlapping |
| Resources | `.p-resources` | turquoise | `.shelf` of `.spine` strokes |

`.hs` strokes are positioned inline with `--c`, `--x` (right), `--y` (top), `--w`, `--h`, `--r` (rotation). Every page's hero strokes sit inside one `<div class="hero-art">`, which covers the hero on desktop. Below 900px `.hero-art` is hidden: the painted key phrase and the glaze carry the hero on phones and tablets. (A band of scaled-down strokes under the hero text was tried and read as clutter.)

**Footer**: a `--turq-deep` field whose top edge is a `--brush-dense` stroke (`footer.foot::before`), with a magenta stroke (`::after`) and `.foot-gold` span laid over it. Every hand-authored footer includes `<span class="foot-gold">`.

**Motion** (`motion.js`, loaded on every hand-authored page): adds `.js` to `<html>`, paints `.paint` / `.stroke` and fades up `.rise` as they scroll into view, drifts `.drift` elements at different rates, counts up `.fact .n`. Reveal is position-based rather than IntersectionObserver so strokes still paint in hidden tabs and screenshot tools. All of it is off under `prefers-reduced-motion`.

**Guide chrome**: `SITE_CSS` in `port-to-site.py` mirrors the nav, fonts and turquoise brushed footer with `--s-*` tokens (including its own copy of the brush mask as `--s-brush`). Change the site nav or footer, change it there too, then re-port.

### Shell containers
- `.shell-wide` — full content width (most sections)
- `.shell` — standard content width (case studies, article body)
- `.shell-narrow` — narrow column (pull quotes, artist note)

### Section spacing
- `.pad-y` — large vertical padding `clamp(64px, 8vw, 112px)`
- `.pad-y-sm` — smaller `clamp(40px, 5vw, 64px)`

### Layout utilities
- `.cols-2` — two-column layout (used at top of case studies and most sections)
- `.gallery` — 12-column grid. Figure spans: default `span 6`, `.wide` = 8, `.narrow` = 4, `.full` = 12
- `.framed` — paper mat with an ink outline, used on the oil painting figures in art.html
- `.stats` / `.stat` — key number display (used in case study headers and index.html)
- `.chips` / `.chip` — small tag labels (used in case studies for status and topic)
- `.eyebrow` — small caps mono label above headings, with a magenta chip
- `.page-hero` — first section of a page; see the design system above
- `.case-index` — bordered index grid. Defaults to 5 columns (work page); `.two-up` and `.three-up` modifiers override for shorter lists
- `.lede` — larger intro paragraph

### Subpage path rule
All asset, CSS, script, and nav paths are root-relative (`/styles.css`, `/claude`, `/assets/...`). Do not use `../` prefixes; the clean-URL structure means a page at `/work/clubhouse/` is two levels deep and relative paths break.

---

## How to add a new case study

1. **Create `work/[slug].html`** — Copy an existing case file as a starting point. `destination-browse.html` (Case 05) is the cleanest template.

2. **Update the file:**
   - Change `data-palette`, title, meta description
   - Update eyebrow ("Case 06"), h2 title, chips
   - Replace stats and body paragraphs
   - Update prev/next `case-nav` links at the bottom
   - Update the previous case's `case-nav` to add a "Next" link pointing here

3. **Add to `work.html` case index** — Add a new `<li>` to `<ol class="case-index">` with the case number, title, and meta line.

4. **Add assets** — Create `assets/work/[slug]/` for any screenshots. Use `loading="lazy"` on all images.

### Case study HTML structure
```html
<section class="pad-y case-section" id="case-06">
  <div class="shell">
    <a class="back-link" href="../work.html">Back to Work</a>
    <div class="cols-2">
      <div>
        <div class="eyebrow">Case 06</div>
        <h2>Title.</h2>
        <div class="chips">...</div>
      </div>
      <div style="max-width: 64ch;">
        <div class="stats">...</div>
        <p class="lede">First paragraph...</p>
        <p>Second paragraph...</p>
      </div>
    </div>
  </div>
  <!-- gallery block if needed -->
</section>

<hr class="rule" />

<div class="shell" style="padding: 40px 0 64px;">
  <a class="back-link" href="../work.html">Back to Work</a>
  <nav class="case-nav">
    <a href="previous-case.html" class="case-nav-prev">← Previous: Previous Case Title</a>
    <a href="next-case.html" class="case-nav-next">Next: Next Case Title →</a>
  </nav>
</div>
```

---

## How to add a new top-level page

1. Copy `connect.html` (simplest page) as a starting point.
2. Update `<title>`, `<meta name="description">`. Give the first section `class="pad-y page-hero"`, add hero strokes (`.hs` or `.swatch-*`), paint the headline's key phrase with a `.stroke`, and keep the `<script src="/motion.js">` tag.
3. Add the page to the nav in **every** existing HTML file. The canonical nav is Home · Work · Claude · Resources · Art · Connect, identical on every page, inside `<div class="nav-links">`, and it appears in every page including `404.html` and the resource subpages. Claude 101 and the Playbook are the exception: their nav lives in their own `.sitebar` block and must be updated separately.
4. Update the footer links similarly.
5. No `../` prefix needed for top-level pages; subpages in `work/` and `resources/` already use `../` so will pick up the new link automatically once nav is updated in their files.

---

## Assets

```
assets/
  paintings/          Oil paintings (cropped, no wall visible)
    murals/           Mural photos
  work/               Product screenshots and case study images
    portal-home.png   Member Portal homepage screenshot
    browse/           Destination Browse prototype screenshots
    clubhouse/        The Clubhouse screenshots
    destination/      Destination page screenshots
    grocery/          Grocery redesign screenshots
    survey/           Post-trip survey screenshots
  photos/             Portrait and personal photos
```

Image conventions:
- All `<img>` tags use `loading="lazy"` except above-the-fold hero images
- Alt text is descriptive and specific — describe what's actually in the image
- Paintings in art.html use `class="framed"` on the figure element
