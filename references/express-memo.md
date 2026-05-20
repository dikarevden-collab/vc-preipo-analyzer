# Express Memo — Template, Rules, and Discipline

A 4–5 page screening memo that distills a verified full memo into a balanced summary for the IC. The express memo surfaces the inputs the IC needs to ask the question "Should we spend more DD effort on this deal, or screen it out now?" — but it does not answer that question itself. The IC does.

## Table of Contents

- [Purpose](#purpose)
- [Save Location](#save-location)
- [Derivation Rules](#derivation-rules-low-freedom)
- [Structure Template](#structure-template)
- [No Recommendation Block](#no-recommendation-in-the-express-memo-low-freedom)
- [Clarity Discipline](#clarity-discipline-low-freedom)
- [Length Discipline](#length-discipline-low-freedom)
- [Audience-Aware Framing](#audience-aware-framing)

## Purpose

Senior IC members typically do not read 40-page memos cold. The express memo is what they read first; the full memo is what they read when they want to dig deeper. Think of it as the abstract that lets the reader decide whether the rest of the document is worth opening — not the abstract that pre-decides.

## Save Location

`{output_folder}/YYYY MM DD {Company} Express Memo.md`

## Derivation Rules **[Low freedom]**

- **No new claims, no new sources.** Every fact in the express memo must trace to the verified full memo. Citing the full memo as the source is correct; introducing external citations not already in the full memo is not.
- **No new numbers.** Round, summarize, or omit — but never introduce a figure (revenue, multiple, growth rate, valuation) that does not appear in the full memo.
- **No recommendation, no verdict, no conviction rating.** The Express Memo presents the case both ways and the pre-conditions; the reader decides. Do NOT include Proceed/Wait/Pass, Buy/Hold, position-sizing, or escalation triggers. Those belong to the full memo (Section 9), not here.
- **Inherit verification.** Facts already verified at the full-memo stage do not need re-verification. Only distillation drift (rounding errors, dropped qualifiers, stale dates) needs a focused check.

## Structure Template

Exact section order, 4–5 pages total; all section headings MUST be numbered as `## N. emoji Title`:

```markdown
# Express Memo: {Company}

**Date:** {date}
**Prepared by:** RLC AltInvest Consultants FZCO
**Purpose:** {one-line statement — what decision the memo serves, who the audience is}

> **CONFIDENTIAL.** {standard confidentiality line}

## 1. 🏢 Company Overview
- **Full Name:**
- **What does the company do?** {3–6 sentences in plain English — what the product is, what problem it solves, who buys it, and how it makes money. Define technical jargon inline on first use, e.g., "AI agents (software that can take multi-step actions on its own, not just answer questions)".}
- **Sector:**
- **Headquarters:** {+ additional offices if material}
- **Founded:** {include stealth-exit date if different}
- **Employees:** {state Unknown if not disclosed}
- **Last Funding Round (Date & Valuation):**
- **Total Funding raised:** {cumulative, breakdown by source}
- **Secondary Market Price and Valuation, Current:** {Forge/Caplight/Hiive or "Not traded"}

## 2. 💼 Deal Terms
*This section must clearly answer: what is the investor offered, on what terms, at what price, and with what known unknowns. State Unknown items explicitly — do not gloss.*

### How this deal works
{Only include for structurally non-trivial deals — SPACs, de-SPACs, SAFE conversions, tender offers, complex tranches. Skip for plain primary or secondary equity purchases. Explain in plain language:
- How this deal differs from a normal "write a check, get shares" transaction
- Key terminology defined (SPAC, SAFE, PIPE, etc.) with 1-sentence definitions on first use
- Why each tranche / instrument exists and how the economics work
- What happens in each failure mode (deal doesn't close, conversion mechanics fail, etc.)
- Why discounts / structures differ between tranches if applicable
~150–300 words. The IC reader should be able to evaluate the term sheet AFTER reading this subsection — not before.}

### What we are being offered

**First, a Counterparties table** naming each role exactly once (this is the only place in the memo where the seller, broker, etc. are named — neutral phrasing elsewhere):

```markdown
**Counterparties:**

| Role | Name |
|---|---|
| Seller / SPV manager | [Name] |
| Broker | [Name] OR `N/A — [reason, e.g. direct relationship with the seller]` |
```

Add additional roles as applicable (placement agent, sub-advisor, fund manager). Always include the row even if the role is N/A — do not omit.

**Then, the tranche comparison table.** If multiple tranches/instruments are offered: use ONE side-by-side comparison table with tranches as columns (e.g., `| Term | Tranche A — SAFE | Tranche B — PIPE |`). Do not split into multiple per-tranche tables — it creates excessive horizontal rules and obscures the comparison.

**Markdown table rule [required]:** Every table header MUST have a non-empty first cell (e.g., "Term", "Item", "Metric"). Tables with empty first headers (`| |`) render badly in `generate_pdf.py` — column widths collapse and row labels overflow into the next column.

Rows of the tranche comparison table (in order):
- Instrument (SAFE / PIPE / direct primary / secondary / SPV unit / etc.)
- Pricing (headline + any discount mechanic)
- Effective entry vs. headline valuation (analyst math)
- Day-1 paper gain at par (entry vs. fair value)
- Net Day-1 gain after SPV/vehicle fees (analyst math; state hurdle assumptions if known)
- Lockup (state explicitly if "None")
- Capacity available to us
- If deal mechanics fail (e.g., SPAC doesn't close, round fails to fill)
- Status (signed / open / pending)

**If only one tranche is offered:** use a single 2-column key-value table with the same row labels.

Then below the tranche table, in **short paragraphs** (not bullet lists, not separate tables):
- **Vehicle:** SPV details, distribution mechanics, fee structure
- **GP Track Record on This Name:** prior round participation by the GP/intermediary — explicitly flag this is GP-side cost basis, NOT ours

Followed by a compact **Known Unknowns** table:
- Item | Status (Unknown / Awaiting GP response / TBD pre-close, with one-line reason)

## 3. 📊 Market Context
- **TAM:** {deck claim if any + analyst-derived SAM with critique if deck overstates}
- **Tailwinds:** {macro trends helping}
- **Headwinds:** {structural / cyclical challenges}
- **Category Maturity:** {Early / Growth / Mature / Consolidating}
- **Competitive Intensity:** {Fragmented / Clear leaders / Up for grabs}

## 4. 📊 Investment Case
- **Strengths:** {3–6 verified positives}
- **Weaknesses:** {3–6 verified negatives — derived from full memo, not speculation}
- **What's the moat?** {by moat type: Talent / Capital / Technical / Customer-Data / Distribution — Strong / Partial / Unproven / Unverified verdict per moat}
- **How expensive is this vs. similar companies?** {public comp median + implied multiple at headline valuation + same after any discount mechanic + private comp set with stale-mark flagging}

## 5. 🔥 Growth & Momentum
- **Key Metrics:** {ARR, users, customers, pipeline, benchmarks — state Unknown if undisclosed}
- **Recent Achievements:** {bulleted milestones past 12 months}
- **Strategic Importance:** {why this company matters at this point in its category}

## 6. 🧠 Investors
- **Lead Investors:** {by round, with track-record note}
- **Repeat Participation:** {Y/N, which rounds — include GP/intermediary as potential co-investor if applicable}

## 7. ⚠️ Risks
- **Legal and Regulatory:**
- **Market:**
- **Execution:**
- *(For applicable sectors, add Key-Person / Technology / Concentration risks as additional bullets)*

## 8. 🔎 Additional Notes
- **Data Room:** {provided / pending / TBD}
- **Articles / Press Links:** {tier-1 coverage with hyperlinks; explicitly note absence if material}
- **Pitch Deck:** {filename and date}
- **Other Research:** {full memo cross-reference + verification score; comp data source and date}

## 9. 📎 Appendix (optional)
{Use this section for analytical commentary that does not fit cleanly in Sections 1–8 but is material to the IC's understanding. Examples:
- Why this deal is structured the way it is (e.g., "Why a SPAC and not a private round?")
- Cross-cycle / cross-comparable historical context
- Detailed walk-throughs of specific risk scenarios
- Counterfactual analysis (what would change our view)
Keep to one focused topic per Appendix item; multiple appendices can use sub-headings (9.1, 9.2, etc.). Same length / clarity / no-recommendation discipline applies.}

**Verification:** {one-line trace to full memo and accuracy score; note any GP-direct statements incorporated and their date}
```

## No Recommendation in the Express Memo **[Low freedom — strict]**

- The Express Memo presents facts and balanced analysis (Strengths AND Weaknesses; Tailwinds AND Headwinds; Risks across multiple categories). It does NOT state a Proceed / Wait / Pass verdict, conviction rating, position-sizing guidance, or escalation trigger.
- The reader (IC, partner, LP) makes the call. The memo's job is to give them the inputs cleanly — not to pre-decide.
- The full memo retains the conviction rating, position sizing, and remaining-diligence list (Section 9). That is where the recommendation lives — not here.
- If any section header reads "Recommendation," "Conviction," or "Verdict" in the Express Memo, delete it before delivery.

## Clarity Discipline **[Low freedom — must follow]**

- **Plain language, define jargon inline.** Write for an IC member who is smart and busy, not for a specialist. Avoid analyst/finance jargon where plain English works. On first use of any technical term — "AI agents," "PIPE," "S-4," "SAFE," "fab excursion" — give a 5-to-10-word inline definition in parentheses. Prefer short sentences. Avoid em-dash chains.
- **Section numbering.** Every Express Memo H2 heading must be numbered: `## 1. 🏢 Company Overview`, `## 2. 💼 Deal Terms`, etc. The numbers go BEFORE the emoji.
- **Name counterparties exactly once, in a dedicated table.** At the top of the "What we are being offered" subsection of Deal Terms, include a small **Counterparties** table naming the seller and broker (and any other distinct parties — fund manager, sub-advisor, placement agent — as applicable). If a role is not applicable (e.g., no broker because the relationship is direct), write `N/A — direct relationship with the seller`. Throughout the rest of the memo, use neutral phrasing instead of repeating names: "the GP", "the seller", "the offering party", "the SPV", "the offered vehicle". This keeps the memo readable, allows easy redaction for external versions, and signals that the IC's analysis turns on the deal and the asset, not on the personality offering it.
- **State unknowns as Unknown.** Never gloss, never speculate. If a fact is not in the full memo and not provided by the offering party, write `Unknown` or `Pending — awaiting response`. Vagueness is a worse failure than admitting ignorance.
- **No ambiguity about who's who.** When citing GP-side cost basis, prior-round participation, or intermediary statements, explicitly mark them as such. Never conflate the investor (us) with the GP, the prior-round investors, or the founders.
- **Show the math.** When the deal has discount mechanics (SAFE discount, PIPE discount, OID, structured warrants), show effective entry price AND Day-1 paper gain AND net-of-fees gain. Raw terms without derived numbers leaves the reader doing arithmetic the analyst should have already done.
- **Every external-data point includes its source date.** Public comp pulls, leaderboard checks, market caps, valuations — all dated.

## Length Discipline **[Low freedom]**

- Target 1,500–2,500 words total (corresponds to ~4–5 PDF pages)
- Strengths / Weaknesses / Risks bullets: ≤80 words each
- Deal Terms tranche tables: include all required fields, no shortcuts
- If draft exceeds 3,000 words, cut — usually from Market Context (TAM/headwinds) and Investment Case (Strengths/Weaknesses) which tend to bloat

## Audience-Aware Framing

Before drafting, identify the specific decision being made:

| Audience | Decision | Framing |
|---|---|---|
| Internal IC, existing position | Should we top up at the new round / SPAC? | Existing layers out of scope — focus solely on new-money economics |
| Internal IC, fresh deal | Should we enter at all? | Full screening; standard go/no-go framing |
| External LP / co-investor | Is this an investable deal for someone with no insider position? | Cautious tone; no insider context; emphasize structural items |
| Mixed audience | Both fresh-entry and top-up readers | Slightly longer (~5 pages); explicit section noting differential conclusion by holder type |

If audience is ambiguous, ask the user before drafting.
