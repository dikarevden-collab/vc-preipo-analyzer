#!/usr/bin/env python3
"""Extract text from PDF files.

Usage:
    python scripts/extract_pdf.py <file.pdf> [--pages 1-5] [--max-chars 50000]

Examples:
    python scripts/extract_pdf.py "data-room/Executive Summary.pdf"
    python scripts/extract_pdf.py pitch-deck.pdf --pages 1-10
    python scripts/extract_pdf.py financials.pdf --max-chars 30000

Requires: pip install PyPDF2
"""

import sys
import io
import argparse

# Fix Windows Unicode output
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

try:
    from PyPDF2 import PdfReader
except ImportError:
    print("ERROR: PyPDF2 not installed. Run: pip install PyPDF2", file=sys.stderr)
    sys.exit(1)


def parse_page_range(page_str: str, total_pages: int) -> list[int]:
    """Parse page range like '1-5' or '3' into list of 0-indexed page numbers."""
    pages = []
    for part in page_str.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            start = max(1, int(start))
            end = min(total_pages, int(end))
            pages.extend(range(start - 1, end))
        else:
            p = int(part) - 1
            if 0 <= p < total_pages:
                pages.append(p)
    return pages


def main():
    parser = argparse.ArgumentParser(description="Extract text from PDF")
    parser.add_argument("file", help="Path to PDF file")
    parser.add_argument("--pages", help="Page range (e.g., '1-5', '3,7-10')")
    parser.add_argument("--max-chars", type=int, default=100000,
                        help="Maximum characters to output (default: 100000)")
    args = parser.parse_args()

    try:
        reader = PdfReader(args.file)
    except Exception as e:
        print(f"ERROR: Cannot read PDF: {e}", file=sys.stderr)
        sys.exit(1)

    total_pages = len(reader.pages)
    print(f"PDF: {args.file} — {total_pages} pages", file=sys.stderr)

    if args.pages:
        page_indices = parse_page_range(args.pages, total_pages)
    else:
        page_indices = list(range(total_pages))

    output = []
    chars = 0
    for i in page_indices:
        try:
            text = reader.pages[i].extract_text() or ""
            header = f"\n--- Page {i + 1} ---\n"
            if chars + len(header) + len(text) > args.max_chars:
                remaining = args.max_chars - chars - len(header)
                if remaining > 100:
                    output.append(header)
                    output.append(text[:remaining])
                    output.append(f"\n[TRUNCATED at {args.max_chars} chars — {total_pages - i - 1} pages remaining]")
                break
            output.append(header)
            output.append(text)
            chars += len(header) + len(text)
        except Exception as e:
            output.append(f"\n--- Page {i + 1} ---\n[ERROR extracting page: {e}]\n")

    print("".join(output))
    print(f"\nExtracted {len(page_indices)} pages, {chars} characters", file=sys.stderr)


if __name__ == "__main__":
    main()
