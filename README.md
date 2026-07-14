# Health Tracker — a personal health archive plugin for Claude Cowork

This repository is a **Claude plugin marketplace**. It packages a private, agent-driven personal
health archive so a **non-technical person** can run it themselves in **Claude Cowork** — no git,
no terminal, no Python, and no medical data in the cloud.

It's a de-personalized, portable version of a working medical-records archive: same folder
discipline, same skills, same genetic-analysis pipeline — with all patient-specific identity and
data stripped out and replaced by an interview-driven setup.

## What the user gets

Once installed, they talk to Claude in plain language:

| They say… | The skill that runs | What happens |
|---|---|---|
| "Set up my health archive" | `setup-archive` | Interviews them, builds the folder structure, profile, and living documents |
| "File these records" / drops files in `intake/` | `file-records` | Sorts and files records, updates the lab timeline and living summary |
| "Log a symptom" / "I had another episode" | `log-symptom` | Records an episode in specialist-ready detail, flags time-critical follow-ups |
| "Make me a health report" | `health-report` | Generates a printable, doctor-ready health assessment |
| "Analyze my DNA" | `analyze-genome` | Runs the genetic pipeline on their raw 23andMe/AncestryDNA export |

Their records and DNA live in a **folder on their own computer** that they connect to Cowork.
Only public reference data (ClinVar, PharmGKB) ships in the plugin.

## How they install it

See **[SETUP.md](SETUP.md)** — a plain-English guide written for the non-technical user. The short
version:

1. Install the Claude desktop app and sign in (Pro plan or higher — Cowork is included).
2. In Cowork: **Customize → Plugins → Add marketplace**, enter this repo (`owner/health-tracker`).
3. Install the **health-archive** plugin.
4. Make a folder for their health data, connect it in Cowork, and say "set up my health archive."

## Repository layout

```
.claude-plugin/marketplace.json     ← marketplace manifest (lists the plugin)
plugins/health-archive/
  .claude-plugin/plugin.json         ← plugin manifest
  version.json                       ← bump to push an update to installed users
  skills/                            ← the five skills (setup, file, log, report, genome)
  scripts/                           ← the genetic-analysis pipeline (Python stdlib only)
  reference/                         ← public ClinVar + PharmGKB data, gzipped (lossless)
SETUP.md                            ← non-technical setup guide for the end user
```

## About the reference data (why it's gzipped)

The genetic pipeline reads two public datasets: **ClinVar** (341,375 variants) and **PharmGKB**.
The raw ClinVar file is 289 MB — too large to host on GitHub (100 MB/file limit) and over the
plugin size cap. It's stored gzipped (~27 MB total) and read directly by the pipeline via Python's
`gzip` module.

**Nothing was filtered out.** The compression is byte-for-byte lossless: every row, every column of
the original is recoverable (verified by SHA-256), and the pipeline produces identical findings to
the uncompressed original (verified by a seed-pinned output diff). To refresh the data later,
download the latest ClinVar/PharmGKB TSVs, gzip them into `reference/`, and bump `version.json`.

## Pushing updates to users

Because this is a git-backed marketplace, you stay able to fix things without touching the user's
machine:

1. Edit a skill or the pipeline here.
2. Bump `version` in `plugins/health-archive/version.json` (and `plugin.json`).
3. Commit and push.
4. The user clicks **Update** on the marketplace in Cowork and gets the change.

## Privacy model

- **Public repo is fine.** The plugin contains only generic skills and public reference data — no
  PHI. Public repos clone anonymously, so there's no auth friction for the user.
- **The user's data never comes here.** Records, genome, and reports live only in the local folder
  they connect to Cowork. Nothing in this repo, and nothing pushed to GitHub, is theirs.

## Not medical advice

Everything generated is AI-assisted synthesis of the user's own documents and public research data.
It exists to make conversations with real clinicians more productive — not to replace them. The
genetic analysis reads consumer genotyping data, which has false positives; findings are prompts to
discuss with a doctor or genetic counselor, not diagnoses.
