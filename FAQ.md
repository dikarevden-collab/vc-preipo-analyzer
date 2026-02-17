# VC/Pre-IPO Analyzer — FAQ

## What is this?

A Claude Code **skill** — a reusable analysis framework that you invoke with a single command. Instead of copy-pasting a long prompt every time you want to evaluate a deal, you run one command and Claude follows a structured, institutional-grade due diligence process.

## What files make up this skill?

```
~/.claude/skills/vc-preipo-analyzer/
│
├── SKILL.md                    # The core skill — what Claude reads and executes
│                                 Analysis framework, sector detection, missing data
│                                 protocol, Notion export, capabilities, quality checks
│
├── sector-overlays.md          # Sector-specific analysis extensions
│                                 Per-sector metrics, DD questions, risk weight
│                                 adjustments, and comp guidance for: SaaS, Fintech,
│                                 Medtech, AI, Infrastructure, Chips, Marketplace, Consumer
│
├── comparable-multiples.md     # Public comps methodology reference
│                                 Comp selection criteria, key multiples by business model,
│                                 private company discount framework, comp table templates,
│                                 common pitfalls, data sources
│
├── analysis-template.md        # Standardized output template
│                                 Exact structure for every analysis — tables, sections,
│                                 scoring matrices. Ensures consistency across deals
│
├── due-diligence-checklist.md  # DD tracking checklist
│                                 Categorized checklist (financial, commercial, market,
│                                 tech, team, legal, investor, valuation) with scoring
│
└── FAQ.md                      # This file
```

## How do I run it?

### Basic usage
```
/vc-preipo-analyzer [Company Name]
```

### With additional context
```
/vc-preipo-analyzer Anduril — focus on defense sector comps and contract backlog
```

### With attached files (pitch deck, financials, data room docs)
```
/vc-preipo-analyzer [Company Name]
```
Then provide files via @filename references or paste data into the conversation.

### Examples
```
/vc-preipo-analyzer SpaceX
/vc-preipo-analyzer "Stripe at $65B secondary valuation"
/vc-preipo-analyzer "Series B fintech, $500M ask — pitch deck attached"
```

## What does it produce?

A structured investment memo covering 10 sections:

1. **Company Overview** — identity, funding history, cap table
2. **Financial Deep Dive** — revenue, unit economics, margins, burn, revenue quality
3. **Comparable Public Multiples** — peer set with trading multiples, implied valuation range
4. **Market Context** — TAM/SAM/SOM, tailwinds/headwinds, moat assessment
5. **Growth & Momentum** — operating metrics, sales efficiency, catalysts
6. **Investor & Governance** — round history, board quality, signal assessment
7. **Risk Assessment** — weighted 8-dimension scoring matrix with composite score
8. **Valuation & Return Analysis** — scenario analysis (bull/base/bear), IRR, MOIC
9. **Investment Thesis** — conviction rating, reasons for/against, remaining questions
10. **Supporting Materials** — links, data room, articles, pitch deck notes

## What data does it need?

**Minimum** (for a public-info-only analysis):
- Company name

**Better** (for a meaningful analysis):
- Company name + key financials (ARR, growth rate, margins)
- Last round valuation and funding history

**Best** (for institutional-quality output):
- Pitch deck or investor presentation
- Financial statements or management accounts
- Data room access
- Customer references or NPS data
- Cap table details

The skill will clearly flag where data is missing and mark those items as **[NO INFO]** so you know exactly what gaps remain.

## How is it different from just asking Claude to "analyze a company"?

| Without the skill | With the skill |
|---|---|
| Different structure every time | Consistent 10-section framework |
| May forget key sections | Comprehensive — nothing skipped |
| No public comp benchmarking | Systematic comp table with implied valuations |
| Qualitative risk assessment | Quantified 8-dimension risk matrix |
| No return analysis | Bull/base/bear scenarios with IRR and MOIC |
| Freeform output | Standardized template — easy to compare deals |
| Starts from scratch each time | Builds on reference files and methodology |

## Can I customize it?

Yes. The skill files are plain markdown. You can:
- Edit `SKILL.md` to change the analysis framework
- Edit `analysis-template.md` to change the output format
- Edit `comparable-multiples.md` to add sector-specific comp guidance
- Edit `due-diligence-checklist.md` to add/remove checklist items
- Add new reference files for sector-specific frameworks

## What's the relationship with the Anthropic financial skills?

The Anthropic skills (`creating-financial-models` and `analyzing-financial-statements`) are complementary:

| Skill | Purpose | When to use |
|---|---|---|
| **vc-preipo-analyzer** (this) | Full deal evaluation and investment memo | Evaluating a new deal end-to-end |
| **creating-financial-models** | DCF, Monte Carlo, sensitivity analysis | Deep-dive on valuation modeling |
| **analyzing-financial-statements** | Ratio calculation and interpretation | When you have detailed financials to crunch |

You can use them together — run `vc-preipo-analyzer` for the full picture, then use the Anthropic skills to go deeper on specific financial questions.

## How does sector-specific analysis work?

The skill **auto-detects** the company's sector and pulls in the relevant overlay from `sector-overlays.md`. Each overlay adds:

- **Sector-specific metrics** (e.g., NRR for SaaS, take rate for fintech, clinical pipeline for medtech)
- **Sector-specific DD questions** (e.g., FDA pathway for medtech, export controls for chips)
- **Adjusted risk weights** (e.g., regulatory risk is weighted higher for fintech and medtech)
- **Comp guidance** (e.g., which multiples matter most for that sector)

Currently supported: SaaS, Fintech, Medtech/Biotech, AI/ML, Infrastructure/Industrials, Semiconductors, Marketplace/Platform, Consumer/D2C.

If the sector is ambiguous, Claude will ask you to confirm before proceeding.

## What happens when data is missing?

Every field gets an explicit answer. There are no blank cells or silent omissions:

| Situation | How it's shown |
|---|---|
| Data is available | The actual value |
| Data is not available | `[NO INFO]` |
| Data is estimated/inferred | `[ESTIMATED — basis: ...]` |

At the end of each section, a **Data Gaps** summary lists all [NO INFO] items and rates them:
- **Critical** — materially affects the investment decision
- **Important** — weakens confidence but doesn't block assessment
- **Minor** — nice-to-have

The Investment Thesis section includes a **Data Completeness Score** (% of fields with actual data).

## Does it integrate with Notion?

Yes (when configured). After completing an analysis, the skill can auto-export the results to a Notion database via MCP. It maps all key metrics (valuation, ARR, growth, risk score, IRR, conviction rating, etc.) to Notion properties and pastes the full memo into the page body.

**Setup required:** Notion MCP server must be connected in Claude Code, and the target database ID must be configured in `SKILL.md`.

## Planned enhancements

- **Presentation reverse-engineering**: Feed real pitch decks to extract and incorporate the questions they implicitly answer, refining sector-specific sections
- **Data room integration**: Systematic workflow for ingesting and analyzing a full data room, cross-referencing against the DD checklist
- **Portfolio-level views**: Compare multiple analyzed deals side-by-side in Notion
- **Historical comp tracking**: Track how public multiples change over time for key peer sets
