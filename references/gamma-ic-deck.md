# Gamma IC Deck — Generation Spec

After generating the full memo PDF, create a **20-slide investment committee presentation** via the Gamma MCP tool. This deck distills the full memo into an IC-ready format.

## Table of Contents

- [Gamma Parameters](#gamma-parameters-low-freedom)
- [Header/Footer (Pro plan + fallback)](#headerfooter-logo--page-numbers--confidential)
- [Theme Config](#theme-config)
- [Slide Structure](#slide-structure)
- [Splitting Long Decks](#if-content-requires-more-than-20-slides)
- [Execution Flow](#execution-flow)
- [Output Files](#output-files)

## Gamma Parameters **[Low freedom — use exact values]**

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| `inputText` | Full memo markdown (sections 1-10 + exec summary) | Gamma requires complete content — never summarize |
| `format` | `"presentation"` | IC deck |
| `numCards` | `20` | Gamma max is 20 per deck. If content requires 21-40 slides, split into 2 presentations |
| `textMode` | `"condense"` | Distills 30-50KB memo into slide-appropriate bullets |
| `themeId` | `"tf15c1vstmnc6z1"` | RLC custom theme |
| `textOptions` | `{amount: "medium", tone: "professional", audience: "executives"}` | IC audience |
| `imageOptions` | `{source: "noImages"}` | Data-driven deck, no decorative images |
| `cardOptions` | See below | Standard 16x9 with logo + page numbers |
| `exportAs` | `"pptx"` (1st call) then `"pdf"` (2nd call) | Two generate calls with identical content. ~120 credits total. |

**cardOptions (exact JSON):**
```json
{"dimensions": "16x9"}
```

## Header/Footer (logo + page numbers + CONFIDENTIAL)

- Gamma `headerFooter` in `cardOptions` requires **Pro plan**. If available, use:
  ```json
  {"dimensions": "16x9", "headerFooter": {"topLeft": {"type": "image", "source": "themeLogo", "size": "sm"}, "topRight": {"type": "text", "value": "CONFIDENTIAL"}, "bottomRight": {"type": "cardNumber"}, "hideFromFirstCard": true}}
  ```
- **If Pro not available (current):** Omit `headerFooter` from `cardOptions`. Instead, include in `additionalInstructions`: "Add 'CONFIDENTIAL' label in the top-right corner of every slide except the title slide. The RLC logo is automatically applied via the theme. Number each slide in the format 'N / total' in the bottom-right area of each slide except the title."

## Theme Config

- Custom RLC theme: `tf15c1vstmnc6z1`
- To update: call `mcp__claude_ai_Gamma__get_themes` with `name: "RLC"` to verify ID

## Slide Structure

Pass the following as `additionalInstructions`:

> Create a 20-slide investment committee presentation with this exact structure:
>
> **Opening (slides 1-3)**
> 1. Title slide: Company name, date, "Investment Committee Presentation". **No conviction badge / no "Conviction: X" subtitle** (universal no-recommendation rule). Subtitle should describe the situation or sector — e.g. "{Sector} — {Latest Round Headline}".
> 2. Executive Summary: 3-4 bullet synthesis — what the company does, key financials, the analytical situation. **No "bottom-line recommendation" / no Buy-Hold-Pass.** End with what would have to be true for the deal to clear, or what the open structural items are — committee decides.
> 3. Deal Overview: entry valuation, deal structure, share class, investment horizon, target return
>
> **Company & Market (slides 4-7)**
> 4. Company Overview: founding date, HQ, employees, product description, key customers
> 5. Funding History & Cap Table: round-by-round table, key investors, ownership breakdown
> 6. Market Opportunity: TAM/SAM/SOM with sources, market growth rate, key tailwinds
> 7. Competitive Landscape: positioning table, moat assessment, headwinds & tailwinds
>
> **Financials (slides 8-13)**
> 8. Revenue & Growth: revenue trajectory, YoY growth rates, revenue mix
> 9. Unit Economics: take rate / CAC / LTV / payback / GPAC metrics
> 10. Profitability & Margins: gross margin, EBITDA margin, burn rate, runway
> 11. Comparable Public Multiples: comp table (5-10 peers) with EV/Revenue, EV/GP, Rule of 40
> 12. Implied Valuation: private company discount application, valuation range vs current ask
> 13. Secondary Market Data: Forge/Caplight/Hiive prices, spread analysis, vs last primary round
>
> **Growth & Governance (slides 14-15)**
> 14. Growth Metrics & Catalysts: key operating KPIs, near-term catalysts, pipeline
> 15. Investor & Board Quality: notable investors, board composition, governance signals
>
> **Risk & Return (slides 16-18)**
> 16. Risk Assessment Matrix: 8-dimension weighted scoring table with composite score + critical risks
> 17. Scenario Analysis: bull/base/bear table with probabilities, exit multiples, IRR, MOIC
> 18. IRR Sensitivity & Exit Pathways: matrix + IPO/M&A/secondary timeline
>
> **Conclusion (slides 19-20)**
> 19. Investment Thesis — For: top 3-5 reasons to invest (left column) vs Against: top 3-5 reasons NOT to invest (right column)
> 20. Decision Inputs for the Committee: open structural items, key de-risking milestones to monitor, remaining DD questions, and a single hand-off line ("The committee has the inputs — the floor is yours"). **No "Recommendation" header, no "Conviction Rating: X", no vote request.** This must always be the last slide.
>
> Use tables and structured layouts over prose. Keep bullet points to 4-6 per slide maximum. Use bold for key numbers. No decorative images — this is a data-driven IC deck.

## If content requires more than 20 slides

(e.g., complex multi-business analysis), split into 2 Gamma presentations:
- **Part 1 (20 slides):** Opening + Company + Market + Financials + Comps
- **Part 2 (up to 20 slides):** Risk + Return + Thesis + Appendix slides
- Name Part 2 with suffix "(Part 2 — Risk & Return)"

## Execution Flow

1. **PPTX generation:** Call `mcp__claude_ai_Gamma__generate` with `exportAs: "pptx"` and all parameters above
2. **Poll:** `mcp__claude_ai_Gamma__get_generation_status` until `status: "completed"`
3. **Capture:** `gammaUrl`, `exportUrl` (PPTX link)
4. **Download PPTX:** `curl -L -o "{output_folder}/YYYY MM DD {Company} IC Deck.pptx" "{exportUrl}"`
5. **PDF generation:** Call `mcp__claude_ai_Gamma__generate` **again** with identical `inputText`, `additionalInstructions`, theme, and all parameters — but `exportAs: "pdf"`
6. **Poll + capture** PDF `exportUrl`
7. **Download PDF:** `curl -L -o "{output_folder}/YYYY MM DD {Company} IC Deck.pdf" "{exportUrl}"`
8. **Report:** Gamma URL, local PPTX path, local PDF path

## Output Files

All saved to the company output folder:

```
{output_folder}/
  YYYY MM DD {Company} Investment Case.md    ← full memo (~30-50pp)
  YYYY MM DD {Company} Investment Case.pdf   ← full memo PDF
  YYYY MM DD {Company} Express Memo.md       ← 2-3pp screening memo (derived from full memo)
  YYYY MM DD {Company} Express Memo.pdf      ← express memo PDF
  YYYY MM DD {Company} IC Deck.pptx          ← Gamma IC deck (PPTX)
  YYYY MM DD {Company} IC Deck.pdf           ← Gamma IC deck (PDF)
  YYYY MM DD {Company} IC Narrative.md       ← speaker script (aligned to deck)
  YYYY MM DD {Company} IC Narrative.pdf      ← speaker script PDF
```
