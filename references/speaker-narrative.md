# Speaker Narrative — Generation Spec

After the IC deck and Express Memo are generated, produce a **speaker script** — the exact words the presenter will say aloud while presenting the case to the IC. This is a **script to be spoken**, not a written summary.

Two variants supported. Default is the **10-min IC Brief aligned to Express Memo** — use this unless the user explicitly requests the longer slide-by-slide format.

## Table of Contents

- [Variant A — 10-min IC Brief (DEFAULT)](#variant-a--10-min-ic-brief-default)
- [Variant B — 25-30 min Slide-by-Slide Narrative](#variant-b--25-30-min-slide-by-slide-narrative)
- [Format & Structure Per Section / Slide](#format)
- [Examples (Correct vs. Wrong)](#example-correct--spoken-script)
- [Tone](#tone)
- [Rules](#rules-low-freedom)
- [Source Material](#source-material)
- [Execution](#execution)
- [Graceful Degradation](#graceful-degradation)

## Variant A — 10-min IC Brief (DEFAULT)

- **Pairs with:** Express Memo (the IC's primary reading document)
- **Length:** ~10 minutes / ~1,500–2,000 spoken words
- **Structure:** Mirrors Express Memo's 9 sections (Title + 8 sections + optional Appendix); each section gets ~1 minute of speaking time (~150–200 words)
- **Filename:** `{output_folder}/YYYY MM DD {Company} IC Brief (10 min).md`
- **Use when:** Standard IC presentation. The audience reads the Express Memo as their visual reference and the speaker delivers this concise walk-through.

### Section mapping to Express Memo

| Express Memo section | Brief slot | Speaking time |
|---|---|---|
| (Title + Conviction) | Opening | ~30 sec |
| 1. Company Overview | Slot 1 | ~1 min |
| 2. Deal Terms (incl. "How this deal works") | Slot 2 | ~1.5–2 min — densest content |
| 3. Market Context | Slot 3 | ~1 min |
| 4. Investment Case (Strengths + Weaknesses + Moat + Valuation) | Slot 4 | ~1.5 min |
| 5. Growth & Momentum | Slot 5 | ~45 sec |
| 6. Investors | Slot 6 | ~30 sec |
| 7. Risks | Slot 7 | ~1.5 min — anchor on the key risk(s) |
| 9. Appendix (e.g., "Why SPAC not private") | Slot 8 (if present) | ~45 sec |
| (Hand to IC) | Close | ~30 sec — outstanding diligence, IC questions to weigh |

## Variant B — 25-30 min Slide-by-Slide Narrative

- **Pairs with:** Gamma IC Deck (20 slides)
- **Length:** ~25–30 minutes / ~3,000–4,000 spoken words
- **Structure:** One spoken section per deck slide (20 sections), each 150–200 words
- **Filename:** `{output_folder}/YYYY MM DD {Company} IC Narrative.md`
- **Use when:** The user requests a detailed deck walk-through, or when the IC will spend significant time on the deck visuals during the meeting.

## Format

Markdown file. One section per slide, numbered to match the deck.

### Structure per slide

```markdown
### Slide N: {Slide Title}

[SPEAKER:]
"{Verbatim script — written as natural spoken language, exactly as the presenter
would say it aloud. 150-200 words per slide. Include pauses, rhetorical questions,
and emphasis. This is not a summary — it is what the person reads/says.}"

**Key point to land:** {One sentence the audience must remember from this slide.}

---
```

### Example (correct — spoken script)

> ### Slide 13: Implied Valuation
>
> [SPEAKER:]
> "So here's where it gets uncomfortable. At two point one billion, Clip is trading at eight and a half times gross revenue. The median for public LatAm payment comps is two times. That's a two hundred and thirty percent premium. Now — the strategic investors are clearly pricing something the public market doesn't see yet: the consumer wallet optionality. But for us, buying at this level with a two-to-three year horizon, the margin of safety is thin. If we could get in at one and a half billion, this becomes a very different conversation."
>
> **Key point to land:** The current valuation prices in near-perfect execution — there's no room for stumbles.

### Example (WRONG — written summary, do NOT do this)

> ~~Clip trades at 8.5x EV/Rev, a 230% premium to the median of 2.01x. The implied fair value range is $418M–$868M. Strategic investors may be pricing consumer wallet optionality.~~

## Tone

Conversational, confident, direct. First person plural ("we looked at...", "our view is...", "what concerned us..."). The speaker is walking colleagues through the case for the committee to decide — not reading a document, and not delivering a recommendation. Use natural speech patterns — contractions, rhetorical questions, emphasis markers.

## Rules **[Low freedom]**

- **This is a script, not a summary** — write it as spoken words. If it sounds wrong read aloud, rewrite it.
- **Never repeat slide text verbatim** — the audience can read. The speaker adds what they can't see.
- **Lead with the "so what"** — don't build up to the point, start with it.
- **Flag surprises and red flags explicitly** — "This is the number that concerned us most..."
- **Transition between slides** — end each section with a natural bridge to the next ("So that's the market. Now let's look at what Clip is actually delivering financially...")
- **Time guide:** ~60-90 seconds of speaking per slide = ~150-200 words per slide. Total script for 20 slides ≈ 3,000-4,000 words. The full presentation should take ~25-30 minutes to deliver.
- **Mark decision points** — where the IC needs to weigh in: "This is where we'd like the committee's view on..."
- **No recommendation, no verdict, no conviction rating.** The final slide script must NOT state a Proceed / Wait / Pass verdict, conviction rating, position-sizing recommendation, or "We recommend..." language. Close by laying out the decision inputs (deal mechanics, verified numbers, open structural items, key conditions) and explicitly handing the call to the committee. Same principle as the Express Memo: present the inputs cleanly; the committee decides. The full memo (Section 9) retains the conviction rating for those who want it. Acceptable closing patterns: "The committee has the inputs — the floor is yours" / "These are the open structural items — the decision is yours" / "Happy to dig into any section before you weigh in."
- **Cover the introducer / counterparty.** Slide 3 (Deal Overview, Variant B) or Slot 2 (Deal Terms, Variant A) must name who brought the deal and flag the introducer's economic interest — or its absence — as a confirmation item, even if the visual deck doesn't have a dedicated panel for it.
- **No AI-provenance language.** Drop "Status: Draft — pending human review" from the header. Use natural analyst phrasing throughout — "we confirmed", "the data shows", "independent sources cite" — not "the verifier found" or "the agent confirmed". Verification claims are fine as analyst rigor; process language is not.
- **Include stage directions where useful** — e.g., "[pause]", "[point to table row]", "[advance to next slide]"

## Source Material

The narrative draws from BOTH the IC deck (slide structure, visual flow) AND the full investment memo (deeper analysis, data, nuance). The deck provides the visual skeleton the audience sees; the memo provides the depth the speaker delivers verbally. The speaker should reference specific data, risks, and context from the memo that the slides necessarily compress or omit — this is where the value of the spoken presentation lies.

## Execution

Generate the narrative AFTER the Gamma deck is created. Use `mcp__claude_ai_Gamma__read_gamma` to read the actual slide titles and content, AND re-read the full investment memo. Write the script by walking through the deck slide-by-slide while pulling in deeper analysis, context, and judgment from the memo that the slides don't show.

## Graceful Degradation

- If Gamma MCP not connected → skip, inform user
- If PPTX generation fails → warn user, continue with memo PDF + Notion
- If PDF generation fails → deliver PPTX only, user can export PDF from gamma.app
- If `curl` download fails → report `exportUrl` directly for manual download
- Gamma is an enhancement, not core — pipeline must never fail because Gamma is down
