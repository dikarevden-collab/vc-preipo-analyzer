#!/bin/bash
# Single-company secondary pricing scraper for vc-preipo-analyzer
# Uses agent-browser to search Forge, Caplight, and Hiive for a given company
# Usage: bash fetch_secondary_prices.sh "Company Name"
# Requires: agent-browser connected to Chrome debug profile on port 9222
# Output: JSON to stdout with prices from each platform

set +e  # Don't abort on individual command failures

COMPANY="$1"
if [ -z "$COMPANY" ]; then
  echo '{"error": "Usage: fetch_secondary_prices.sh \"Company Name\""}' >&2
  exit 1
fi

SLUG=$(echo "$COMPANY" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | sed 's/[^a-z0-9-]//g')

# Windows-compatible temp file
REAL_TEMP=$(python3 -c "import tempfile; print(tempfile.gettempdir())")
RESULTS_FILE="${REAL_TEMP}/secondary_prices_$$.json"
echo '{}' > "$RESULTS_FILE"

CHROME_PORT=9222
CHROME_EXE="/c/Program Files/Google/Chrome/Application/chrome.exe"
CHROME_DATA="C:\\Users\\denis\\.chrome-debug"

# Helper: random delay between min and max seconds
delay() {
  local min=${1:-2} max=${2:-5}
  sleep $(( RANDOM % (max - min + 1) + min ))
}

# Helper: save result to JSON
save_result() {
  local platform="$1" price="$2" url="$3"
  python3 -c "
import json, sys
with open(r'$RESULTS_FILE','r') as f: d=json.load(f)
d['$platform'] = {'price': '$price', 'url': '$url'}
with open(r'$RESULTS_FILE','w') as f: json.dump(d,f,indent=2)
"
}

# Helper: extract @eN ref from a snapshot line
extract_ref() {
  echo "$1" | sed 's/.*\(@e[0-9]*\).*/\1/' | head -1
}

# Check agent-browser is available
if ! command -v agent-browser &> /dev/null; then
  echo '{"error": "agent-browser not installed. Run: npm i -g agent-browser"}' >&2
  exit 1
fi

# ========== Auto-launch Chrome debug profile if not running ==========
chrome_running() {
  curl -s "http://localhost:${CHROME_PORT}/json/version" > /dev/null 2>&1
}

if ! chrome_running; then
  echo "Launching Chrome debug profile on port $CHROME_PORT..." >&2
  "$CHROME_EXE" \
    --remote-debugging-port=$CHROME_PORT \
    --user-data-dir="$CHROME_DATA" \
    --profile-directory="Default" &
  # Wait for Chrome to start (up to 15 seconds)
  for i in $(seq 1 15); do
    sleep 1
    if chrome_running; then
      echo "Chrome ready." >&2
      break
    fi
    [ "$i" -eq 15 ] && echo "Warning: Chrome may not have started." >&2
  done
  delay 2 3
fi

# ========== Connect agent-browser ==========
echo "Connecting agent-browser to port $CHROME_PORT..." >&2
agent-browser connect $CHROME_PORT 2>/dev/null
delay 1 2

# ========== Helper: check if page is a login/auth wall ==========
# Returns 0 (true) if page appears to be logged in (not a login page)
is_logged_in() {
  local snap="$1"
  # If page contains login/sign-in indicators, we're NOT logged in
  if echo "$snap" | grep -qi 'Sign [Ii]n\|Log [Ii]n\|Enter your email\|Enter your password\|Create an account\|SSO\|forgot.password'; then
    return 1
  fi
  # If page is mostly empty or an error, we're NOT logged in
  local line_count=$(echo "$snap" | wc -l)
  if [ "$line_count" -lt 10 ]; then
    return 1
  fi
  return 0
}

# Wait for user to complete login in the Chrome window.
wait_for_login() {
  local platform="$1" timeout_sec="${2:-90}"
  local elapsed=0
  echo "$platform: Not logged in. Please log in via the Chrome window." >&2
  echo "$platform: Waiting up to ${timeout_sec}s for login..." >&2
  while [ $elapsed -lt $timeout_sec ]; do
    sleep 5
    elapsed=$((elapsed + 5))
    snap=$(agent-browser snapshot 2>/dev/null)
    if is_logged_in "$snap"; then
      echo "$platform: Login detected." >&2
      return 0
    fi
    echo "$platform: Still waiting... (${elapsed}s)" >&2
  done
  echo "$platform: Login timed out after ${timeout_sec}s." >&2
  return 1
}

# ========== FORGE (no login, direct URL with slug guess) ==========
echo "=== Forge: $COMPANY ===" >&2
forge_url="https://forgeglobal.com/${SLUG}_stock/"
agent-browser tab new "$forge_url" 2>/dev/null
agent-browser wait --load networkidle 2>/dev/null || sleep 5
delay 2 4

snap=$(agent-browser snapshot 2>/dev/null)
# Check if page exists (not 404)
if echo "$snap" | grep -q 'Forge Price'; then
  forge_price=$(echo "$snap" | grep -A6 'link "Forge Price"' | grep 'StaticText "\$[0-9]' | head -1 | sed 's/.*StaticText "\$\([0-9,\.]*\).*/\1/' | tr -d ',')
  [ -z "$forge_price" ] && forge_price="n/a"
else
  forge_price="n/a"
  # Try without hyphens in slug
  alt_slug=$(echo "$SLUG" | tr -d '-')
  if [ "$alt_slug" != "$SLUG" ]; then
    forge_url="https://forgeglobal.com/${alt_slug}_stock/"
    agent-browser tab close 2>/dev/null
    agent-browser tab new "$forge_url" 2>/dev/null
    agent-browser wait --load networkidle 2>/dev/null || sleep 5
    delay 2 4
    snap=$(agent-browser snapshot 2>/dev/null)
    if echo "$snap" | grep -q 'Forge Price'; then
      forge_price=$(echo "$snap" | grep -A6 'link "Forge Price"' | grep 'StaticText "\$[0-9]' | head -1 | sed 's/.*StaticText "\$\([0-9,\.]*\).*/\1/' | tr -d ',')
      [ -z "$forge_price" ] && forge_price="n/a"
    fi
  fi
  # Try with "-space-industries" suffix for Varda-style names
  if [ "$forge_price" = "n/a" ]; then
    forge_url="https://forgeglobal.com/${SLUG}-industries_stock/"
    agent-browser tab close 2>/dev/null
    agent-browser tab new "$forge_url" 2>/dev/null
    agent-browser wait --load networkidle 2>/dev/null || sleep 5
    delay 2 4
    snap=$(agent-browser snapshot 2>/dev/null)
    if echo "$snap" | grep -q 'Forge Price'; then
      forge_price=$(echo "$snap" | grep -A6 'link "Forge Price"' | grep 'StaticText "\$[0-9]' | head -1 | sed 's/.*StaticText "\$\([0-9,\.]*\).*/\1/' | tr -d ',')
      [ -z "$forge_price" ] && forge_price="n/a"
    fi
  fi
fi
echo "Forge: \$$forge_price" >&2
save_result "forge" "$forge_price" "$forge_url"
agent-browser tab close 2>/dev/null
delay 2 4

# ========== CAPLIGHT (requires login, snapshot-ref search) ==========
echo "=== Caplight: $COMPANY ===" >&2
agent-browser tab new "https://platform.caplight.com/market" 2>/dev/null
agent-browser wait --load networkidle 2>/dev/null || sleep 5
sleep 5

# Check login status
snap=$(agent-browser snapshot 2>/dev/null)
if ! is_logged_in "$snap"; then
  if ! wait_for_login "Caplight" 90; then
    echo "Caplight: skipping (not logged in)" >&2
    save_result "caplight" "n/a" "https://platform.caplight.com"
    agent-browser tab close 2>/dev/null
  fi
  # Re-snapshot after login
  snap=$(agent-browser snapshot -i 2>/dev/null)
fi

cap_url="https://platform.caplight.com"

# Search via Ctrl+K to open search modal
echo "Caplight: opening search modal (Ctrl+K)..." >&2
agent-browser press "Control+k" 2>/dev/null
sleep 3

# Snapshot to find the search input ref
snap=$(agent-browser snapshot -i 2>/dev/null)
search_ref=$(echo "$snap" | grep -iE 'textbox|search|input' | grep '@e' | head -1)
search_ref_id=$(echo "$search_ref" | sed 's/.*\(@e[0-9]*\).*/\1/')

if [ -n "$search_ref_id" ]; then
  echo "Caplight: found search input $search_ref_id, typing '$COMPANY'..." >&2
  agent-browser type "$search_ref_id" "$COMPANY" 2>/dev/null
  sleep 6  # wait for search API to return results

  # Snapshot to find the matching result
  snap=$(agent-browser snapshot -i 2>/dev/null)
  result_line=$(echo "$snap" | grep -i "$COMPANY" | grep '@e' | head -1)
  result_ref=$(echo "$result_line" | sed 's/.*\(@e[0-9]*\).*/\1/')

  if [ -n "$result_ref" ]; then
    echo "Caplight: clicking result $result_ref..." >&2
    agent-browser click "$result_ref" 2>/dev/null
    agent-browser wait --load networkidle 2>/dev/null || sleep 5
    sleep 5
  else
    # Fallback: ArrowDown + Enter to select first result
    echo "Caplight: no ref match, trying ArrowDown+Enter..." >&2
    agent-browser press "ArrowDown" 2>/dev/null
    sleep 1
    agent-browser press "Enter" 2>/dev/null
    agent-browser wait --load networkidle 2>/dev/null || sleep 5
    sleep 5
  fi
else
  # Fallback: try clicking a visible Search element via snapshot refs
  echo "Caplight: Ctrl+K modal not detected, looking for search element..." >&2
  search_elem=$(echo "$snap" | grep -iE '"Search"|search.*combobox' | grep '@e' | head -1)
  search_elem_ref=$(echo "$search_elem" | sed 's/.*\(@e[0-9]*\).*/\1/')
  if [ -n "$search_elem_ref" ]; then
    agent-browser click "$search_elem_ref" 2>/dev/null
    sleep 2
    snap=$(agent-browser snapshot -i 2>/dev/null)
    input_ref=$(echo "$snap" | grep -iE 'textbox|input' | grep '@e' | head -1 | sed 's/.*\(@e[0-9]*\).*/\1/')
    if [ -n "$input_ref" ]; then
      agent-browser type "$input_ref" "$COMPANY" 2>/dev/null
      sleep 6
      snap=$(agent-browser snapshot -i 2>/dev/null)
      result_ref=$(echo "$snap" | grep -i "$COMPANY" | grep '@e' | head -1 | sed 's/.*\(@e[0-9]*\).*/\1/')
      if [ -n "$result_ref" ]; then
        agent-browser click "$result_ref" 2>/dev/null
        agent-browser wait --load networkidle 2>/dev/null || sleep 5
        sleep 5
      fi
    fi
  fi
fi

snap=$(agent-browser snapshot 2>/dev/null)
cap_url=$(agent-browser url 2>/dev/null || echo "https://platform.caplight.com")
echo "Caplight: URL = $cap_url" >&2

# Check if we navigated to a company page (URL should change from /market)
if echo "$cap_url" | grep -q '/market$'; then
  echo "Caplight: search did not navigate to company page, staying on market table" >&2
  cap_price="n/a"
else
  # Extract price — try Caplight MarketPrice label first
  cap_price=$(echo "$snap" | grep -iA2 'Caplight.MarketPrice\|MarketPrice\|Market.Price' | grep 'StaticText "\$' | head -1 | sed 's/.*StaticText "\$\([0-9,\.]*\).*/\1/' | tr -d ',')
  if [ -z "$cap_price" ]; then
    cap_price=$(echo "$snap" | grep 'StaticText "\$[0-9]' | head -1 | sed 's/.*StaticText "\$\([0-9,\.]*\).*/\1/' | tr -d ',')
  fi
  [ -z "$cap_price" ] && cap_price="n/a"
fi

echo "Caplight: \$$cap_price" >&2
save_result "caplight" "$cap_price" "$cap_url"
agent-browser tab close 2>/dev/null
delay 2 4

# ========== HIIVE (requires login, snapshot-ref search) ==========
echo "=== Hiive: $COMPANY ===" >&2
agent-browser tab new "https://app.hiive.com/dashboard" 2>/dev/null
agent-browser wait --load networkidle 2>/dev/null || sleep 5
sleep 5

# Check login status
snap=$(agent-browser snapshot 2>/dev/null)
if ! is_logged_in "$snap"; then
  if ! wait_for_login "Hiive" 90; then
    echo "Hiive: skipping (not logged in)" >&2
    save_result "hiive" "n/a" "https://app.hiive.com"
    agent-browser tab close 2>/dev/null
  fi
  snap=$(agent-browser snapshot -i 2>/dev/null)
fi

# Snapshot to find search element
echo "Hiive: looking for search element..." >&2
snap=$(agent-browser snapshot -i 2>/dev/null)

# Try Ctrl+K first (primary search method)
echo "Hiive: opening search (Ctrl+K)..." >&2
agent-browser press "Control+k" 2>/dev/null
sleep 2

snap=$(agent-browser snapshot -i 2>/dev/null)
search_ref=$(echo "$snap" | grep -iE 'textbox|search.*input|combobox' | grep '@e' | head -1 | sed 's/.*\(@e[0-9]*\).*/\1/')

if [ -z "$search_ref" ]; then
  # Fallback: find and click "Search company" or similar element
  echo "Hiive: Ctrl+K not detected, looking for search combobox..." >&2
  search_elem=$(echo "$snap" | grep -iE '"Search company"|"Search"|combobox' | grep '@e' | head -1 | sed 's/.*\(@e[0-9]*\).*/\1/')
  if [ -n "$search_elem" ]; then
    agent-browser click "$search_elem" 2>/dev/null
    sleep 2
    snap=$(agent-browser snapshot -i 2>/dev/null)
    search_ref=$(echo "$snap" | grep -iE 'textbox|input' | grep '@e' | head -1 | sed 's/.*\(@e[0-9]*\).*/\1/')
  fi
fi

if [ -n "$search_ref" ]; then
  echo "Hiive: found search input $search_ref, typing '$COMPANY'..." >&2
  agent-browser type "$search_ref" "$COMPANY" 2>/dev/null
  sleep 6  # wait for search API to return results

  # Price is in the dropdown — snapshot to extract
  snap=$(agent-browser snapshot -i 2>/dev/null)
  echo "Hiive: extracting price from search dropdown..." >&2

  # Match link/option containing company name + price
  dropdown_match=$(echo "$snap" | grep -i "$COMPANY" | grep -E 'link|option|listitem' | head -1)
  echo "Hiive: dropdown match: $dropdown_match" >&2

  hiive_price=$(echo "$dropdown_match" | sed 's/.*\$\([0-9,\.]*\).*/\1/' | tr -d ',')
  [ -z "$hiive_price" ] && hiive_price="n/a"

  # If no price in dropdown, click result and extract from company page
  if [ "$hiive_price" = "n/a" ]; then
    result_ref=$(echo "$snap" | grep -i "$COMPANY" | grep '@e' | head -1 | sed 's/.*\(@e[0-9]*\).*/\1/')
    if [ -n "$result_ref" ]; then
      echo "Hiive: clicking result $result_ref to open company page..." >&2
      agent-browser click "$result_ref" 2>/dev/null
      agent-browser wait --load networkidle 2>/dev/null || sleep 5
      sleep 5
      snap=$(agent-browser snapshot 2>/dev/null)
      # Try HIIVE PRICE label
      hiive_price=$(echo "$snap" | grep -iA4 'HIIVE.PRICE' | grep 'StaticText "\$' | head -1 | sed 's/.*StaticText "\$\([0-9,\.]*\).*/\1/' | tr -d ',')
      # Fallback: HIGHEST BID
      if [ -z "$hiive_price" ]; then
        hiive_price=$(echo "$snap" | grep -iA4 'HIGHEST.BID' | grep 'StaticText "\$' | head -1 | sed 's/.*StaticText "\$\([0-9,\.]*\).*/\1/' | tr -d ',')
      fi
      [ -z "$hiive_price" ] && hiive_price="n/a"
    fi
  fi
else
  echo "Hiive: could not find search input" >&2
  hiive_price="n/a"
fi

hiive_url=$(agent-browser url 2>/dev/null || echo "https://app.hiive.com")
echo "Hiive: \$$hiive_price" >&2
save_result "hiive" "$hiive_price" "$hiive_url"
agent-browser tab close 2>/dev/null

# ========== Output final JSON to stdout ==========
echo "" >&2
echo "=== Results for $COMPANY ===" >&2
cat "$RESULTS_FILE" >&2

# Add metadata and output
python3 -c "
import json, datetime
with open(r'$RESULTS_FILE','r') as f: d=json.load(f)
d['company'] = '$COMPANY'
d['date'] = datetime.date.today().isoformat()
print(json.dumps(d, indent=2))
"

# Cleanup temp file
echo "Temp file at $RESULTS_FILE can be manually deleted." >&2
