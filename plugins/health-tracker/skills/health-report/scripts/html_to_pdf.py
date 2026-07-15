#!/usr/bin/env python3
"""Convert an HTML file to PDF using whatever engine is available.

Cross-platform (macOS, Linux, Windows) and Python-stdlib only, so it runs
anywhere the rest of this plugin does — no bash required, which matters on
Windows where the old html_to_pdf.sh could not run at all.

It tries headless Chrome/Chromium/Edge, then wkhtmltopdf, then WeasyPrint. If
none is present it fails loudly (exit 3) and leaves the HTML untouched — the HTML
opens in any browser and prints to PDF from there, so a missing engine is not a
lost report. It never silently produces nothing.

Usage:  python3 html_to_pdf.py <input.html> <output.pdf>
        (on Windows use `python html_to_pdf.py ...` or `py -3 html_to_pdf.py ...`)
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


def _chrome_candidates() -> list[str]:
    """Chrome/Chromium/Edge locations across platforms, PATH first."""
    names = [
        "chromium", "chromium-browser", "google-chrome", "google-chrome-stable",
        "chrome", "msedge", "microsoft-edge",
    ]
    found = [p for n in names if (p := shutil.which(n))]

    # Known install paths not always on PATH.
    program_files = [
        os.environ.get("PROGRAMFILES", r"C:\Program Files"),
        os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)"),
        os.environ.get("LOCALAPPDATA", ""),
    ]
    explicit = [
        # macOS
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    ]
    for base in program_files:
        if not base:
            continue
        explicit += [
            str(Path(base) / "Google/Chrome/Application/chrome.exe"),
            str(Path(base) / "Microsoft/Edge/Application/msedge.exe"),
            str(Path(base) / "Chromium/Application/chrome.exe"),
        ]

    for path in explicit:
        if Path(path).is_file():
            found.append(path)
    return found


def _try_chrome(input_html: str, output_pdf: str) -> bool:
    src = Path(input_html).resolve().as_uri()
    for binary in _chrome_candidates():
        try:
            result = subprocess.run(
                [binary, "--headless", "--disable-gpu", "--no-sandbox",
                 f"--print-to-pdf={output_pdf}", src],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
        except (OSError, subprocess.SubprocessError):
            continue
        if result.returncode == 0 and Path(output_pdf).is_file():
            print(f"PDF generated with Chrome/Chromium/Edge: {output_pdf}")
            return True
    return False


def _try_cmd(engine: str, args: list[str], output_pdf: str, label: str) -> bool:
    if not shutil.which(engine):
        return False
    try:
        result = subprocess.run(args, stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)
    except (OSError, subprocess.SubprocessError):
        return False
    if result.returncode == 0 and Path(output_pdf).is_file():
        print(f"PDF generated with {label}: {output_pdf}")
        return True
    return False


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("Usage: html_to_pdf.py <input.html> <output.pdf>", file=sys.stderr)
        return 2
    input_html, output_pdf = argv[1], argv[2]
    if not Path(input_html).is_file():
        print(f"Input HTML not found: {input_html}", file=sys.stderr)
        return 2

    if (_try_chrome(input_html, output_pdf)
            or _try_cmd("wkhtmltopdf", ["wkhtmltopdf", "--quiet", input_html, output_pdf],
                        output_pdf, "wkhtmltopdf")
            or _try_cmd("weasyprint", ["weasyprint", input_html, output_pdf],
                        output_pdf, "WeasyPrint")):
        return 0

    print("No PDF engine found (looked for Chrome/Chromium/Edge, wkhtmltopdf, "
          "WeasyPrint).", file=sys.stderr)
    print(f"The HTML report is ready and unmodified: {input_html}", file=sys.stderr)
    print("Open it in any browser and use Print > Save as PDF.", file=sys.stderr)
    return 3


if __name__ == "__main__":
    sys.exit(main(sys.argv))
