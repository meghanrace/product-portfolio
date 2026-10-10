# Home page content: changes made and proposals

Branch: `redesign-riso` (uncommitted). `_notes/` is underscore-prefixed, so Jekyll will not publish this file.

The design critic scored the home page 5, 6, 5.5, 6, 6.5, 6, 6, 6.5, 6, 6 and 6 over 11 rounds. Its asks converged on content, not layout: too many sections in the same rhythm, and the same facts restated in several places. Several rounds also contradicted each other (framed screenshot vs. unframed, painting in red vs. true colour, certifications as a list vs. one line), so not every note below is worth acting on.

---

## Part A. Copy already changed on this branch

These went in during the redesign without your sign-off. Nothing here is committed. The cleanest option is to restore all of it on `redesign-riso`, so the design branch keeps your original copy and every content decision moves to the separate content branch.

### Removed
| Where | What | Why it happened |
|---|---|---|
| Hero | The intro paragraph ("I came to product from twelve years on the front line...") | Dropped in a rebuild. Not a deliberate call; should come back. |
| Hero | Eyebrow "Meghan Race · Product Manager" | Redundant with the nav |
| About | Heading "I forged this path." | Critic: the "forged" line repeats three times on the page |
| About | Paragraph "At every job I've ever had..." | Critic: About was a wall of text |
| About | Paragraph "What I bring to product is unusual..." | Same |
| About | Caption "Meghan Race · Denver, CO" | The facts strip says Arvada, so the two conflicted |
| Stats | "12 yrs / In Member Services first" and "12 mo / Junior → PM" | Repeats the headline. Replaced (see Added) |
| What I do | "What I do now" label and "See the case studies →" link | Section restructured; case-study link moved to the portal screenshot |
| What I do | Numbers 01 to 05 as labels, trailing periods on the five statements | Styling, but it changes the text |
| Claude | "The differentiator" label, the three cards (setup, workflow, teaching) and their copy | Third card duplicated the Resources section |
| Resources | "Resources I've made" label, "Teaching is part of the practice." heading and its paragraph, the per-guide labels ("Handbook · start here" etc.), "Read ..." links, "All four guides →" | Section rebuilt as a contents list; guide blurbs shortened |
| Certifications | "Credentials" label and the paragraph "I taught myself product the way I taught myself oil painting..." | Section merged into the record |
| Experience | "Experience" label, heading "From Member Services to owning the platform.", its intro paragraph, "the trajectory shift", "Vail & Beaver Creek, CO" | Replaced by the timeline chart |
| Closing | "I forged my way into product, and I'm thriving here." and both closing paragraphs | Critic: weakest line on the page, and repeats About |

### Added or rewritten
| Where | New copy | Note |
|---|---|---|
| Hero | Facts reworded: "Product Manager, Exclusive Resorts / In the role since Jan 2025 / Arvada, Colorado" | Was "Exclusive Resorts · since 2012" etc. |
| Stats | "2 wk / Release cadence" | New stat, taken from your "bi-weekly major releases" line |
| Stats | "Platform owned", "Trips a year", "25K" (was "~25K") | Shortened; dropping the tilde makes the number less precise than it was |
| Portal | Screenshot callouts: "Search & Book. The booking flow, which I own end to end." / "My Trips. Trip planning and the pre-arrival workflows." / "The Clubhouse. Member community, led from zero to beta." | Written by me from the case studies. Check accuracy, especially "led from zero to beta" |
| About | "Today that's the Member Portal at Exclusive Resorts, a members-only luxury travel club: the $200M+ digital surface..." | Your "PM at Exclusive Resorts" paragraph, reworded |
| What I do | Heading "What owning it means" | Replaces "PM at Exclusive Resorts." |
| Claude | Link "How it's set up"; a CLAUDE.md excerpt quoting your working conventions and voice rules | Excerpt is real text from your CLAUDE.md. Check you're happy publishing it |
| Resources | "Guides / Four, written to be handed on. Two for anyone, two for PMs." and shorter blurbs | My wording |
| Experience | Heading "From the phone to the platform"; band labels "On the phone" / "On the platform"; role renamed "Portal stakeholder, Member Services"; "Regional Manager, Northeast" | Shortened role titles to fit the chart |
| Art | "I still paint, and I paint walls." | My wording. The painting band is new to the home page |
| Closing | Headline is now your sentence "I'd rather have the conversation than the email thread."; CTA "Let's connect →" | Promoted from body copy |

---

## Part B. Proposals for the content branch

Ranked by how often the critic raised them and how much they would move the score.

1. **Say "twelve years" once.** It's in the hero headline, the hero intro, the About lede, statement 04 and the closing paragraph. Keep the headline; rephrase the others around what changed, not the duration.
2. **Cut the five statements to three.** Rounds 7 to 10 flagged five identical "I ..." rows as templated. Suggested keep: roadmap ownership, technical investigation, cadence (it has the only hard number). Fold "challenge solutions" into roadmap, and "customer evidence" into the About section.
3. **Move certifications off the home page.** Rounds 4, 8 and 10 read the six-cert list as résumé padding directly after "Now I own the platform." Options: a line on /connect, a block on /work, or one sentence in About ("six certifications in eighteen months, including AWS and Salesforce").
4. **Fold education into the timeline.** Add a Colby row to the chart (I don't have your years; you'd need to supply them) and drop the separate block. The painting stays as the link to /art.
5. **Give the Claude section one sentence, not a paragraph.** The 5:36 Confluence detail is the best line; lead with it.
6. **Add a qualifier under each stat** ("Booking, trips, Clubhouse" under $200M+). The labels read as generic.
7. **Restate the closing.** The critic called "I forged my way into product, and I'm thriving here" the weakest sentence on the page. Your own "I'd rather have the conversation than the email thread" now leads, and it works.
8. **Fewer sections.** Round 10 suggested six: hero, proof (stats and portal), how I work, Claude, the timeline, contact. The page currently has nine.

## Suggested order

1. On `redesign-riso`: restore Part A copy so the branch is design-only, review, commit.
2. New branch `content-pass` off it: work through Part B with you, one section at a time.
