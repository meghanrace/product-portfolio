# How I Use Cowork — A Practical Guide for the Team

## What Is Cowork?

Cowork is a mode within the Claude desktop app that turns Claude from a chat assistant into something closer to a digital coworker. It can read and create files on your computer, run code, connect to tools like Jira and Confluence, and follow customized playbooks ("skills") for recurring work. Think of it as giving Claude the ability to actually *do things* — not just answer questions.

This guide walks through how I (Meghan) have set mine up, what it does for me day-to-day, and how you could build something similar for your own work.

---

## The Quick Concepts

Before diving into specifics, here are the four things you'll configure:

**Connectors** link Claude to your tools (Jira, Confluence, Figma, Salesforce data, etc.) so it can read and write real data. This is the foundation — without connectors, Claude is just working with whatever you paste into the chat.

**Scheduled Tasks** are automated jobs that run on a timer. Claude wakes up, does the work, and publishes the result — no interaction needed. This is where the biggest time savings come from.

**Skills** are detailed instruction sets that tell Claude exactly how to do a specific type of task — what format to use, what sections to include, where to publish, etc. These can be built-in or custom-made.

**Plugins** are bundles of skills you install from a marketplace. They cover broad areas like product management, engineering, or design.

---

## What Cowork Actually Does for Me

My setup is centered around two automated pipelines and a set of ad-hoc workflows. Here's the honest breakdown of where the time savings are.

### The Two Workhorses

**1. Automated Meeting Summarizer (runs every weekday at 5:36 PM)**

This is the single most valuable thing in my setup. Every afternoon, Claude scans my local Zoom transcripts folder for new meetings recorded that day. For each new meeting, it reads the transcript, writes a structured summary, and publishes it as a Confluence page under the correct parent page — all without me touching anything.

What makes it genuinely useful (and not just a generic summary tool) is that it applies different formats depending on the meeting type:

- **Engineering All-Hands** → grouped by themes, includes key quotes from participants, decisions vs. open items clearly separated. Published to the ETR Confluence space under "2026 Engineering Meeting Notes."
- **Member Interviews** → structured around the member's background, pain points with signal strength ratings (Strong/Moderate/Emerging), and direct quotes. Published under "Member Interviews" in the TSV space.
- **Tech Talks** → organized by topics covered, Q&A highlights, and resources mentioned. Published under "Tech Talk - Weekly Training Recordings."
- **All other meetings** → a general format with a High-Level Overview (quick-scan bullet points), Key Outcomes, Decisions Made, dynamic topic sections based on content, Pending Confirmation, Action Items grouped by person, and Next Steps.

It tracks what it's already processed via a JSON file so it doesn't re-summarize old meetings. If there are multiple sessions of the same meeting on the same day (reconnects, etc.), it groups them into one summary.

This format has evolved over time. I've updated it at least four times — adding the interview format, adding tech talk routing, switching action items from flat tables to grouped-by-person, adding the High-Level Overview section. The key point is that **you keep refining the instructions as you learn what works.** You don't have to get it perfect on day one.

**2. Weekly Survey Analysis Pipeline (Monday mornings)**

This is a multi-step chain that processes member satisfaction survey data from Salesforce and produces both a Confluence report and an Excel spreadsheet. It runs in stages:

- **9:00 AM** — Claude sends me a reminder to run the Salesforce data export command (it can't access SF directly, so this is a manual step — I run one terminal command and then Claude takes over).
- **9:35 AM** — The analysis task kicks off. It reads the fresh JSON data, calculates satisfaction distributions, booking ease ratings, theme analysis (13 keyword categories like "Mobile App Issues," "Availability/Date Competition," "Navigation/Usability"), identifies top quotes per theme, and ranks members open to follow-up by dissatisfaction level.
- It then launches two parallel workers: one builds a formatted Excel spreadsheet with a Dashboard sheet (charts, formulas, color-coded), a Follow-Up Members sheet (linked to Salesforce contacts), and an All Responses sheet. The other updates a specific Confluence page with the executive summary, rating tables, theme breakdowns with member quotes, and a follow-up member list — while preserving any "Eng Plan to Address" or "Jira Tickets" content that the engineering team may have manually added.
- Finally, it reminds me to copy the spreadsheet to OneDrive for sharing.

There's also a **comprehensive version** (currently paused) that analyzes ALL survey question areas — not just app/portal — across 8 topic areas using 8 parallel workers (overall membership, sales, ambassadors, onsite experience, residences, booking/availability, app/portal, travel preferences). Each worker does independent theme analysis and the results get assembled into a full Confluence page.

### Ad-Hoc Work (Where I Spend Interactive Time)

Beyond the automations, I use Cowork sessions for project management synthesis work. Some real examples:

- **Synthesizing multiple meeting notes into stakeholder communications.** For a Travel Desk transition project, I had Claude read 5 different meeting summaries from Confluence, then draft a "here's what I understand to be true" status update with decisions needed and action items by owner — iterating on tone and length until it was right for a broad audience.

- **Building and maintaining project trackers.** For design work with Anna, I had Claude pull context from Confluence PRDs and meeting notes to build a Design Work in Progress document tracking status, design vs. dev timelines, and stakeholders — eventually landing on a lean markdown format for Confluence rather than a long Word doc.

- **Confluence page management.** Updating roadmap docs, writing epic descriptions for Jira, updating destination page documentation, organizing to-do lists.

- **Preparing for leadership meetings.** Pulling relevant context from Confluence and prior meeting notes to build a focused agenda or talking points.

- **Data investigation.** When survey report numbers didn't match expectations, I had Claude dig into the data to find the discrepancy.

The common thread: **most of my interactive sessions involve Claude reading from Confluence, synthesizing across multiple sources, and producing a deliverable** — usually another Confluence page, a markdown doc, or a Word document that I'll share with stakeholders.

---

## The Infrastructure That Makes It Work

### Connectors

**Atlassian (Jira + Confluence)** — This is by far the most important connector. Almost everything in my workflow either reads from or writes to Confluence. Meeting summaries get published there. Survey analyses get published there. Project trackers live there. Without this connector, about 80% of what I use Cowork for wouldn't work.

**Figma** — Useful for pulling design context when reviewing work with the design team. Claude can take screenshots of specific frames, browse component libraries, and pull metadata.

Both of these were set up at the org level — I didn't have to configure them myself. If you're getting started with Cowork and don't see these connectors, check with your admin. There are also a few other utility connectors available at the org level (Mermaid for diagrams, a docs library, AWS Marketplace) that you may see in your setup.

### Scheduled Tasks

| Task | Schedule | What It Does |
|------|----------|-------------|
| Meeting Summarizer | Weekdays 5:36 PM | Scans Zoom transcripts, summarizes, publishes to Confluence |
| Survey Data Pull Reminder | Mondays 9:00 AM | Reminds me to run the SF export command |
| Full Survey Data Pull Reminder | Mondays 9:08 AM | Reminds me to run the full-field SF export |
| Weekly Survey Refresh | Mondays 9:35 AM | Analyzes app/portal survey data, builds spreadsheet, updates Confluence |
| Weekly Full Survey Analysis | Mondays 10:35 AM | Comprehensive 8-topic analysis (currently paused) |

### Plugins Installed

I have seven plugins installed but use them unevenly. Here's the honest breakdown:

**Heavily used:** Product Management (the only plugin I installed myself — specs, roadmaps, stakeholder updates)

**Moderately used:** Design (design critique, handoff specs — useful when working with Anna), Engineering (code review, architecture discussions), PDF Viewer (contract review, form filling)

**Installed but lighter use:** Brand Voice (have it for content consistency — useful if you're writing external-facing content), Zoom (developer-oriented — relevant if you're building Zoom integrations), Cowork Plugin Management (meta-tool for creating/customizing plugins)

### Built-in Skills I Actually Use

**Document creation (docx, xlsx)** — Excel spreadsheets for survey analysis, Word docs for stakeholder communications when markdown won't cut it.

**Schedule** — This is how I set up the automated tasks above.

**Internal Comms (custom skill)** — Templates for 3P updates, company newsletters, FAQ roundups, and general comms. Each template defines the exact format, tone, length, and data sources. This is a custom skill I built, not something from a plugin.

**Skill Creator** — Used to build and refine the Internal Comms skill and other custom workflows.

---

## How to Build Your Own Setup

### Start Here (Day 1)

1. **Install the Claude desktop app** and open Cowork mode.
2. **Check your connectors.** Atlassian (Jira + Confluence) and Figma are set up at the org level, so you should already have them. If you don't see them, check with your admin.
3. **Set your user preferences.** In Settings, add a few sentences about how you want Claude to work with you. Mine are:
   - Ask clarifying questions before providing answers to avoid making inaccurate assumptions
   - Recognize that I may not know all the details of our tech stack
   - Be clear, concise, well-formatted, professional
   - Occasional emojis are okay

### Build Your First Automation (Week 1)

Think about what you do repeatedly that follows a predictable pattern. Good candidates:

- **Meeting notes** — If you record meetings in Zoom, you can set up a meeting summarizer similar to mine. The key is defining the format you want (what sections, how action items should be structured, where to publish).
- **Weekly reports** — Any report that pulls from the same data sources every week and publishes to the same place.
- **Data processing** — If you regularly export data, analyze it, and share results.

To create a scheduled task, tell Claude: "I want to set up a scheduled task that [does X] every [when]." It'll walk you through defining the instructions and setting the cron schedule.

### Refine Over Time

The most important thing I've learned: **your automations will not be perfect on the first try, and that's fine.** My meeting summarizer has gone through at least four major revisions. I added the interview format when I realized those meetings needed a different structure. I switched to grouped action items after flat tables proved hard to scan. I added the High-Level Overview section after feedback that summaries needed a quicker entry point.

Each time, I just opened a new session and said something like "Update the meeting summarizer to group action items by person instead of using a flat table" — and Claude updated the scheduled task instructions.

### What To Do for Your Role

**If you're in Product/PM:** Install the Product Management plugin. You already have the Atlassian and Figma connectors at the org level. Set up meeting note automation first. Then build a custom skill for whatever recurring communications your team does (status updates, sprint reviews, stakeholder emails).

**If you're in Engineering:** The Engineering plugin has useful skills for code review, architecture decisions, and incident response. The Atlassian connector (already available) lets Claude read and update Jira tickets directly.

**If you're in Design:** You already have Figma connected. Add the Design plugin for critique, accessibility audits, and handoff spec generation. Useful for getting a structured second opinion on a design.

**If you're in Ops/Member Services:** The Atlassian connector is already available for Confluence-based documentation. Focus on building custom skills for whatever recurring reports or communications you produce.

---

## Tips From ~80 Sessions of Use

- **Confluence is the hub.** Almost everything I do starts or ends in Confluence. The good news is that the Atlassian connector is already set up at the org level, so you should have it from day one.
- **Scheduled tasks are the highest ROI.** The meeting summarizer alone saves me 30+ minutes per day of note-taking and formatting. It runs automatically — I just review the output occasionally and refine the instructions when needed.
- **Custom formats matter more than fancy plugins.** The most valuable thing in my setup isn't a plugin — it's the specific instructions I've written for how meeting notes should be structured, what sections a survey analysis should have, and how action items should be grouped. Start with format, not features.
- **Iterate in small batches.** Don't try to build the perfect automation on day one. Get a basic version working, use it for a week, then refine based on what bothers you.
- **Claude is good at synthesis.** Its sweet spot is reading multiple sources (meeting notes, Confluence pages, data exports) and producing a coherent summary or communication. Lean into that.
- **Be specific about where things should go.** When setting up Confluence publishing, specify exact parent page IDs and space keys. Claude can look these up, but being explicit avoids pages ending up in the wrong place.
- **The SF data export is my one manual step.** Claude can't access Salesforce directly, so I have a reminder task that tells me to run a terminal command before the analysis task kicks off. It's a small friction point but worth it for the analysis automation that follows.
