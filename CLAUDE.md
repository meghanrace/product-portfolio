# meghanrace-site — Claude context

Personal portfolio site for Meghan Race, PM at Exclusive Resorts. Static HTML/CSS, no build step, no framework. Edited via Claude Code.

---

## Site map

| File | Page | Purpose |
|------|------|---------|
| `index.html` | Home | Hero, about, stats strip |
| `work.html` | Work index | Case study index + portal screenshot |
| `claude.html` | Claude | How I use Claude Code day-to-day |
| `art.html` | Art | Mural sections + oil paintings gallery |
| `connect.html` | Connect | Contact page |
| `work/grocery-redesign.html` | Case 01 | Grocery ordering redesign |
| `work/post-trip-survey.html` | Case 02 | Post-trip survey platform |
| `work/clubhouse.html` | Case 03 | The Clubhouse |
| `work/destination-page.html` | Case 04 | Destination page reimagined |
| `work/destination-browse.html` | Case 05 | Destination Browse |
| `resources/cowork-for-pms.html` | Resource | Cowork/Claude guide for PMs |

---

## Key copy locations

### index.html
- **Hero h1** — "Twelve years on the phone. / Now I own the platform." Near top of body.
- **Home facts strip** — `.home-facts` div: location, company/tenure, title/tenure.
- **About section** — 4 paragraphs inside `data-screen-label="03 About"`. This is the main biographical copy. The lede paragraph starts "Twenty years in hospitality..."
- **Stats strip** — Numbers (12 yrs, Jan 2025, etc.) in the `data-screen-label="04 Stats"` section below About.

### work.html
- **Hero lede** — `.lede` paragraph under the h1. Describes the Member Portal and five case studies.
- **Case index** — `<ol class="case-index">` with five list items linking to subpages. Update here when adding/removing cases.
- **Portal screenshot caption** — figcaption under `assets/work/portal-home.png`.

### claude.html
- **Hero lede** — The main paragraph describing how Claude Code changed what a PM can own.
- **Setup details, example sessions, etc.** — Body sections below the hr.

### art.html
- **Hero lede** — Studio intro paragraph.
- **Mural body copy** — Inside `.mural-body` div in the aspen stairwell section.
- **Oil paintings lede** — Under "From the studio years." heading — describes landscapes + fabric series.
- **Artist note** — `data-screen-label` not set; the pull quote + two paragraphs near the bottom.

### Case study subpages (work/*.html)
Each has a cols-2 layout at the top:
- Left column: eyebrow ("Case 01"), h2 title, chips
- Right column: stats div + 2–3 lede/body paragraphs
The body paragraphs are the main case study copy.

---

## Voice and style rules

Universal rules (no em-dashes, concrete language, forward-facing tone, no trailing summaries, etc.) now live in the root `CLAUDE.md` one level up and apply here too. Nothing site-specific to add beyond that currently.

---

## Tech and CSS conventions

### Palette
All pages use `data-palette="marsh"` on the `<html>` element. The palette can be changed via the tweaks panel (React/Babel CDN at bottom of each page). Palette-aware CSS variables:
- `--accent` — golden amber
- `--accent-2` — rust/terra cotta (used for active nav, pull-quote accents, chips)
- `--accent-3` — sage green
- `--bg-2` — slightly darker background (used for alternating sections)
- `--ink-2`, `--ink-3` — secondary/tertiary text
- `--rule` — border/divider color
- `--f-display` — display typeface
- `--f-mono` — monospace typeface

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
- `.framed` — warm gold border (`#c4a97a`) + shadow, used on the oil painting figures in art.html
- `.stats` / `.stat` — key number display (used in case study headers and index.html)
- `.chips` / `.chip` — small tag labels (used in case studies for status and topic)
- `.eyebrow` — small caps mono label above headings
- `.lede` — larger intro paragraph

### Subpage path rule
Pages in `work/` and `resources/` must use `../` prefix for all asset, CSS, and script paths. Nav links also use `../index.html`, `../work.html`, etc.

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
2. Update `<title>`, `<meta name="description">`, `data-palette` if different.
3. Add the page to the nav in **every** existing HTML file — the nav appears in: `index.html`, `work.html`, `claude.html`, `art.html`, `connect.html`, and all files in `work/` and `resources/`.
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
