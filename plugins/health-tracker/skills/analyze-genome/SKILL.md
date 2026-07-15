---
name: analyze-genome
description: Run a genetic health analysis on the person's raw DNA export and produce plain-language reports on drug-gene interactions, disease-risk variants, carrier status, and lifestyle genetics. Use when someone asks to "analyze my DNA", "run my genome", "what does my 23andMe say", "genetic health report", "check my DNA for health risks", "pharmacogenomics", or "which medications affect me genetically", and a raw DNA export exists (or can be added) in records/genome/.
---

# Analyze Genome

Run the bundled genetic analysis pipeline over the person's raw DNA export and turn the output into
something they can actually understand and use.

## What this needs

- A raw DNA export in **`records/genome/`** — the `.txt` file from **23andMe** or **AncestryDNA**
  (the "raw data" download, not the PDF ancestry report). If they downloaded a `.zip`, unzip it
  first so the `.txt` is in the folder. If there's no export there yet, tell them how to get one
  and stop — this skill can't run without it.

## What ships with the plugin

The reference datasets (ClinVar, PharmGKB) and the analysis scripts are bundled inside this
plugin, under its `reference/` and `scripts/` folders. The reference data is stored gzipped to fit
hosting limits, but **nothing was trimmed** — every ClinVar variant and every PharmGKB annotation
is present, and the pipeline reads the compressed files directly. The datasets are public
third-party reference data, identical for everyone; only the DNA export is personal.

## How to run it

The pipeline is a self-contained Python program that uses only the Python standard library (needs
**Python 3.9+**) — no package installation, no internet. Run it from the person's archive folder
(the current working directory), pointing at the plugin's script:

```bash
# macOS / Linux (CLAUDE_PLUGIN_ROOT points at this plugin's root inside Cowork/Claude Code):
python3 "$CLAUDE_PLUGIN_ROOT/scripts/run_full_analysis.py" --name "<their name>"
```

**On Windows**, `python3` often isn't on the PATH and the shell expands variables differently — use
`python` or `py -3`, and the env var as `%CLAUDE_PLUGIN_ROOT%` (cmd) or `$env:CLAUDE_PLUGIN_ROOT`
(PowerShell). For example, in PowerShell:

```powershell
python "$env:CLAUDE_PLUGIN_ROOT\scripts\run_full_analysis.py" --name "<their name>"
```

If `CLAUDE_PLUGIN_ROOT` isn't set, find `run_full_analysis.py` inside this plugin's `scripts/`
folder and run it with whichever Python launcher works (`python3`, `python`, or `py -3`). It
automatically:
- finds the single DNA export in `records/genome/`,
- writes its reports into **`reports/genetics/`** in the person's archive (regenerable — safe to
  delete and re-run),
- leaves `records/` and the plugin untouched.

It produces:
- `EXHAUSTIVE_GENETIC_REPORT.md` — lifestyle/health findings + drug-gene interactions
- `EXHAUSTIVE_DISEASE_RISK_REPORT.md` — pathogenic / likely-pathogenic / risk-factor variants
- `ACTIONABLE_HEALTH_PROTOCOL_V3.md` — the findings synthesized into concrete recommendations
- `comprehensive_results.json` — the structured data behind the reports

## After it runs — translate, don't just hand over

The raw reports are dense and use magnitudes, genotypes, and gene symbols. Your job is to make them
usable:

1. **Lead with what's actionable and high-confidence** — especially drug-gene interactions, which
   are the most clinically useful part. If a variant affects how they metabolize a common
   medication, say so in plain terms and point them to discuss it with their prescriber.
2. **Be honest about uncertainty.** Consumer genotyping has false positives; a single variant is a
   flag to discuss, not a diagnosis. Say that clearly.
3. **Distinguish carrier status from personal risk.** Being a carrier for a recessive condition
   usually doesn't affect the person's own health — it matters for family planning. Don't alarm.
4. **Feed the important findings into the living documents.** If the analysis surfaces a
   prescribing caution (e.g. a metabolizer status that changes drug dosing), add it to
   `reports/current/medications-and-cautions.md`. If it reveals something that belongs in the
   ongoing picture, note it in `reports/current/medical-journey.md`.

## Boundaries — say these plainly

This is **not** a clinical-grade genetic test and **not** medical advice. It reads consumer
genotyping data against public research databases to surface things worth discussing with a
doctor or a genetic counselor. Anything that looks serious should be confirmed with proper
clinical testing before anyone acts on it. Make sure the person understands this before they read
the reports, not after.
