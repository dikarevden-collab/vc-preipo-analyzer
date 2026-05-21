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

## Crunchbase Signals Capture **[Low freedom — must follow]**

Three third-party momentum proxies from Crunchbase's company profile must be captured for every memo and carried into **Section 5 Growth & Momentum**: **Growth Score** (0–100, employee/traffic/funding velocity), **CB Rank** (integer; lower = better global rank), **Heat Score** (0–100, short-term activity surge). Each carries a trend arrow (↑/↓) that matters as much as the value.

**Capture protocol (in priority order):**

1. **If a Crunchbase PDF is in the intake materials** (typical filename: `Crunchbase.pdf`, or any PDF whose first page contains the Crunchbase logo + the company name): read the three scores **and their trend arrows** from page 1 visually via the `Read` tool. Crunchbase PDFs are image-based — `extract_pdf.py` returns empty text; the Read tool's multimodal view is the working path. Record the values + arrows + the access date of the PDF.

2. **Else, present a single AskUserQuestion chip** asking the analyst for all three scores in one round-trip. Use this chip text:
   - Header: `Crunchbase signals`
   - Question: `What are the current Crunchbase signals for {Company}? Check the company's Crunchbase profile (https://www.crunchbase.com/organization/{slug}) and report Growth Score, CB Rank, and Heat Score, each with its trend arrow (↑ or ↓).`
   - Free-text input — analyst pastes a single line, e.g. `Growth 86 ↓, CB Rank 47 ↑, Heat 92 ↑`.

3. **Else (analyst declines or marks unknown)**: record `[NO INFO]` for all three fields and continue. Do not block the pipeline.

### Official Crunchbase definitions (source: support.crunchbase.com Knowledge Center)

**[Low freedom — quote these definitions verbatim or near-verbatim in any memo glossary or footnote]** All three signals are AI-generated by Crunchbase from proprietary data; users cannot edit them. The first two are **self-normalized** — that is the single most important interpretation rule.

- **Growth Score (0–100):** Quantifies a private company's growth using both predictions and historical data including funding, operations, headcount, market share, financial, customer growth, product usage, M&A, and historical growth of the company. **Self-normalized**: the score reflects how the company's current growth compares to *its own* historical trends, not to other companies. The higher the score, the more likely the company is experiencing strong growth across multiple areas relative to its own trajectory. *(Source: [What is a Growth Score?](https://support.crunchbase.com/hc/en-us/articles/39902124712211-What-is-a-Growth-Score))*
- **Heat Score (0–100):** Measures market interest or prominence based on Crunchbase profile activity and presence in the media. **Self-normalized**: reflects how current market interest compares to the company's own historical baseline. The higher the score, the more likely the company is currently attracting attention from investors, partners, and competitors. *(Source: [What is a Heat Score?](https://support.crunchbase.com/hc/en-us/articles/39902159873043-What-is-a-Heat-Score))*
- **CB Rank (integer; 1 = best):** A holistic Crunchbase popularity rank across **all entities of the same type** (e.g. companies vs. companies). Inputs include total funding amount, the entity's strength of relationships with other entities in the Crunchbase ecosystem, and how many times the entity has been viewed recently. Unlike Growth and Heat, CB Rank is **global, not self-normalized** — a rank of 47 means the company is the 47th most-ranked among all companies. *(Source: [Crunchbase Rank (CB Rank)](https://support.crunchbase.com/hc/en-us/articles/115010477187-Crunchbase-Rank-CB-Rank))*

### Interpretation rubric for memo commentary

Because Growth and Heat are self-normalized, **do not describe absolute scores as universal bands** ("breakout across the universe of companies"). Instead, describe them in self-relative terms:

- **Growth Score & Heat Score (self-normalized, 0–100):**
  - Value alone shows how far the company has moved relative to its own historical baseline (high = currently above its own trajectory; low = below).
  - **Arrow is the load-bearing read.** ↑ = trending up vs. recent self-history; ↓ = trending down vs. recent self-history. A high score with a ↓ arrow signals the company is still well above its own historical average but has begun to roll over from a recent peak — that is the early-warning signal, not the absolute value.
  - Do NOT use the bands "stalled / moderate / strong / breakout" as universal labels; if used at all, frame them as "high/low relative to the company's own history."
- **CB Rank (global, integer, lower = better):**
  - **<100 = top-tier global**; 100–1,000 = top stratum; 1,000–10,000 = mid; >10,000 = niche. These bands ARE universal — CB Rank is genuinely global.
  - Arrow: ↑ = climbing toward #1 (improving); ↓ = falling away from #1 (deteriorating).
- **Divergent combinations are the most informative read.** Example: *Heat 92 ↑ with Growth 86 ↓* means the company is at a peak of market attention (relative to its own history) but its underlying growth signal has begun to roll over from a recent peak. That divergence — spotlight at maximum, fundamentals cooling — is exactly the kind of layered signal that warrants explicit memo commentary. Do not present the three numbers without interpretation.

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
8. **Push to Notion** — ALWAYS run (unless `NOTION_TOKEN` is absent — see config below). **Two-step procedure: [Low freedom — must follow]**
   - **Step 8a — Create the page via curl** (NOT via the claude.ai Notion MCP `notion-create-pages` tool — its `parent` param double-serializes JSON objects and fails for database-parented pages):
     ```bash
     curl -s -X POST "https://api.notion.com/v1/pages" \
       -H "Authorization: Bearer $NOTION_TOKEN" \
       -H "Notion-Version: 2022-06-28" \
       -H "Content-Type: application/json" \
       -d '{
         "parent": {"database_id": "1dfe5367-1ac8-8045-ab59-cd61c9f6d622"},
         "properties": {
           "Company": {"title": [{"text": {"content": "{Company}"}}]},
           "Sector": {"rich_text": [{"text": {"content": "{Sector} — {Sub-sector}"}}]},
           "Comment": {"rich_text": [{"text": {"content": "{1-line headline: last round + conviction}"}}]}
         }
       }'
     ```
     Capture the returned `id` as `PAGE_ID`. Leave the scoring columns (Suitability, Tech, Investors, Team, Momentum, Strategic, Legal & Risks, IPO, Secondary, CapTable, Valuation, Repeats) empty — those are for the analyst's manual IC scoring.
   - **Step 8b — Push memo body via the script** (handles all block types — tables, headings, callouts, code blocks — within the 100-block-per-PATCH and 2000-char-per-rich-text Notion API limits, batched automatically):
     ```bash
     python scripts/push_to_notion.py PAGE_ID memo.md --token "$NOTION_TOKEN"
     ```
     Push the full memo if it was produced; otherwise push the Express Memo.
9. **Report** file paths (only for deliverables actually produced), Gamma URL (if generated), Notion URL, and verification summary to user. Note which deliverables were skipped per the Deliverables Interview.

**Notion export config:**
- Database ID: `1dfe5367-1ac8-8045-ab59-cd61c9f6d622` (Companies Cards)
- Token env var: `NOTION_TOKEN` — Internal Integration token (`ntn_…`), stored as a **Windows User env var** (`[System.Environment]::SetEnvironmentVariable("NOTION_TOKEN", "ntn_…", "User")`). The Companies Cards database must be explicitly shared with the integration via Connections menu — workspace-level access is not sufficient under Notion's current permission model.
- **Path selection: prefer the curl + script combo over the claude.ai Notion MCP** for memo pushes. The MCP can disconnect mid-session, and its block schema only supports paragraph + bulleted_list_item — memo tables and headings would be silently dropped. The script path is the durable default; the MCP is fine for lookups (`notion-fetch`, `notion-search`) but not for content writes.
- **If `NOTION_TOKEN` is unset**: skip the Notion push entirely, inform the user, and point them to `references/setup-guide.md` for one-time setup.

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
- **Notion MCP (`claude.ai Notion`) disconnected**: not a blocker — the Notion push uses curl + `push_to_notion.py` with `NOTION_TOKEN`, which is independent of the MCP. The MCP is only used for read operations (database lookups) if at all.
- **`NOTION_TOKEN` not set**: skip Notion push, inform user, point them to `references/setup-guide.md` § "Notion setup" for the one-time token setup. Do NOT attempt the claude.ai MCP `notion-create-pages` fallback — it double-serializes the `parent` field and fails.
- **Notion API 404 / "object_not_found" on page creation**: the integration is not shared with the Companies Cards database. Direct user to open the DB → `…` menu → Connections → connect their Internal Integration. Token alone is insufficient under Notion's current permission model.

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
