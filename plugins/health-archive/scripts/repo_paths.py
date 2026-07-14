"""Path resolution for the health-archive genome pipeline.

Two distinct roots, and keeping them separate is the whole point of this file:

  1. REFERENCE DATA ships *inside the plugin*. It is public third-party data
     (ClinVar, PharmGKB), identical for every user, and read-only. It is stored
     gzipped purely to fit hosting limits. Every row and every column of the
     original is preserved byte-for-byte -- nothing was filtered out. Python
     reads it through gzip.open() with no unzip step, so the compression is
     invisible to everything downstream.

  2. THE PERSON'S DATA lives in *their workspace* -- the folder they connected
     to Cowork. Their genome, their records, their reports. The pipeline reads
     the genome and writes reports there. It never writes into the plugin.

Change paths here and nowhere else.
"""

from __future__ import annotations

import gzip
import os
from pathlib import Path
from typing import IO

# --------------------------------------------------------------------------
# 1. Reference data (bundled with the plugin, read-only)
# --------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
PLUGIN_DIR = SCRIPT_DIR.parent
REFERENCE_DIR = PLUGIN_DIR / "reference"

# The analysis scripts import this name.
DATA_DIR = REFERENCE_DIR


def data_file(name: str) -> Path:
    """Resolve a reference dataset, preferring the gzipped copy.

    Accepts "clinvar_alleles.tsv" or "clinvar_alleles.tsv.gz" and returns
    whichever exists, so someone who drops in a fresh uncompressed download
    from ClinVar or PharmGKB keeps working with no code change.
    """
    plain = REFERENCE_DIR / name.removesuffix(".gz")
    gzipped = REFERENCE_DIR / (plain.name + ".gz")

    if gzipped.exists():
        return gzipped
    if plain.exists():
        return plain

    raise FileNotFoundError(
        f"Reference dataset '{plain.name}' not found in {REFERENCE_DIR}.\n"
        "The plugin ships this data, so a missing file means the install is "
        "incomplete. Reinstall the plugin from the marketplace."
    )


def open_data(path: Path, encoding: str = "utf-8") -> IO[str]:
    """Open a data file for reading, transparently decompressing .gz.

    Streams row by row exactly like a plain open(); nothing is expanded to disk
    and memory use is unchanged.
    """
    if path.suffix == ".gz":
        return gzip.open(path, "rt", encoding=encoding, newline="")
    return open(path, "r", encoding=encoding, newline="")


# --------------------------------------------------------------------------
# 2. The person's workspace (the folder they connected to Cowork)
# --------------------------------------------------------------------------

WORKSPACE_MARKER = ".health-archive"


def find_workspace() -> Path:
    """Locate the health archive workspace.

    Resolution order, most explicit first:
      1. $HEALTH_ARCHIVE_WORKSPACE
      2. nearest parent directory holding a .health-archive marker
      3. nearest parent directory holding a records/ directory
      4. the current directory
    """
    env = os.environ.get("HEALTH_ARCHIVE_WORKSPACE")
    if env:
        return Path(env).expanduser().resolve()

    cwd = Path.cwd().resolve()
    for candidate in (cwd, *cwd.parents):
        if (candidate / WORKSPACE_MARKER).exists():
            return candidate
    for candidate in (cwd, *cwd.parents):
        if (candidate / "records").is_dir():
            return candidate

    return cwd


def require_workspace() -> Path:
    """Return the workspace, failing loudly if this isn't one."""
    ws = find_workspace()
    if not (ws / WORKSPACE_MARKER).exists() and not (ws / "records").is_dir():
        raise FileNotFoundError(
            f"No health archive found at {ws}.\n"
            "Expected a folder containing records/.\n"
            "If this is a new archive, ask Claude to 'set up my health archive' first."
        )
    return ws


WORKSPACE = find_workspace()

# Source of truth. Append-only; never written to by this pipeline.
RECORDS_DIR = WORKSPACE / "records"
RAW_GENOME_DIR = RECORDS_DIR / "genome"

# Machine-generated genome reports. Regenerable: safe to delete and rebuild.
REPORTS_DIR = WORKSPACE / "reports" / "genetics"


def ensure_reports_dir() -> Path:
    """Create the genome-reports output directory if needed, and return it."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    return REPORTS_DIR


DEFAULT_GENOME_HELP = "defaults to the single genome export in records/genome/"

# Genotyping exports arrive as .txt, and sometimes gzipped.
GENOME_PATTERNS = ("*.txt", "*.txt.gz", "*.tsv", "*.tsv.gz")


def find_default_genome_path() -> Path:
    """Locate the person's genome export in their workspace."""
    if not RAW_GENOME_DIR.exists():
        raise FileNotFoundError(
            f"No genome folder at {RAW_GENOME_DIR}.\n"
            "Put your raw DNA export (the .txt file from 23andMe or AncestryDNA) "
            "in records/genome/ and try again."
        )

    candidates = sorted(
        p
        for pattern in GENOME_PATTERNS
        for p in RAW_GENOME_DIR.glob(pattern)
        if p.is_file()
    )

    if not candidates:
        raise FileNotFoundError(
            f"No genome export found in {RAW_GENOME_DIR}.\n"
            "Expected a raw DNA export (.txt) from 23andMe or AncestryDNA. "
            "If you downloaded a .zip, unzip it first."
        )

    if len(candidates) == 1:
        return candidates[0]

    choices = "\n".join(f"  - {p.name}" for p in candidates)
    raise FileNotFoundError(
        "Multiple genome files found in records/genome/. Pass one explicitly:\n"
        f"{choices}"
    )
