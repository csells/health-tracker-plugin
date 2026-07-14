#!/bin/bash
# Convert an HTML file to PDF using whatever engine is available.
#
# Tries several engines in order because this runs in different places: a Linux
# sandbox (Cowork), macOS (Claude Code / desktop), etc. If none is present it
# fails loudly and leaves the HTML in place -- the HTML opens in any browser and
# prints to PDF from there, so a missing engine is not a lost report.
set -euo pipefail

INPUT="${1:-}"
OUTPUT="${2:-}"

if [ -z "$INPUT" ] || [ -z "$OUTPUT" ]; then
  echo "Usage: html_to_pdf.sh <input.html> <output.pdf>" >&2
  exit 2
fi
if [ ! -f "$INPUT" ]; then
  echo "Input HTML not found: $INPUT" >&2
  exit 2
fi

# Candidate Chromium/Chrome binaries across platforms.
CHROME_CANDIDATES=(
  "chromium" "chromium-browser" "google-chrome" "google-chrome-stable"
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
  "/Applications/Chromium.app/Contents/MacOS/Chromium"
)

try_chrome() {
  local bin
  for bin in "${CHROME_CANDIDATES[@]}"; do
    if command -v "$bin" >/dev/null 2>&1 || [ -x "$bin" ]; then
      if "$bin" --headless --disable-gpu --no-sandbox \
           --print-to-pdf="$OUTPUT" "$INPUT" >/dev/null 2>&1; then
        echo "PDF generated with Chrome/Chromium: $OUTPUT"
        return 0
      fi
    fi
  done
  return 1
}

try_wkhtmltopdf() {
  if command -v wkhtmltopdf >/dev/null 2>&1; then
    if wkhtmltopdf --quiet "$INPUT" "$OUTPUT" >/dev/null 2>&1; then
      echo "PDF generated with wkhtmltopdf: $OUTPUT"
      return 0
    fi
  fi
  return 1
}

try_weasyprint() {
  if command -v weasyprint >/dev/null 2>&1; then
    if weasyprint "$INPUT" "$OUTPUT" >/dev/null 2>&1; then
      echo "PDF generated with WeasyPrint: $OUTPUT"
      return 0
    fi
  fi
  # Also try the Python module form.
  if python3 -c "import weasyprint" >/dev/null 2>&1; then
    if python3 -m weasyprint "$INPUT" "$OUTPUT" >/dev/null 2>&1; then
      echo "PDF generated with WeasyPrint (module): $OUTPUT"
      return 0
    fi
  fi
  return 1
}

if try_chrome || try_wkhtmltopdf || try_weasyprint; then
  exit 0
fi

echo "No PDF engine found (looked for Chrome/Chromium, wkhtmltopdf, WeasyPrint)." >&2
echo "The HTML report is ready and unmodified: $INPUT" >&2
echo "Open it in any browser and use Print > Save as PDF." >&2
exit 3
