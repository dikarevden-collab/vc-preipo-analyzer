---
name: vc-preipo-analyzer
description: >
  Structured due diligence and investment memo for private/pre-IPO companies.
  Use when user asks to analyze a company, evaluate an investment, run due
  diligence, build a comp table, or write an investment memo. Do NOT use for
  general market Q&A, public equity research, or research notes.
---

# VC / Pre-IPO Investment Analyzer

Structured due diligence framework for evaluating private company investments across financials, market positioning, valuation, comparable public multiples, and risk assessment.

## When to Use

- User asks to "analyze [Company]" or "evaluate [Company] as an investment"
- User provides a pitch deck, data room, or financials and wants a memo
- User asks to "run due diligence" or "build a comp table"
- User wants scenario analysis (bull/base/bear) or IRR/MOIC calculations
- User asks to compare secondary pricing across multiple private companies
- User says "investment memo", "investment case", or "deal evaluation"

## When NOT to Use

- General market Q&A ("What's the S&P 500 at?", "How are rates trending?")
- Quick price lookups or single-number questions
- Research notes or market commentary — use **research-note-generator** instead
- Financial modeling deep-dives without a specific company — use Anthropic's `creating-financial-models` skill
- Ratio analysis on public company financials — use `analyzing-financial-statements` skill

## Deal Intake Interview

Before starting research, collect deal-specific context the tool cannot find on its own. **Company name is the only required field** — all others are optional but significantly improve memo quality.

Present these questions to the user as a numbered list. Wait for answers before proceeding.

1. **Company name** *(required)*
2. **Materials** — "Do you have files to provide? Attach them or give a folder path (deck, data room, financials, cap table, website URL)"
3. **Deal terms** — Entry valuation, price per share, share class, deal structure (secondary / SPV / direct / primary co-invest)
4. **Investment horizon** — Quick flip (<1yr), medium-term (2-3yr), or hold-to-IPO (5yr+)?
5. **Target return** — MOIC floor or IRR minimum the deal must clear?
6. **Appeal to investors** — Who are the target LPs / co-investors? Has any pre-marketing been done? What's the reception so far?
7. **Why this company?** — Origination story. Why was it selected over alternatives? Who brought the deal?
8. **Specific concerns** — Any risks or questions you want pressure-tested?

**Smart skip logic:** [Low freedom — must follow]
- Parse the user's initial message for answers already provided (e.g., "analyze SpaceX at $350B, secondary, 3yr hold" → questions 1, 3, 4 are answered)
- Only ask questions whose answers are not yet known
- If user says "just run it" or "skip interview" → proceed with company name only, produce generic analysis
- After materials are ingested (PDFs, Excel), reassess which questions are already answered by the documents before asking remaining ones

## Sector Detection & Specialization

Automatically detect the company's sector and apply the relevant overlay from `references/sector-overlays.md`. **Read only the matching sector section** — do not load all overlays. If ambiguous, ask the user to confirm.

**Supported sectors:** SaaS / Cloud Software, Fintech, Medtech / Biotech, AI / ML, Infrastructure / Industrials, Semiconductors / Chips, Cross-Border Payments / Remittance, Marketplace / Platform, Consumer / D2C.

After identifying the sector, **append sector-specific questions and metrics** to each relevant section. Sector-specific items extend the core framework, they do not replace it.

## Missing Data Protocol

**Every field must have an explicit value.** When information is unavailable:

1. **Mark the field**: `[NO INFO]`
2. **Note impact**: After each section, list `[NO INFO]` items with materiality (Critical / Important / Minor)
3. **Aggregate**: Include a "Data Completeness Score" in the Investment Thesis section
4. **Never guess**: Use `[ESTIMATED — basis: ...]` for estimates. Never present assumptions as facts.

## Source Requirements & Citations

All external data must come from verifiable, authoritative sources.

**Preferred sources (priority order):**
1. Yahoo Finance (market data, multiples) — use `scripts/fetch_yahoo_finance.py`
2. Company IR / SEC filings
3. Capital IQ / Bloomberg / PitchBook (if user provides)
4. StockAnalysis.com, CompaniesMarketCap.com, MacroTrends
5. Industry reports (FXC Intelligence, McKinsey, Nilson Report, etc.)

**Citation rules:** [Low freedom — exact format]
- Every section with external data ends with a `Sources:` block
- Format: `Source: [Description](URL) — accessed [date]`
- Never present a number without attribution
- Flag data >6 months old as `[STALE — as of YYYY-MM]`
- Distinguish TTM vs NTM multiples explicitly

## Analysis Framework

Load `references/analysis-framework.md` when starting. Each section's detailed checklist is there.

0. **Deal Intake Interview** — collect deal context from user (see above)
1. **Company Overview** — identity, funding, cap table
2. **Financial Deep Dive** — revenue, unit economics, margins, burn
- [ ] Checkpoint: all metrics present or marked [NO INFO] with materiality
3. **Comparable Public Multiples** — run `scripts/fetch_yahoo_finance.py`; see `references/comparable-multiples.md`
3.5. **Secondary Market Pricing** — run `scripts/fetch_secondary_prices.sh`; see `references/secondary-selectors.md`
- [ ] Checkpoint: secondary prices fetched from Forge/Caplight/Hiive or marked [NO INFO]
4. **Market Context** — TAM/SAM/SOM, moats, competitive landscape
- [ ] Checkpoint: sector overlay applied, comps fetched, TTM vs NTM labeled
5. **Growth & Momentum** — operating metrics, efficiency, catalysts
6. **Investor & Governance** — round history, board quality
7. **Risk Assessment** — weighted 8-dimension scoring matrix
8. **Valuation & Return** — scenarios, IRR, MOIC, exit pathways, secondary-implied valuation
- [ ] Checkpoint: scenario probabilities sum to 100%; IRR uses consistent entry valuation
9. **Investment Thesis** — conviction rating, for/against, remaining questions
10. **Supporting Materials** — data room, articles, pitch deck notes
- [ ] Checkpoint: memo saved, PDF generated, Notion updated (if NOTION_TOKEN set)

## Bundled Scripts

### `scripts/fetch_yahoo_finance.py`
Fetch public comp data from Yahoo Finance for Section 3.
```bash
python scripts/fetch_yahoo_finance.py WISE.L RELY DLO FLYW PAYONEER WU --format table
```
Requires: `pip install yfinance`

### `scripts/extract_pdf.py`
Extract text from data room PDFs (pitch decks, financials).
```bash
python scripts/extract_pdf.py "path/to/file.pdf" --pages 1-10 --max-chars 50000
```
Requires: `pip install PyPDF2`

### `scripts/extract_excel.py`
Extract data from Excel files (financial models, cap tables).
```bash
python scripts/extract_excel.py "path/to/model.xlsx" --sheets "Income Statement,Cap Table" --max-rows 200
```
Requires: `pip install openpyxl`

### `scripts/generate_pdf.py`
Generate a Notion-styled PDF from a markdown memo.
```bash
python scripts/generate_pdf.py "path/to/memo.md" --output "path/to/output.pdf"
```
Requires (one of — script auto-detects):
- `pip install markdown reportlab` (lightweight, no native deps — always works)
- `pip install markdown xhtml2pdf` (richer HTML/CSS — needs native build tools)

### `scripts/fetch_secondary_prices.sh`
Scrape secondary market prices for a single company from Forge, Caplight, and Hiive.
```bash
bash scripts/fetch_secondary_prices.sh "SpaceX"
```
Requires: `agent-browser` CLI (`npm i -g agent-browser`), Chrome debug profile with Caplight + Hiive sessions.
Outputs JSON to stdout: `{forge: {price, url}, caplight: {price, url}, hiive: {price, url}, company, date}`
See `references/secondary-selectors.md` for platform navigation details.

### `scripts/push_to_notion.py`
Push a completed memo to Notion as formatted blocks.
```bash
python scripts/push_to_notion.py PAGE_ID "path/to/memo.md" --token $NOTION_TOKEN
```
Requires: `pip install requests`

## Context Efficiency

Load supporting files **selectively**:
- `references/sector-overlays.md` — read **only** the detected sector section
- `references/comparable-multiples.md` — read when building the comp table (Section 3)
- `references/analysis-framework.md` — load when starting the analysis
- `assets/analysis-template.md` — reference for output structure; load at output time
- `references/due-diligence-checklist.md` — load only if user requests a DD status check
- `references/secondary-selectors.md` — load when scraping secondary prices (Section 3.5)
- `references/setup-guide.md` — load if Notion or PDF generation fails, or if user asks about setup
- `references/faq.md` — load only if user asks how the skill works

## Input Requirements

- **Company name or description**: Required
- **Financial data**: Pitch deck, financial statements, data room contents, or key metrics
- **Market data**: Industry reports, competitor information, market sizing sources
- **Accepted formats**: PDF, CSV, JSON, plain text, Excel, or conversational input
- **Public comps**: Optionally provide a peer set; otherwise one will be constructed

## Output: Investment Memo

The deliverable is a **standalone investment memo** saved as markdown.

**Local save convention:** [Medium freedom — structure required, prose flexible]
- If user provides `--folder` path, save there
- Default: `C:\Users\denis\OneDrive - RLC AltInvest Consultants FZCO\Work\{CompanyName}\`
  - Create the company subfolder if it doesn't exist
  - If OneDrive path is not available, ask the user where to save
- Fallback: the skill's `output/` directory
- Naming: `YYYY MM DD CompanyName Investment Case` (.md / .pdf)

**Post-analysis pipeline:** [Low freedom — execute in order]
1. **Verification Agent** — run independent fact-check (see below)
2. Generate PDF — `python scripts/generate_pdf.py memo.md --output "folder/...pdf"`
3. Push to Notion — create page in Companies Cards database, then `python scripts/push_to_notion.py PAGE_ID memo.md --token $NOTION_TOKEN`
4. Report file paths, Notion URL, and verification summary to user

## Verification Agent

After the memo draft is written and before PDF/Notion export, launch an **independent verification agent** (`Agent` tool, subagent_type: `general-purpose`) that audits the memo for factual accuracy.

**Agent briefing template:**
> You are a fact-checker reviewing an investment memo about {Company}. Your job is to independently verify key claims using web search. You have NOT seen the research that produced this memo — approach it fresh.
>
> Read the memo at: {memo_path}
>
> Check the following categories. For each claim, search independently and report: CONFIRMED / DISPUTED / UNVERIFIABLE.
>
> 1. **Company facts** — founding date, HQ, founders, employee count, funding amounts, valuation
> 2. **Financial claims** — revenue figures, growth rates, margins, burn rate (if stated)
> 3. **Market data** — TAM/SAM figures, market growth rates, market share claims
> 4. **Competitor facts** — funding rounds, valuations, partnerships, product status
> 5. **Public comp data** — market caps, multiples, revenue (cross-check vs Yahoo Finance)
> 6. **Partnership/customer claims** — named partners, contract details
> 7. **Investor roster** — named investors, round participation
>
> Output a structured verification report in this exact format:
>
> ```
> ## Verification Report
> **Verified:** {date}
> **Claims checked:** {N}
> **Results:** {confirmed} confirmed, {disputed} disputed, {unverifiable} unverifiable
>
> ### Confirmed
> - {claim} — {source}
>
> ### Disputed
> - {claim} — Memo says: {X}. Found: {Y}. Source: {URL}
>
> ### Unverifiable
> - {claim} — no independent source found
>
> ### Accuracy Score: {confirmed / (confirmed + disputed)} %
> ```
>
> Be thorough but concise. Only check factual claims, not opinions or projections. This is research only — do not modify any files.

**Integration rules:** [Low freedom]
- The verifier agent runs in the **foreground** — wait for results before proceeding
- Append the verification report to the memo as a new section before the Sources Appendix
- If any claim is **DISPUTED**, flag it inline in the memo with `[DISPUTED — verifier found: {X}]` and let the analyst (user) decide whether to correct
- If Accuracy Score < 80%, warn the user before proceeding to PDF/Notion
- The verifier must use **fresh web searches** — it must not rely on the research agent's earlier findings

**Memo structure:** Header → Executive Summary (2-3 paragraphs, standalone brief) → Sections 1-10 → Sources appendix.

**Notion export config:**
- Database ID: `1dfe5367-1ac8-8045-ab59-cd61c9f6d622` (Companies Cards)
- Token env var: `NOTION_TOKEN`
- If Notion MCP is unavailable, skip export and inform user.

## Example Usage

> "Analyze SpaceX as a pre-IPO investment opportunity. Focus on Starlink segment economics."

> "I have the Series C pitch deck for [Company]. Evaluate at a $2B valuation, benchmark against public SaaS comps growing 40%+ YoY."

> "Compare secondary market pricing of Stripe, Databricks, and Canva against their public comp sets."

> "Run a bear/base/bull scenario analysis for Anduril at $14B valuation."

> **Output:** `2026-02-24 SpaceX Investment Case.md` — Executive Summary + 10 sections + Sources appendix + Data Completeness Score

## Edge Cases

- **DRM-protected PDF**: `extract_pdf.py` may return only watermark text — inform user, request plain text or manual paste
- **Ambiguous sector**: spans 2+ sectors → ask user to confirm primary; load one overlay only
- **Conflicting sources**: flag explicitly; prefer Company IR > third-party; document in Sources block
- **No public comps**: fall back to private round multiples; note "no quoted peers — DCF-only valuation"
- **Secondary pricing, no financials**: proceed with market-implied analysis; label clearly as market sentiment not fundamental
- **agent-browser not installed**: skip secondary scraping, inform user, mark `[NO INFO]` for secondary prices
- **Platform login expired**: inform user to re-login in Chrome debug profile (`~/.chrome-debug`), retry or skip
- **Company not found on secondary platforms**: record `[NO INFO]` per platform, note in memo — company may be too early-stage or not actively traded

## Quality Checks

1. All financial metrics internally consistent (ARR = MRR x 12)
2. Comparables are genuinely comparable (sector, scale, growth)
3. Implied valuation ranges reasonable for stage
4. Risk scores align with qualitative descriptions
5. Scenario probabilities sum to 100%
6. IRR calculations use consistent entry valuation and horizons
7. Investment thesis supported by preceding analysis
8. Public multiples cross-referenced against recent data

## Limitations

- Informational/educational purposes only, not investment advice
- Private company data may be unaudited or incomplete
- Public multiples are point-in-time snapshots
- No access to Bloomberg/PitchBook unless user provides data
- Projections and scenarios are inherently uncertain
