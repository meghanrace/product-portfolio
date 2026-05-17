# Claude Code for PMs — Setup & Workflow Guide

*How to set up Claude Code as a true work assistant — not just a chatbot, but a tool that knows your projects, your writing style, and your tools.*

> **Who this is for:** Product Managers (and anyone in a non-engineering role) who want to use Claude Code to draft tickets, release notes, exec updates, research synthesis, and one-off investigations — without learning to write code or live in Terminal.

---

## 📋 Part 1: High-Level Overview — What You Can Use Claude Code For

Claude Code is a tool from Anthropic that runs locally on your computer, has access to your files, and can use connectors (called MCPs — Model Context Protocol) to talk to systems like Jira, Confluence, your codebase host (Bitbucket, GitHub, GitLab), your CMS, your data warehouse, and more. Once you set it up well, it stops being "an AI chat" and starts being "a teammate that already knows the project, the team, and how you write."

> ✅ **Use the Claude desktop app, not the terminal.** Developers typically run Claude Code from a CLI like Terminal or iTerm, and that's a perfectly valid setup. What's nice about the desktop app is that you can easily switch between **Code** (file-aware work — drafting docs, reading repos), **Cowork** (longer-running automated tasks), and **Chat** (quick questions, brainstorming) all in the same window. You'll only need Terminal in rare cases for a specific command.

### Concrete examples of what a PM can do with it

| Task | How it works |
|------|--------------|
| **Draft a Jira ticket (or any work ticket)** | "Draft a feature ticket for [X]." Claude reads your context files, follows your ticket format, generates HTML you paste into Jira. |
| **Draft release notes** | "Draft release notes for the [date] release based on these tickets." Claude pulls tickets via the Jira MCP, follows your release-notes style rules, produces a ready-to-paste draft. |
| **Write an exec update or recap email** | "Draft the exec recap for the last three releases for our leadership team." Claude follows your exec-voice style rules (different tone, length, and structure than internal docs). |
| **Investigate a question or pull data** | "How many users did [X] in the last 30 days?" If you've set up the right connectors, Claude can run a query against your data warehouse and return results. |
| **Research synthesis** | "Synthesize themes from these 12 user interview notes in `research/active/[topic]/`." Claude reads the files and produces a themed write-up. |
| **Survey or feedback analysis** | "Analyze this week's survey responses and flag anything new compared to last week." Claude reads the data files and writes an analysis doc. |

None of this works well out of the box. The reason it works well over time is the setup described below.

---

## 🔧 Part 2: One-Time Setup

### 2.1 Install Claude Code

**Recommended: download the Claude desktop app** from [claude.ai/download](https://claude.ai/download). Sign in with your Anthropic account. The desktop app gives you Code, Cowork, and Chat in one place, which is what most PMs will use 95% of the time.

If you're more technical or want to run Claude Code from a CLI:

1. Install Node.js from [nodejs.org](https://nodejs.org) if you don't have it.
2. Install via npm: `npm install -g @anthropic-ai/claude-code`
3. Run `claude` in Terminal — it'll walk you through signing in.

You can also install the VS Code or Cursor extension if you want an in-editor chat panel.

### 2.2 Create a single project folder for all your work

Keep **everything** in one folder. That way Claude Code has one consistent working directory and one set of instructions to follow. Here's a structure that works well for PM work:

```
Claude projects/
├── CLAUDE.md                    ← The "system prompt" Claude reads on every session
├── .env                         ← API keys (NEVER commit this)
├── .gitignore                   ← Excludes .env from version control
├── context/                     ← Reference docs Claude reads before drafting
│   ├── ticket-guidelines.md
│   ├── formatting-strategy.md
│   ├── product-architecture.md
│   ├── team-directory.md
│   ├── research-playbook.md
│   └── api-key-authentication-guide.md
├── ticket-templates/            ← HTML templates (bug, feature)
├── tickets/                     ← Finished tickets (paste into Jira)
├── release-notes-drafts/        ← Confluence / doc drafts
├── trackers/                    ← Live working docs (stakeholder tracker, etc.)
├── comms/                       ← Email drafts and outbound communications
├── research/
│   ├── active/                  ← In-flight initiatives
│   └── archived/
├── data/                        ← Survey data, exports, analyses
├── archive/                     ← Older stuff out of the way
└── repos/                       ← Local clones of your team's code repos
```

> ✅ **Why this matters:** Claude reads the file tree as part of its context. A clean, predictable folder structure means it finds the right reference file every time without you having to point at it.

### 2.3 Create the `.env` file (API keys)

The `.env` file lives at the root of your project folder and holds the API tokens Claude needs to talk to external systems (your ticketing tool, docs platform, code repo host, etc.). It is excluded from git via `.gitignore` — **never commit it, never paste its contents anywhere.**

#### Step 1: Get the API tokens from each service yourself

You don't need to ask IT for these — every modern SaaS tool has a self-serve "generate an API token" page in user settings. Get the tokens first, then bring them back to Claude. Common ones for a PM:

| Service | Where to get the token |
|---------|------------------------|
| **Jira** (Atlassian) | Go to [id.atlassian.com → Security → API tokens](https://id.atlassian.com/manage-profile/security/api-tokens). Click "Create API token," give it a label like "Claude Code - Jira," copy the value immediately (you can't see it again). |
| **Confluence** (Atlassian) | Same page as Jira — [id.atlassian.com → Security → API tokens](https://id.atlassian.com/manage-profile/security/api-tokens). Create a **separate** token labeled "Claude Code - Confluence." Even though both are Atlassian products, you typically use two distinct tokens. |
| **Bitbucket** (or other code repo) | In Bitbucket, click your profile picture → **Personal settings** → **App passwords** → **Create app password**. Check the read/write scopes for repositories and pull requests. Copy the value. *GitHub equivalent: Settings → Developer settings → Personal access tokens. GitLab equivalent: User Settings → Access Tokens.* |
| **Other tools** (CMS, analytics, search, etc.) | Look under Settings → API or Developer in any modern SaaS app. Most will have a self-serve "generate API key" button under your profile or workspace settings. |

> ⚠️ **The pattern is the same everywhere:** Profile → Settings → API tokens / App passwords / Developer → Create new → Copy and save somewhere safe. If you can't find it, your tool's docs will have a "creating an API token" page — search for that phrase.

#### Step 2: Ask Claude to create the `.env` file and `.gitignore`

Once you have the tokens, you don't need to open Terminal. Just paste a prompt like this into the Claude desktop app:

> "Please create a `.env` file in the root of my project folder with placeholder entries for these keys: `JIRA_API_KEY`, `CONFLUENCE_API_KEY`, `BITBUCKET_API_KEY`, [plus any others you have]. Also create a `.gitignore` file that excludes `.env` so the keys never get committed."

Claude will:

- Create `.env` at the root of your project folder with empty placeholder values
- Create `.gitignore` with `.env` excluded (plus `.env.local` and `.env.*.local` for good measure)

#### Step 3: Ask Claude to open the `.env` file so you can paste in your keys

The `.env` file now exists but is empty. To fill it in, ask Claude to open it for you:

> "Please open the `.env` file so I can paste in my API keys."

The file will open in your default editor. Paste your real values in after each `=` sign — no quotes, no spaces around the `=` — then save and close. Done.

> ⚠️ **If you need access to a data warehouse** (Salesforce, Snowflake, BigQuery, an internal SQL database) — most PMs don't, but if you do, those require different credentials and a slightly different setup. Ask your tech lead for connection details.

### 2.4 Create your `CLAUDE.md` file

This is the single most important file. CLAUDE.md sits at the root of your project folder, and Claude Code reads it **at the start of every conversation**. Think of it as the standing instructions you'd give a new contractor on day one.

A good CLAUDE.md typically has six sections:

1. **Project Overview** — One paragraph: what this workspace is for and what kinds of work you do here.
2. **Folder Structure** — Your folder tree with one-line descriptions of what each folder is for. This is what tells Claude where to find things.
3. **Preferences** — How you want Claude to communicate. E.g. "Provide detailed explanations of reasoning and tradeoffs," "Present options with pros/cons before proceeding," "Ask clarifying questions if a request is ambiguous."
4. **Code Style** (if relevant) — Conventions like "clean code, meaningful names, simple over clever."
5. **Workflow** — How you want it to operate ("Read existing context files before drafting," "Always save outputs to the right subfolder").
6. **API Keys / Integrations note** — Note that keys live in `.env` and must never be exposed in code, logs, or documentation.

The easiest way to build yours is to **ask Claude to help you create it**. A prompt like:

> "Help me create a CLAUDE.md file at the root of my project folder. Use these six sections as a reference structure: (1) Project Overview, (2) Folder Structure, (3) Preferences for how I want you to communicate, (4) Code Style, (5) Workflow, (6) API Keys note. Ask me questions about my role, what kinds of work I do, and how I like to receive information, then draft the file based on my answers."

> ✅ **Iterate on it.** Whenever you notice Claude doing something the wrong way twice, add a line to CLAUDE.md (or just tell Claude "please update CLAUDE.md to remember that..."). Over time the file becomes a precise mirror of how you actually work.

### 2.5 Set up your `context/` reference files

The `context/` folder is where the magic happens. These are markdown files that capture the institutional knowledge Claude needs to do high-quality work — the stuff you would brief a new hire on. Examples of files worth creating:

| File | What's in it |
|------|--------------|
| `ticket-guidelines.md` | Your ticket structure, writing principles (business-perspective vs. technical-implementation), word counts, section order, naming and capitalization rules |
| `formatting-strategy.md` | How to format output for the tools you use — e.g., HTML for Jira Cloud (since markdown doesn't paste cleanly), markdown for GitHub issues, etc. |
| `product-architecture.md` | Product and tech architecture reference — integrations, key flows, terminology your team uses |
| `team-directory.md` | Who owns what, contact list, reporting lines |
| `research-playbook.md` | Methodology for research synthesis — interview frameworks, theme extraction |
| `release-notes-style.md` | Your house style for release notes — voice, structure, audience-specific rules |
| `exec-comms-style.md` | Style rules for exec-facing communications — length, tone, what to include/exclude |

These files capturing your **voice** and **style** are what make the output sound like *you*, not generic AI prose.

> ⚠️ **How to build yours:** Don't try to write all of these on day one. Start with one — a team directory or a product-architecture doc you might already have — and add more as you notice Claude missing context. After a few weeks you'll have a library.

### 2.6 Clone your team's code repos locally (optional but powerful)

If you want Claude to read actual code (debugging, "where does this logic live", "explain how X works"), you'll want your team's repos cloned into your `repos/` folder.

**Good news: you don't need to run git commands yourself.** Once your code-repo API key is in `.env`, you can just tell Claude in plain English what you want and it'll handle the cloning for you.

A prompt like:

> "Please clone the following repos into my `repos/` folder: [repo-1], [repo-2], [repo-3]. Use my Bitbucket API key from `.env`."

To get the latest code later, just say: *"Pull the latest changes for [repo-name]."*

> ✅ **You probably don't need every repo on day one.** Start with the 2-3 repos most relevant to what you work on. Add more as needed. Cloning everything is rarely helpful and just adds noise to Claude's context.

Once they're cloned, Claude can answer questions like: *"How does the password reset email get triggered?"* or *"Where is the logic that determines whether a user sees feature X?"* — by reading the code directly.

### 2.7 Connect MCPs (Jira, Confluence, your code repo, etc.)

MCP = Model Context Protocol. These are connectors that let Claude Code talk to external services. Once configured, Claude can read tickets, fetch docs, comment on PRs, query your CMS — all without you copy-pasting.

To add one, ask Claude in the desktop app: *"Help me add the [tool] MCP connector."* It'll walk you through it. Or you can manage them under Settings → Connectors in the desktop app. Common ones for a PM:

| MCP | What it does |
|-----|--------------|
| **Atlassian (Jira + Confluence)** | Read tickets, search Jira with JQL, fetch Confluence pages, post comments, create pages |
| **Bitbucket / GitHub / GitLab** | Read PRs, comment on PRs, open new PRs, list branches |
| **Your CMS** (Contentful, Hygraph, Sanity, etc.) | Query content via GraphQL or REST |
| **Figma** | Pull design context for tickets and handoff specs |
| **Your data warehouse** (Snowflake, BigQuery, Postgres, etc.) | Query data directly with SQL |

The Atlassian and Bitbucket MCPs use OAuth — the first time you use them, a browser window will open to confirm access. After that, they just work.

> ✅ **Start small.** Just adding the Atlassian MCP unlocks 80% of the value for a PM. Get that one working before adding others.

---

## 📝 Part 3: How You'd Actually Use Claude Code Day-to-Day

The setup above is the boring part. Here's what the daily workflow looks like once it's done.

### 3.1 Writing a ticket

**What you type:**

> "Draft a feature ticket for adding a [new feature] to [product area]. The goal is to [business outcome]."

**What Claude does:**

1. Reads your `context/ticket-guidelines.md` for structure and tone.
2. Reads `context/formatting-strategy.md` — outputs the right format for your tool.
3. Reads `context/product-architecture.md` for product context.
4. Uses your `ticket-templates/` file as a skeleton.
5. Writes the ticket, saves it to `tickets/[ticket-name].html`.

**What you do:** Open the file, copy, paste into your ticketing tool. Done.

### 3.2 Drafting release notes

**What you type:**

> "Pull the tickets in the [date] release and draft release notes for Confluence."

**What Claude does:** Queries Jira via the Atlassian MCP for that release, groups tickets by Features / Improvements / Bug Fixes, applies your style rules, saves a draft to `release-notes-drafts/`.

### 3.3 Drafting an exec update or recap

**What you type:**

> "Draft the exec recap email for our leadership covering the last three releases."

**What Claude does:** Follows your exec-voice style file (shorter, no bug fixes, business-outcome framing), produces a draft tailored to executives — different voice than the internal release notes.

### 3.4 Querying data

**What you type:**

> "How many users completed [action] in [time period]? Use the data warehouse connector."

**What Claude does:** Writes a SQL query against the right table, returns the count plus a sample. (Requires the data warehouse MCP and credentials to be set up.)

### 3.5 Research synthesis

**What you type:**

> "Read the interview notes in `research/active/[topic]/` and synthesize themes following the research playbook."

**What Claude does:** Reads `context/research-playbook.md`, reads all interview files, extracts themes weighted by frequency and impact, produces a synthesis doc.

---

## 💡 Part 4: Tips & Things to Learn Up Front

- **Treat CLAUDE.md as a living doc.** Every time Claude does something wrong twice, add a line. Every time it nails something non-obvious, capture the rule.
- **The context/ files are the secret sauce.** Generic AI output is generic because there's no context. Feed Claude your product docs, your style rules, your team directory — output quality jumps.
- **Match output format to where it's going.** Jira Cloud's editor doesn't paste markdown cleanly — use HTML. GitHub uses markdown. Confluence accepts both HTML and rich-paste from a browser. Set this expectation once in a `formatting-strategy.md` file and Claude will follow it forever.
- **Never commit `.env`.** Double-check your `.gitignore` includes it before your first commit.
- **Start with one MCP.** Don't try to set up everything at once. Get one workflow working end-to-end, then expand.
- **Be specific in prompts.** "Draft release notes" is OK. "Draft release notes for the [date] release using my Confluence style rules, grouped Features / Improvements / Bug Fixes" is great.
- **Ask Claude to explain its reasoning.** Especially when output doesn't feel right — "Why did you frame this as an Improvement instead of a Feature?" Surfaces the logic and helps you refine the rules.
- **Memory persists across sessions.** Claude Code can remember facts you tell it ("remember that exec recaps never use em dashes") for future sessions.

---

## 🚀 Part 5: Suggested Onboarding Path

1. **Day 1:** Install the Claude desktop app, create your project folder, ask Claude to help you create CLAUDE.md, `.env`, and `.gitignore`.
2. **Day 2:** Connect the Atlassian MCP. Try drafting one ticket and one release-note draft.
3. **Week 1:** Create 2-3 starter `context/` files (team directory, ticket guidelines, formatting strategy). Try a research synthesis task.
4. **Week 2:** Clone the 2-3 code repos most relevant to your work, if you want Claude to read code.
5. **Ongoing:** Every Friday, scan your week's Claude conversations. Anything Claude got wrong twice → CLAUDE.md. Any new institutional knowledge → a new `context/` file.

---

*The investment in setup pays back within the first week. The longer you use it, the better it gets — because the context files and CLAUDE.md keep growing into a precise mirror of how you and your team actually work.*
