---
name: vc-preipo-analyzer
description: >
  Structured due diligence and investment memo for private/pre-IPO companies.
  Produces a verified full investment memo, a 2-3 page Express Memo screening
  document, a 20-slide IC Gamma deck, and a slide-by-slide speaker narrative.
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

## Deliverables Interview

**This is the FIRST step — run before Deal Intake.** A 3-question mini-interview to determine which outputs to generate. Use the `AskUserQuestion` tool, presenting all three questions in a single call:

1. **Gamma IC Deck** — `Yes` (20-slide PPTX + PDF via Gamma MCP) / `No` (skip deck generation)
2. **Memo format** — `Both` (full + Express) / `Full only` / `Express only`
3. **Speaker narrative** — `Both` (Express IC Brief + slide-by-slide) / `Express only` (10-min IC Brief, ~1,800 words, aligned to Express Memo) / `Full only` (25-30 min slide-by-slide, aligned to IC deck) / `None`

Store the answers and reference them throughout the pipeline. Re-confirm the package at the end of Deal Intake if any answer was ambiguous.

**Always present the interview.** **[Low freedom — must follow]** The Deliverables Interview is a single `AskUserQuestion` call carrying all three questions at once — one round-trip, not a stop-and-wait dialogue. Present it on every run, including runs where the user (or a system flag) has said "work without stopping for clarifying questions," "skip interview," or "just run it." The cost of one chip is near-zero; the cost of producing a Gamma deck or a 25-min narrative the user did not want is large. Do NOT default-and-proceed silently.

**The only exception** is when the user's initial message **unambiguously resolves all three questions** (e.g., "just give me the Express Memo, no deck, no narrative" — answers all three). In that case, skip the chip and confirm the inferred package in one line before research. If even one of the three questions is unresolved, present the chip.

**If the user explicitly declines the chip** (e.g., responds "skip the interview", "use defaults", "just run it" *as a direct reply to the chip itself*), then and only then apply the documented default: `Both memos + Gamma Yes + Express narrative` (matches prior runs — Flatpay, VGW, Vast Data).

**Smart skip logic:** **[Low freedom — must follow]**
- Parse the user's initial message for explicit output preferences (e.g., "just an Express Memo", "no deck", "skip the narrative", "full IC package") — if unambiguous on a given question, drop it from the chip and confirm the inferred answer in one line. Only drop questions whose answers are unambiguous; if any one of the three is unresolved, present the chip with the remaining question(s).
- **Dependency: Full narrative requires the Gamma deck** (it is slide-by-slide). If the user picks `Gamma = No` and `Narrative = Full` or `Both`, inform them and ask to either enable Gamma or switch the narrative to `Express` / `None`.
- **`Express only` memo still runs the full memo as intermediate** — the Express Memo is derived from the verified full memo, so the full memo is produced and verified internally; it is simply not saved as a final PDF deliverable when `Express only` is selected.

## Deal Intake Interview

Before starting research, collect deal-specific context the tool cannot find on its own. **Company name is the only required field** — all others are optional but significantly improve memo quality.

Present these questions to the user as a numbered list. Wait for answers before proceeding.

1. **Company name** *(required)*
2. **Materials** — "Do you have files to provide? Attach them or give a folder path (deck, data room, financials, cap table, website URL)"
3. **Counterparty / origination** *(always ask unless unambiguous in materials)* — Who brought the deal? Name the seller, SPV manager, broker, placement agent, or direct relationship — and any prior history we have with this counterparty (first deal / repeat / referred by whom). This question MUST always be asked unless the materials unambiguously name the counterparty. A pitch deck from the company itself does NOT name the counterparty — somebody sent us that deck, so we must ask. Default if the user declines: record `Unknown — counterparty not disclosed at intake` in the Counterparties table and proceed.
4. **Deal terms** — Entry valuation, price per share, share class, deal structure (secondary / SPV / direct / primary co-invest)
5. **Investment horizon** — Quick flip (<1yr), medium-term (2-3yr), or hold-to-IPO (5yr+)?
6. **Target return** — MOIC floor or IRR minimum the deal must clear?
7. **Appeal to investors** — Who are the target LPs / co-investors? Has any pre-marketing been done? What's the reception so far?
8. **Why this company?** — Origination story. Why was it selected over alternatives?
9. **Specific concerns** — Any risks or questions you want pressure-tested?

**Smart skip logic:** **[Low freedom — must follow]**
- Parse the user's initial message for answers already provided (e.g., "analyze SpaceX at $350B, secondary, 3yr hold" → questions 1, 4, 5 are answered)
- Only ask questions whose answers are not yet known
- **Counterparty question (Q3) is always-on UNLESS the materials unambiguously name the seller/broker/SPV manager.** Even on "just run it" / "skip interview" instructions, do not skip Q3 — ask it as a single one-liner before proceeding, or default to `Unknown — counterparty not disclosed at intake`.
- For other questions: if user says "just run it" or "skip interview" → proceed with company name + counterparty only, produce generic analysis on remaining dimensions
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

**Citation rules:** **[Low freedom — exact format]**
- Every section with external data ends with a `Sources:` block
- Format: `Source: [Description](URL) — accessed [date]`
- Never present a number without attribution
- Flag data >6 months old as `[STALE — as of YYYY-MM]`
- Distinguish TTM vs NTM multiples explicitly

## Analysis Framework

Load `references/analysis-framework.md` when starting. Each section's detailed checklist is there.

0a. **Deliverables Interview** — 3-question mini-interview on Gamma deck / memo format / narrative variant (see above)
0b. **Deal Intake Interview** — collect deal context from user (see above)
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
- [ ] Checkpoint: memo saved, PDF generated, Express Memo generated, Gamma deck generated, Notion updated (if NOTION_TOKEN set)

## Bundled Scripts

| Script | Purpose | Requires |
|---|---|---|
| `scripts/fetch_yahoo_finance.py TICKER1 TICKER2 ... --format table` | Public comp data for Section 3 | `pip install yfinance` |
| `scripts/extract_pdf.py "path.pdf" --pages 1-10 --max-chars 50000` | Extract text from data-room PDFs | `pip install PyPDF2` |
| `scripts/extract_excel.py "path.xlsx" --sheets "S1,S2" --max-rows 200` | Extract from financial models / cap tables | `pip install openpyxl` |
| `scripts/generate_pdf.py memo.md --output out.pdf` | Notion-styled PDF from markdown | `pip install markdown reportlab` (or `xhtml2pdf`) |
| `scripts/fetch_secondary_prices.sh "Company"` | Scrape Forge/Caplight/Hiive prices | `agent-browser` CLI + Chrome debug profile |
| `scripts/push_to_notion.py PAGE_ID memo.md --token $NOTION_TOKEN` | Push memo to Notion as blocks | `pip install requests` |
| `mcp__claude_ai_Gamma__generate` | Generate IC deck (PPTX + PDF) | Gamma MCP server connection |

## Output: Investment Memo

The primary deliverable is a **standalone investment memo** saved as markdown, plus four secondary outputs (Express Memo, IC Deck, Speaker Narrative — see references below).

**Local save convention:** **[Medium freedom — structure required, prose flexible]**
- If user provides `--folder` path, save there
- Default: `C:\Users\denis\OneDrive - RLC AltInvest Consultants FZCO\Work\{CompanyName}\`
  - Create the company subfolder if it doesn't exist
  - If OneDrive path is not available, ask the user where to save
- Fallback: the skill's `output/` directory
- Naming: `YYYY MM DD CompanyName Investment Case` (.md / .pdf)

**Memo structure:** Header → Executive Summary (2-3 paragraphs, standalone brief) → Sections 1-10 → Sources appendix → Section 11 Verification Report (auto-appended) → Section 12 Appendix (optional — for structural / counterfactual commentary that doesn't fit Sections 1-11).

## Concluding Fact-Check (mandatory for all research) **[Low freedom — never skip]**

Every research operation — initial memo generation **AND** any subsequent edit, update, addition, correction, or follow-up question that produces or modifies factual content — MUST conclude with an **independent fact-check agent**. This is non-negotiable.

- The fact-check must be performed by a **separate agent** (spawn via the `Agent` tool, subagent_type `general-purpose` unless a domain-appropriate one is available), not by the same agent that produced the changes. Self-verification is not verification.
- The fact-check must verify every factual claim added or modified: dates, amounts, lead investors, valuations, growth rates, customer names, hire dates, round participants, market data, every numbered metric.
- **Required output format:** a structured report with (a) findings per claim, (b) primary source URL(s) per finding, (c) confidence rating per finding (High / Medium / Low), (d) explicit `UNVERIFIED` flag for any claim that cannot be sourced, (e) a "Discrepancies vs. claim" table flagging anything that contradicts the memo.
- **Apply corrections before reporting work complete.** If a fact cannot be verified, mark it as `UNVERIFIED — pending data-room confirmation` in the memo rather than removing it or claiming verification.
- This rule applies to ALL deliverables touched: full memo, Express Memo, IC Brief, Speaker Narrative, and any Gamma deck content.
- See `references/verification-agents.md` for the full agent spec.

**Why this rule exists:** Independent verification catches errors that the producing agent missed during writing. Skipping this step has historically produced internally-contradicting memos — e.g., a funding history table correctly showing one lead investor while the prose above it named a different lead.

**Post-analysis pipeline:** **[Low freedom — execute in order; gate each step on the Deliverables Interview answers]**
1. **Full Memo Verification Agent** — ALWAYS run. Independent fact-check on full memo. See `references/verification-agents.md`. (Required even when user picked `Express only` because the Express Memo is derived from the verified full memo.)
2. **Generate Express Memo** — *Skip if Memo format = `Full only`.* 2-3 page screening memo distilled from verified full memo. See `references/express-memo.md`.
3. **Focused Verification on Express Memo** — *Skip if Memo format = `Full only`.* Drift check vs. full memo + spot-check. See `references/verification-agents.md`.
4. **Generate full memo PDF** — *Skip if Memo format = `Express only`.* `python scripts/generate_pdf.py memo.md --output "folder/...pdf"`
5. **Generate Express Memo PDF** — *Skip if Memo format = `Full only`.* Same script applied to the Express Memo.
6. **Generate Gamma IC Deck** — *Skip if Gamma = `No`.* PPTX + PDF export, downloaded to output folder. See `references/gamma-ic-deck.md`.
7. **Generate Speaker Narrative** — gated by Narrative choice:
   - `Express only` → 10-min IC Brief (~1,800 words) aligned to the Express Memo's 9 sections
   - `Full only` → 25-30 min slide-by-slide narrative aligned to the IC Deck (requires Gamma deck from step 6)
   - `Both` → produce both
   - `None` → skip
   - See `references/speaker-narrative.md` for both variants.
8. **Push to Notion** — ALWAYS run (unless Notion MCP unavailable). Create page in Companies Cards database, then `python scripts/push_to_notion.py PAGE_ID memo.md --token $NOTION_TOKEN`. Push the full memo if it was produced; otherwise push the Express Memo.
9. **Report** file paths (only for deliverables actually produced), Gamma URL (if generated), Notion URL, and verification summary to user. Note which deliverables were skipped per the Deliverables Interview.

**Notion export config:**
- Database ID: `1dfe5367-1ac8-8045-ab59-cd61c9f6d622` (Companies Cards)
- Token env var: `NOTION_TOKEN`
- If Notion MCP is unavailable, skip export and inform user.

## Document Formatting

All RLC investment documents follow the same formatting rules (Gilroy fonts, navy + teal + red palette, navy table headers with alternating rows, parenthesized negatives, date-stamped external data, etc.). **See `references/formatting.md` for the full spec** — load it when generating any final document (memo, express memo, narrative) or when adjusting `generate_pdf.py` styling.

## Sub-Deliverable References

Each of the four supporting deliverables has its own reference file. Load only the file(s) relevant to the current step of the pipeline:

- **Verification agents** (full memo + express memo drift-check) → `references/verification-agents.md`
- **Express Memo** (structure template, derivation rules, clarity discipline, audience framing, no-recommendation rule, length discipline) → `references/express-memo.md`
- **Gamma IC Deck** (Gamma MCP parameters, slide structure, execution flow, output files) → `references/gamma-ic-deck.md`
- **Speaker Narrative** (script format, tone, rules, examples) → `references/speaker-narrative.md`

## Context Efficiency

Load supporting files **selectively** — do not load everything up front:

- `references/sector-overlays.md` — read **only** the detected sector section
- `references/comparable-multiples.md` — load when building the comp table (Section 3)
- `references/analysis-framework.md` — load when starting the analysis
- `assets/analysis-template.md` — reference for output structure; load at output time
- `references/due-diligence-checklist.md` — load only if user requests a DD status check
- `references/secondary-selectors.md` — load when scraping secondary prices (Section 3.5)
- `references/setup-guide.md` — load if Notion or PDF generation fails, or if user asks about setup
- `references/formatting.md` — load when generating final documents or adjusting PDF styling
- `references/verification-agents.md` — load before running either verification pass
- `references/express-memo.md` — load when generating the Express Memo
- `references/gamma-ic-deck.md` — load when generating the IC deck
- `references/speaker-narrative.md` — load when generating the speaker script

## Input Requirements

- **Company name or description**: Required
- **Financial data**: Pitch deck, financial statements, data room contents, or key metrics
- **Market data**: Industry reports, competitor information, market sizing sources
- **Accepted formats**: PDF, CSV, JSON, plain text, Excel, or conversational input
- **Public comps**: Optionally provide a peer set; otherwise one will be constructed

## Example Usage

> "Analyze SpaceX as a pre-IPO investment opportunity. Focus on Starlink segment economics."

> "I have the Series C pitch deck for [Company]. Evaluate at a $2B valuation, benchmark against public SaaS comps growing 40%+ YoY."

> "Compare secondary market pricing of Stripe, Databricks, and Canva against their public comp sets."

> "Run a bear/base/bull scenario analysis for Anduril at $14B valuation."

**Output:** `2026-02-24 SpaceX Investment Case.md` (+ Express Memo, IC Deck PPTX/PDF, Speaker Narrative) — Executive Summary + 10 sections + Sources appendix + Verification Report.

## Edge Cases

- **DRM-protected PDF**: `extract_pdf.py` may return only watermark text — inform user, request plain text or manual paste
- **Ambiguous sector**: spans 2+ sectors → ask user to confirm primary; load one overlay only
- **Conflicting sources**: flag explicitly; prefer Company IR > third-party; document in Sources block
- **No public comps**: fall back to private round multiples; note "no quoted peers — DCF-only valuation"
- **Secondary pricing, no financials**: proceed with market-implied analysis; label clearly as market sentiment not fundamental
- **agent-browser not installed**: skip secondary scraping, inform user, mark `[NO INFO]` for secondary prices
- **Platform login expired**: inform user to re-login in Chrome debug profile (`~/.chrome-debug`), retry or skip
- **Company not found on secondary platforms**: record `[NO INFO]` per platform, note in memo — company may be too early-stage or not actively traded
- **Gamma MCP unavailable**: skip IC deck + Speaker Narrative generation, inform user, continue with full memo + Express Memo + Notion
- **Gamma generation fails**: warn user with error details, continue pipeline — Gamma is an enhancement, not core

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
