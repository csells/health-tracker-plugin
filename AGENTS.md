# Shared Agent Guide

Canonical shared project instructions for Claude Code, Codex, and Gemini CLI. `CLAUDE.md` and
`GEMINI.md` import this file; keep guidance here unless it genuinely applies to only one tool.

## What this repo is

This repo is **the plugin, not the data**. It is a Claude Code / Cowork plugin distributed through a
marketplace manifest; users install it and then point it at a *separate* folder of their own — their
health workspace — which holds their medical records and DNA. Nothing personal ever lives here.

Two roots, and never confuse them:

| Root | What it is | Written by the pipeline? |
|---|---|---|
| **This repo** (`plugins/health-tracker/`) | Skills, Python scripts, and public reference data (ClinVar, PharmGKB). Same for every user. | **Never.** Read-only at runtime. |
| **The user's workspace** | Their `records/`, `reports/`, `PROFILE.md`. Found at runtime, not committed anywhere. | Yes — reports only. |

`scripts/repo_paths.py` is the **single place** both roots are resolved. Change paths there and
nowhere else.

## 🔴 This repo is PUBLIC — never commit anything about a real patient

Everything here is world-readable the moment it is pushed, and a push is cached and indexed
immediately. The plugin is developed against a **real person's** medical archive as test input,
which lives **outside this repo** and is **read-only**. That archive, and everything about the human
it belongs to, must never cross the boundary into this repo.

That means, in commits, code, comments, plans, and `specs/` alike:

- **No genome or genotype data.** Not a slice, not a sample, not "just a few rsids."
- **No records, reports, or output** generated from a real person's data.
- **No name, path, initials, or relationship** identifying whose data the test input is — this
  includes the directory name of the archive.
- **No findings attributed to an identifiable person.** "*N* pathogenic variants" is a harmless
  regression fixture; "*N* pathogenic variants **in <name>'s genome**" is a health disclosure about
  someone real. The number is fine; the attribution is what leaks.

This has bitten once already: a planning doc in `specs/` named the subject and attributed her
variant counts to her, and was committed. It was caught before the first push and purged from
history. **Internal artifacts still belong in `specs/`** — that rule stands — but write them as if a
stranger will read them, because one will.

Test only in **throwaway workspaces** (`mktemp -d`, a scratch folder). The real archive is never a
write target and never a copy source into this tree.

## Commands

There is **no test suite, no linter, and no CI** in this repo. Verification is running the real
pipeline against a real genome export (see below) and reading the reports it emits.

```bash
# Run the genome pipeline. MUST be run with the user's workspace as cwd (see gotcha below).
cd /path/to/user/health-workspace
python3 "$CLAUDE_PLUGIN_ROOT/scripts/run_full_analysis.py" --name "Their Name"
python3 /abs/path/to/plugins/health-tracker/scripts/run_full_analysis.py   # when CLAUDE_PLUGIN_ROOT is unset

# Smoke-test path resolution and gzip streaming without a genome:
python3 -c "import repo_paths as r; print(r.WORKSPACE, r.REPORTS_DIR, r.data_file('clinvar_alleles.tsv'))"

# HTML -> PDF (used by the health-report skill; tries Chrome, wkhtmltopdf, WeasyPrint in order)
bash plugins/health-tracker/skills/health-report/scripts/html_to_pdf.sh in.html out.pdf
```

**Shipping an update:** bump `version` in **both** `plugins/health-tracker/version.json` *and*
`plugins/health-tracker/.claude-plugin/plugin.json` — they must stay in sync — then commit and push.
Users click **Update** in the marketplace. You never touch their machine.

### ⚠️ The cwd gotcha

`repo_paths.find_workspace()` resolves the workspace in this order: `$HEALTH_TRACKER_WORKSPACE` → a
parent dir containing a `.health-tracker` marker → a parent dir containing `records/` → **the current
directory**. That last fallback means running `run_full_analysis.py` from inside `scripts/` will
happily create `scripts/reports/genetics/` *inside the plugin*. Always run it from the user's
workspace, or set `$HEALTH_TRACKER_WORKSPACE`.

## Architecture

**The skills are the product.** The Python is a subsystem that only one skill (`analyze-genome`)
invokes. Everything else — filing records, logging symptoms, building reports — is the model
following a SKILL.md, with no code behind it.

### Skills (`plugins/health-tracker/skills/`)

`setup-health-tracker` (interviews the user and scaffolds the workspace) · `file-records` ·
`log-symptom` · `health-report` · `analyze-genome`. Each is a single SKILL.md; `health-report` also
bundles `assets/report-template.html` (the CSS the generated report must use) and
`scripts/html_to_pdf.sh`.

The workspace those skills create and then depend on:

```
.health-tracker          marker file — this is what identifies a workspace
PROFILE.md · known-hazards.md
records/                 SOURCE OF TRUTH, append-only (clinical/<category>/, personal/, genome/)
reports/current/         LIVING documents — maintained in place, never regenerated
reports/genetics/        machine-generated genome reports — regenerable, safe to delete
intake/                  drop-zone for unfiled files
```

### The genome pipeline (`plugins/health-tracker/scripts/`)

**Python standard library only — no pip installs, no network.** That is a hard constraint of running
inside the Cowork sandbox; do not introduce a dependency.

`run_full_analysis.py` is **the only entry point any skill calls.** It loads the genome, matches it
against three sources, and writes four files into the user's `reports/genetics/`:

- `comprehensive_snp_database.py` — curated SNPs across 16 categories (drug metabolism,
  methylation, fitness, …), each with per-genotype descriptions and a `magnitude` 0–4.
- **PharmGKB** — drug-gene interactions, filtered to evidence levels 1A/1B/2A/2B.
- **ClinVar** — matched *by chromosome:position*, not rsid; classified into pathogenic / likely
  pathogenic / risk factor / drug response / protective, then into affected / carrier / unclear by
  zygosity crossed with inheritance mode.

It imports its report-writing functions from `generate_exhaustive_report.py` but inlines its own
ClinVar logic.

### Genome pipeline: correctness invariants (do not regress these)

This is a health tool; a wrong interpretation can steer a real person wrong. These were each a
real bug at some point — keep them fixed:

- **Genome build must match.** ClinVar positions and 23andMe/AncestryDNA v5 exports are both
  **GRCh37**. Position matching is only valid on the same build. A build mismatch produces
  *reproducible garbage* — determinism proves nothing here.
- **Haploid loci.** Consumer arrays report a single-character genotype for all mitochondrial
  variants and for male non-PAR X/Y. A single copy of the alt allele there is homoplasmic/hemizygous
  = **affected**, not "heterozygous." `genotype_call()` handles this; `tests/test_zygosity.py`
  guards it. Don't reintroduce `is_homozygous = gt == alt+alt` as the only affected path.
- **SNP orientation.** A curated entry's genotype keys are in the chip's strand orientation, which is
  often the reverse complement of dbSNP's forward strand. Getting this backwards **flips** the
  interpretation (calls the normal genotype "risk"). **Every new/edited entry must be orientation-
  verified against SNPedia/dbSNP** for which genotype is the risk/effect one. Several entries shipped
  flipped before this was caught.
- **Disclaimers are hard-coded, not model-dependent.** Every generated report embeds a top caveat
  (see `TOP_CAVEAT`) and a full disclaimer including the consumer-genotyping false-positive warning;
  the HTML template carries a fixed disclaimer `<div>`. A user must never receive health-suggestive
  output without the caveat, regardless of what the model does.
- **Recommendations gate on the risk genotype, not gene presence.** Every matched genotype (including
  the *normal* one) becomes a finding, so `if 'GENE' in findings_dict` fires for healthy people. Gate
  on `gene_is_notable()` / an explicit status, or you tell a non-carrier they're a carrier.
- **Never discourage proven folic acid**, especially for anyone who could become pregnant — it is the
  only form proven to prevent neural-tube defects.

**Three scripts are dead code:** `analyze_genome.py`, `full_health_analysis.py`, and
`disease_risk_analyzer.py` are standalone `__main__` scripts that overlap `run_full_analysis.py`,
write *differently-named* outputs (`genetic_report.md`, `COMPLETE_HEALTH_REPORT.md`), and are called
by no skill. Fixing a pipeline bug in one of them fixes nothing the user sees — change
`run_full_analysis.py`.

### Reference data (`plugins/health-tracker/reference/`)

ClinVar + PharmGKB, **gzipped and read gzipped**. Raw ClinVar is 289 MB — over GitHub's 100 MB/file
limit *and* the 200 MB plugin cap — so it ships at ~27 MB and `repo_paths.open_data()` streams it
through `gzip.open()` row by row. There is no unzip step and no temp file; compression is invisible
to callers. **Nothing was filtered out** — the compression is byte-for-byte lossless.

`data_file()` prefers the `.gz` but falls back to a plain `.tsv`, so dropping in a fresh
uncompressed download from ClinVar/PharmGKB just works. To refresh: download the latest TSVs, gzip
them into `reference/`, bump the version.

## Invariants every skill enforces — preserve these when editing

These are not style preferences. They are the reason the product exists, and each one is written
into multiple SKILL.md files on purpose.

1. **`records/` is append-only and sacred.** Never edit, delete, overwrite, or truncate anything
   there — not a duplicate, not a mistake. Corrections are *added alongside*; history is never
   rewritten. Duplicate exports move to `intake/duplicate-exports/` for the **user** to delete.
2. **Quote the person's own words verbatim; never paraphrase a symptom into clinical language.**
   The cautionary pattern, echoed in `log-symptom` and `health-report`: if someone says the floor
   *"tilts like a boat deck"* and a report rewrites it as *"vertigo,"* that names a different
   sensation with different causes — one substituted word can misdirect years of care.
3. **A blank is not a negative.** "Not asked" and "asked, absent" are different facts. Likewise
   "never tested" ≠ "tested negative" — reports must distinguish them so nobody re-orders a test, or
   skips one that was never done.
4. **Living documents (`reports/current/`) are maintained, not regenerated.** Dated reports are
   snapshots; the living docs are the source of truth for the current picture. A skill that files a
   record or logs an episode but doesn't update them has failed — that is exactly how a dropped
   biopsy result disappears for years.
5. **Re-derive from primary sources.** Never restate a prior report's conclusion because a prior
   report said it; prior reports carry errors forward. Cite every claim to its source document.
6. **Not a doctor.** Every genetic output carries a disclaimer. Consumer genotyping produces false
   positives; findings are things to ask a professional about, never diagnoses.

## Writing for this audience

The user is **non-technical and may be frightened** — they are here because something is wrong with
their health. Skill prose (and anything a skill tells Claude to say) avoids file paths, JSON,
terminals, and jargon. Lead with what is time-critical; some post-episode tests lose their value
within hours.

## House Rules

The seven house rules in `house-rules.md` at the root of the shared skill tree
(`~/.claude/skills/../house-rules.md`) are binding defaults here: red-green TDD, fresh-eyes absolute
assessments, never swallow errors, done = verified in the real artifact, whole-branch/whole-codebase
review scope, validate findings + ROI-filter suggestions, and `specs/` as the home for internal
artifacts.

Rule zero deserves restating in this repo specifically, because here it is also the *product's*
core promise: **never destroy the user's data.** When you need a workspace to test against, scaffold
a throwaway one in a temp dir. A real health workspace — someone's records and DNA — is never a test
target.

## Dogfooding

There is **no build step**: the skills are Markdown and the pipeline is stdlib Python. Two loops,
depending on what you changed.

**Changed a script?** Run the pipeline directly from the checkout against a *scratch* workspace —
never a real one:

```bash
WS=$(mktemp -d) && mkdir -p "$WS/records/genome" && touch "$WS/.health-tracker"
cp /path/to/a/genome-export.txt "$WS/records/genome/"
cd "$WS" && python3 /path/to/repo/plugins/health-tracker/scripts/run_full_analysis.py --name "Test"
# then read $WS/reports/genetics/*.md — the reports are the artifact, so actually read them
```

**Changed a skill?** A SKILL.md only takes effect once the plugin is *installed*, so exercise it the
way a user does — install the local checkout as a marketplace and drive the skill in a real session:

```bash
claude plugin marketplace add /path/to/health-tracker-plugin   # local path, not the GitHub repo
claude plugin install health-tracker@health-tracker
```

**Shipping to users:** bump `version` in **both** `version.json` and `.claude-plugin/plugin.json`,
commit, push. Users click **Update** in the marketplace. You never touch their machine — which also
means a bad push reaches real people's health data, so verify before you ship.

## Progress Cadence

During long autonomous work, report at milestones: what's done, what remains, rough % complete, and
any blockers. Never go silent for long stretches — a short update that says "still going, here's
where I am" beats an hour of quiet followed by a surprise.
