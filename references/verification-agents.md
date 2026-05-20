# Verification Agents

Three verification passes are defined: (1) full-memo verifier (initial fresh fact-check), (2) express-memo drift-checker (delta vs. full memo + spot-check), and (3) follow-on edit verifier (for any post-pipeline modification).

**Core rule:** Every research operation — initial generation AND any subsequent edit, update, addition, or correction — MUST conclude with an independent fact-check. Self-verification by the producing agent is not verification. This rule is enforced in the parent SKILL.md and is non-negotiable.

## Table of Contents

- [Full Memo Verification Agent](#full-memo-verification-agent)
- [Focused Verification on Express Memo](#focused-verification-on-express-memo)
- [Follow-on Edit Verifier (mandatory concluding step for all edits)](#follow-on-edit-verifier-mandatory-concluding-step-for-all-edits)

## Full Memo Verification Agent

After the memo draft is written and before PDF/Notion export, launch an **independent verification agent** (`Agent` tool, subagent_type: `general-purpose`) that audits the memo for factual accuracy.

### Agent Briefing Template

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

### Integration Rules **[Low freedom]**

- The verifier agent runs in the **foreground** — wait for results before proceeding
- Append the verification report to the memo as a new section before the Sources Appendix
- If any claim is **DISPUTED**, flag it inline in the memo with `[DISPUTED — verifier found: {X}]` and let the analyst (user) decide whether to correct
- If Accuracy Score < 80%, warn the user before proceeding to PDF/Notion
- The verifier must use **fresh web searches** — it must not rely on the research agent's earlier findings

## Focused Verification on Express Memo

After the express memo is drafted, run a **focused verification pass** (`Agent` tool, subagent_type: `general-purpose`) to catch distillation drift before delivery. This is lighter-weight than the full-memo verification because facts have already been verified once.

### Agent Briefing Template

> You are a drift-check fact-verifier reviewing the express memo at {express_memo_path}. The full memo at {full_memo_path} has already been independently verified at {accuracy_score}% accuracy.
>
> Your job is **not** to re-verify every fact. Your job is to catch:
> 1. **Distillation drift** — any number, date, name, or claim in the express memo that does not appear (with the same value) in the full memo
> 2. **Stale data** — any time-sensitive fact (valuation, stock price, market cap, leadership role) where >30 days have passed since the full memo was verified. Spot-check 5-10 of the most-cited numbers on the current public web
> 3. **Forbidden content** — flag any Recommendation / Conviction / Buy-Hold-Pass / position-sizing / escalation-trigger language in the Express Memo. By policy, the Express Memo does not carry a recommendation; if any such section or line is present, flag it for removal before delivery.
>
> Output format:
>
> ```
> ## Express Memo Drift Check
> **Verified:** {date}
> **Full memo accuracy baseline:** {score}%
>
> ### Drift Issues Found
> - {issue} — express memo says: {X}. Full memo says: {Y}. Action: {correct in express memo}
>
> ### Stale Data Flags
> - {fact} — full memo verified {date}; current web shows {Y}. Action: {update or flag}
>
> ### Contradictions
> - {none / list}
>
> ### Drift Score: {clean_facts / total_facts} %
> ```
>
> If any drift, stale flag, or contradiction is found, apply the correction in-line in the express memo before delivery. If drift score < 95%, also warn the user.
>
> Be efficient — this pass should take <10 minutes. Do not re-verify items that match the full memo. Focus on differences and stale time-sensitive items.

### Integration Rules **[Low freedom]**

- Run in foreground; wait for results before generating express memo PDF
- Apply corrections in-line silently if minor (rounded number, dropped qualifier)
- If drift score <95% OR a contradiction is found, surface to the user before PDF generation
- The drift-check report does NOT need to be appended to the express memo (unlike the full-memo verification report) — its value is upstream, not downstream

## Follow-on Edit Verifier (mandatory concluding step for all edits)

Whenever a memo, Express Memo, IC Brief, or any other deliverable is **modified** after the initial pipeline has run — whether to add a section, fix an error, update a number, incorporate a follow-up question, or refresh stale data — an independent fact-check agent MUST run as the concluding step. This is mandatory under the rule defined in SKILL.md.

### When to trigger

- User asks to add, update, fix, refresh, expand, or correct any factual content in a memo
- A new section is added (e.g., funding rounds history, customer list)
- An assertion is changed (e.g., who led which round)
- Numbers are updated (e.g., refreshed ARR, new round close)
- Cross-memo consistency is checked

### Agent Briefing Template

> You are an independent fact-checker. The user has just had me modify the following deliverable(s):
> - {memo_path_1}
> - {memo_path_2}
>
> The specific changes made are:
> {bulleted summary of what was added/changed}
>
> Your job is to **independently verify** every factual claim in the modified content using fresh web searches against primary sources (company press releases, SEC filings, reputable news, Crunchbase, PitchBook citations).
>
> Specifically verify:
> 1. **Dates** (round close dates, contract dates, hire dates) — match official PR/filings
> 2. **Amounts** (round sizes, contract values, valuations) — match official PR
> 3. **Named entities** (lead investors, participants, customers, partners) — match official PR
> 4. **Quantitative claims** (growth rates, market shares, ARR, employee counts) — match cited sources
> 5. **Cross-memo consistency** — same fact stated consistently across all memos that mention it
>
> Output format:
>
> ```
> ## Follow-on Edit Verification Report
> **Verified:** {date}
> **Deliverables checked:** {list}
> **Claims checked:** {N}
>
> ### Findings (per claim)
> - [{CONFIRMED|DISPUTED|UNVERIFIED}] {claim} — Source: {URL} — Confidence: {High|Medium|Low}
>
> ### Discrepancies vs. memo content
> | Memo claim | Verified | Issue |
> |---|---|---|
> | {what memo says} | {what sources say} | {nature of issue} |
>
> ### Cross-memo consistency check
> - {fact}: stated as {X} in {memo1}, {Y} in {memo2} → {consistent | INCONSISTENT — fix needed}
>
> ### Confidence summary
> - High: {count}
> - Medium: {count}
> - Low / Unverified: {count}
>
> ### Recommended actions
> 1. {specific fix to apply, with file + line ref if possible}
> ```

### Integration Rules **[Low freedom — never skip]**

- Spawn the agent via `Agent` tool with `subagent_type: general-purpose`
- The agent must perform **fresh web searches** — it must not be given the producing agent's research log
- Run in foreground; wait for the report before declaring the edit "complete"
- For every `DISPUTED` finding, apply the correction in-line in the memo before reporting completion to the user
- For every `UNVERIFIED` finding, mark the claim in the memo as `UNVERIFIED — pending data-room confirmation` rather than removing or claiming verification
- Surface the verification report to the user as part of the completion summary
- This rule has NO exceptions. Even single-word factual edits trigger it. The cost of running a fact-check is small; the cost of an unverified factual error in an IC memo is large.
