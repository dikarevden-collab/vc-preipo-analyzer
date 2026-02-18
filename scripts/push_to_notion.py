#!/usr/bin/env python3
"""Push a markdown memo to an existing Notion page as formatted blocks.

Usage:
    python scripts/push_to_notion.py <page_id> <memo_file> --token <NOTION_TOKEN>

Converts markdown headings, paragraphs, bullet lists, tables, and dividers
into Notion block API format and appends them to the page.

Notion API limit: 100 blocks per request, so content is batched.
"""

import sys
import re
import json
import argparse
import io

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

try:
    import requests
except ImportError:
    print("ERROR: requests not installed. Run: pip install requests", file=sys.stderr)
    sys.exit(1)

NOTION_API = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"
MAX_BLOCKS_PER_REQUEST = 100
MAX_TEXT_LENGTH = 2000  # Notion rich_text limit per element


def rich_text(content: str, bold: bool = False, italic: bool = False, code: bool = False) -> list:
    """Create rich_text array, splitting content if it exceeds 2000 chars."""
    chunks = []
    while content:
        chunk = content[:MAX_TEXT_LENGTH]
        content = content[MAX_TEXT_LENGTH:]
        rt = {"type": "text", "text": {"content": chunk}}
        annotations = {}
        if bold:
            annotations["bold"] = True
        if italic:
            annotations["italic"] = True
        if code:
            annotations["code"] = True
        if annotations:
            rt["annotations"] = annotations
        chunks.append(rt)
    return chunks


def parse_inline(text: str) -> list:
    """Parse inline markdown formatting (bold, italic, code) into rich_text segments."""
    segments = []
    # Pattern: **bold**, *italic*, `code`
    pattern = re.compile(r'(\*\*(.+?)\*\*|\*(.+?)\*|`(.+?)`)')
    pos = 0
    for m in pattern.finditer(text):
        # Add plain text before match
        if m.start() > pos:
            segments.extend(rich_text(text[pos:m.start()]))
        if m.group(2):  # bold
            segments.extend(rich_text(m.group(2), bold=True))
        elif m.group(3):  # italic
            segments.extend(rich_text(m.group(3), italic=True))
        elif m.group(4):  # code
            segments.extend(rich_text(m.group(4), code=True))
        pos = m.end()
    # Remaining text
    if pos < len(text):
        segments.extend(rich_text(text[pos:]))
    if not segments:
        segments = rich_text(text)
    return segments


def md_to_blocks(md_content: str) -> list:
    """Convert markdown content to Notion block objects."""
    blocks = []
    lines = md_content.split("\n")
    i = 0
    in_table = False
    table_rows = []

    while i < len(lines):
        line = lines[i]

        # Skip empty lines
        if not line.strip():
            i += 1
            continue

        # Divider
        if line.strip() == "---":
            blocks.append({"type": "divider", "divider": {}})
            i += 1
            continue

        # Headings
        if line.startswith("### "):
            blocks.append({
                "type": "heading_3",
                "heading_3": {"rich_text": parse_inline(line[4:].strip())}
            })
            i += 1
            continue

        if line.startswith("## "):
            blocks.append({
                "type": "heading_2",
                "heading_2": {"rich_text": parse_inline(line[3:].strip())}
            })
            i += 1
            continue

        if line.startswith("# "):
            blocks.append({
                "type": "heading_1",
                "heading_1": {"rich_text": parse_inline(line[2:].strip())}
            })
            i += 1
            continue

        # Table detection
        if "|" in line and line.strip().startswith("|"):
            # Collect all table rows
            table_rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                row = lines[i].strip()
                # Skip separator rows (|---|---|)
                if re.match(r'^[\|\s\-:]+$', row):
                    i += 1
                    continue
                cells = [c.strip() for c in row.split("|")[1:-1]]
                table_rows.append(cells)
                i += 1

            if table_rows:
                # Create table block
                width = max(len(r) for r in table_rows)
                # Pad rows to consistent width
                for r in table_rows:
                    while len(r) < width:
                        r.append("")

                table = {
                    "type": "table",
                    "table": {
                        "table_width": width,
                        "has_column_header": True,
                        "has_row_header": False,
                        "children": []
                    }
                }
                for row in table_rows:
                    table_row = {
                        "type": "table_row",
                        "table_row": {
                            "cells": [parse_inline(cell) if cell else rich_text("") for cell in row]
                        }
                    }
                    table["table"]["children"].append(table_row)
                blocks.append(table)
            continue

        # Bullet list items
        if line.strip().startswith("- ") or line.strip().startswith("* "):
            text = line.strip()[2:]
            blocks.append({
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": parse_inline(text)}
            })
            i += 1
            continue

        # Numbered list items
        if re.match(r'^\d+\.\s', line.strip()):
            text = re.sub(r'^\d+\.\s', '', line.strip())
            blocks.append({
                "type": "numbered_list_item",
                "numbered_list_item": {"rich_text": parse_inline(text)}
            })
            i += 1
            continue

        # Checkbox items
        if line.strip().startswith("- [ ] ") or line.strip().startswith("- [x] "):
            checked = line.strip().startswith("- [x] ")
            text = line.strip()[6:]
            blocks.append({
                "type": "to_do",
                "to_do": {
                    "rich_text": parse_inline(text),
                    "checked": checked
                }
            })
            i += 1
            continue

        # Blockquote
        if line.strip().startswith("> "):
            text = line.strip()[2:]
            blocks.append({
                "type": "quote",
                "quote": {"rich_text": parse_inline(text)}
            })
            i += 1
            continue

        # Regular paragraph
        blocks.append({
            "type": "paragraph",
            "paragraph": {"rich_text": parse_inline(line.strip())}
        })
        i += 1

    return blocks


def append_blocks(page_id: str, blocks: list, token: str):
    """Append blocks to a Notion page in batches of 100."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json"
    }

    total = len(blocks)
    sent = 0

    for batch_start in range(0, total, MAX_BLOCKS_PER_REQUEST):
        batch = blocks[batch_start:batch_start + MAX_BLOCKS_PER_REQUEST]
        resp = requests.patch(
            f"{NOTION_API}/blocks/{page_id}/children",
            headers=headers,
            json={"children": batch}
        )

        if resp.status_code == 200:
            sent += len(batch)
            print(f"  Appended blocks {batch_start + 1}-{batch_start + len(batch)} of {total}", file=sys.stderr)
        else:
            print(f"  ERROR at batch starting {batch_start}: {resp.status_code} — {resp.text[:500]}", file=sys.stderr)
            # Try to identify the problematic block
            if resp.status_code == 400:
                # Try sending blocks one by one to find the problem
                for j, block in enumerate(batch):
                    single_resp = requests.patch(
                        f"{NOTION_API}/blocks/{page_id}/children",
                        headers=headers,
                        json={"children": [block]}
                    )
                    if single_resp.status_code == 200:
                        sent += 1
                    else:
                        print(f"  Skipped block {batch_start + j + 1} (type: {block.get('type', '?')}): {single_resp.text[:200]}", file=sys.stderr)

    print(f"\nDone: {sent}/{total} blocks appended to page {page_id}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Push markdown memo to Notion page")
    parser.add_argument("page_id", help="Notion page ID")
    parser.add_argument("memo_file", help="Path to markdown memo file")
    parser.add_argument("--token", required=True, help="Notion API token")
    args = parser.parse_args()

    with open(args.memo_file, "r", encoding="utf-8") as f:
        md_content = f.read()

    print(f"Converting memo to Notion blocks...", file=sys.stderr)
    blocks = md_to_blocks(md_content)
    print(f"Generated {len(blocks)} blocks from {len(md_content)} chars", file=sys.stderr)

    append_blocks(args.page_id, blocks, args.token)
    print(f"\nPage URL: https://www.notion.so/{args.page_id.replace('-', '')}", file=sys.stderr)


if __name__ == "__main__":
    main()
