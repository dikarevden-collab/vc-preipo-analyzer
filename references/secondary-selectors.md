# Secondary Platform Selectors & Search Flows

Reference for `scripts/fetch_secondary_prices.sh`. Describes how to search for any company on each platform and extract the current price.

## Forge Global (forgeglobal.com)

### Auth
- **No login required** — prices are public

### Navigation (search by slug)
- Try direct URL: `https://forgeglobal.com/{slug}_stock/` where slug = lowercase company name
- Common slug patterns: `spacex`, `revolut`, `bytedance`, `cerebras`, `kraken`
- If 404 → try without hyphens → if still 404 → company not on Forge, record "n/a"

### Price Extraction
- Label: `link "Forge Price"`
- Price: `StaticText "$102.62 "` following the Forge Price link
- Regex on snapshot: `grep -A6 'link "Forge Price"' | grep 'StaticText "\$[0-9]'`
- If price shows `$--` → not yet available, record "n/a"

---

## Caplight (platform.caplight.com)

### Auth Check
- Logged in if page does NOT contain sign-in/login/password indicators
- If not logged in → Chrome window prompts user; script waits up to 90s
- After login, script reloads `/market` page

### Search Flow (snapshot-ref workflow)
1. Navigate to `https://platform.caplight.com/market`
2. `agent-browser press "Control+k"` to open search modal (primary method)
3. `agent-browser snapshot -i` → find textbox/input ref (`@eN`)
4. `agent-browser type @eN "Company Name"` → wait for results
5. `agent-browser snapshot -i` → find result ref matching company name
6. `agent-browser click @eN` → navigates to company page
7. Fallback: if no ref match, `press ArrowDown` → `press Enter`

### Price Extraction
- Label: `StaticText "Caplight MarketPrice™"`
- Price: next `StaticText` starting with `$` (e.g., `StaticText "$97.18"`)
- Regex on snapshot: `grep -A2 'Caplight MarketPrice' | grep 'StaticText "\$'`

---

## Hiive (app.hiive.com)

### Auth Check
- Logged in if page does NOT contain sign-in/login/password indicators
- If not logged in → Chrome window prompts user; script waits up to 90s
- After login, script reloads `/dashboard` page

### Search Flow (snapshot-ref workflow)
1. Navigate to `https://app.hiive.com/dashboard`
2. `agent-browser press "Control+k"` to open search (primary method)
3. `agent-browser snapshot -i` → find textbox/combobox ref (`@eN`)
4. Fallback: find `"Search company"` combobox ref → `agent-browser click @eN`
5. `agent-browser type @eN "Company Name"` → wait for dropdown results
6. Extract price directly from dropdown text (format: `"Company $XX.XX +YY%"`)
7. If no price in dropdown: `agent-browser click @eN` on result → extract from company page

### Price Extraction
- Labels are ALL CAPS: `HIGHEST BID`, `LOWEST ASK`, `HIIVE PRICE`
- Primary: `HIIVE PRICE` → e.g., `$29.93`
- Fallback: `HIGHEST BID` → e.g., `$31.00`
- Regex on snapshot: `grep -iA4 'HIIVE.PRICE' | grep 'StaticText "\$'`
- Note: some companies have listings but no Hiive Price — use HIGHEST BID as fallback

---

## Prerequisites

- `agent-browser` CLI installed (`npm i -g agent-browser`)
- Chrome debug profile at `~/.chrome-debug` with Caplight + Hiive sessions active
- Launch Chrome before running: `"/c/Program Files/Google/Chrome/Application/chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\\Users\\denis\\.chrome-debug" --profile-directory="Default" &`
- Connect agent-browser: `agent-browser connect 9222`
