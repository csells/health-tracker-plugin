---
name: file-records
description: File new medical records into the health tracker and keep the living documents current. Use when someone mentions new health documents, lab results, ER paperwork, visit notes, or imaging to sort; says "I have new records", "file these", "sort out my intake folder", "I downloaded my labs", "add this to my archive", "update my lab results"; or drops files into the intake/ folder. Also handles updating the lab timeline and the living summary after new records arrive.
---

# File Medical Records

File medical documents into the organized archive and — the part that's easy to skip and matters
most — update the living documents so nothing gets lost.

## 🔴 Rule zero: never destroy anything

**Records are the only irreplaceable thing here.** Everything else can be rebuilt from them.

- **Never delete, overwrite, or truncate a file in `records/`.** It is append-only.
- **Duplicates are common** — the same result is often exported several times from a patient
  portal. **Do not delete them.** File one clean copy, move the rest to `intake/duplicate-exports/`,
  and tell the person they're safe to remove. Let *them* delete.
- Before finishing, verify nothing was lost — compare a file count before and after.

## Where records come from

- **`intake/`** — the default drop-zone. Files land here, get filed, and the folder ends up empty.
- **A folder the person points you at** (e.g. their Downloads). **Copy, don't move** — it isn't
  ours to empty.

## Where records go

- Documents from **providers or labs** → `records/clinical/<category>/`
- Documents the **person wrote themselves** → `records/personal/`
- **Raw DNA exports** (`.txt`/`.tsv` from 23andMe/AncestryDNA) → `records/genome/`, **kept under
  their original name and extension** (see the genome exception below)
- Lab values → appended to `reports/current/lab-timeline.csv`

## Workflow

### 1. See what's new

List the source and the archive's `records/` tree. Match new files to existing ones by:
- **Date in the filename** (formats vary: `YYYY-MM-DD`, `YYYY-M-D`, `YYYY_MM_DD`)
- **Content type** ("CBC", "TSH", "metabolic panel")
- **File size / content** (identical content = already filed, even if the names differ)

Classify each as **already filed** / **new** / **unclear** (flag unclear ones for the person).

⚠️ **Portal exports are frequently duplicated** — the same lab may arrive under two different
names. **Read each file to see what it actually contains** — the filenames are unreliable.
Non-PDF files (`.docx`, `.xlsx`) may already exist as converted PDFs; read and compare.

### 2. Show your plan, then wait

Present a short table: new files with the name + destination you propose; already-filed files;
unclear matches. **Wait for the person to confirm before filing anything.**

### 3. File each new document

1. **Read it** to find the **actual service/test date** from the document content — *not* the
   filename date, which is often the download date and often wrong.
2. Pick the destination:

   | Content | Destination |
   |---|---|
   | Blood work, metabolic panels, CBC, nutrition panels | `records/clinical/blood-work/` |
   | TSH, T4, T3, thyroid | `records/clinical/thyroid/` |
   | ECG, troponin, echocardiogram | `records/clinical/cardiac/` |
   | Colonoscopy, CT abdomen, fecal, endoscopy | `records/clinical/gi-health/` |
   | HPV, Pap, STI, gynecological | `records/clinical/womens-health/` |
   | Brain, neuro, audiology, vestibular, cognitive testing | `records/clinical/brain-and-neuro/` |
   | ER visits, admissions, after-visit summaries, visit notes, historical records | `records/clinical/visits/` |
   | Insurance cards | `records/clinical/insurance/` |
   | **Anything the person wrote themselves** (diaries, concerns, questions) | **`records/personal/`** |
   | **Raw DNA export** (a large `.txt`/`.tsv` whose first lines are `#` comment headers followed by rows like `rsid  chromosome  position  genotype`; from 23andMe/AncestryDNA) | **`records/genome/`** |

   If a document doesn't fit these, ask rather than guessing.

3. Name it `YYYY-MM-DD Description.pdf` using the actual service date. **Exception — a raw DNA
   export:** move it into `records/genome/` **unchanged**, keeping its original filename and
   `.txt`/`.tsv` extension. Do **not** date-rename it and do **not** convert it to PDF — the
   `analyze-genome` skill only finds `.txt`/`.tsv` files, so renaming or converting hides it.
4. Move (from `intake/`) or copy (from an external folder) into place.

### 4. Update the lab timeline

If any new file contains lab results:

1. Open `reports/current/lab-timeline.csv` (columns: `Date,Test,Value,Units,Reference Range,Flag,Source File`).
2. Extract **every** result from the new documents into matching rows.
3. **Append in chronological order. Do not create a new CSV** — this file is living and maintained
   in place.
4. Use test names consistent with existing rows; flag `H`/`L` from the reference range **shown in
   that document**; preserve the range exactly as printed; skip non-quantitative results.

### 5. ⚠️ Update the living documents — do not skip this

**This is the step that keeps the archive from rotting.** A filed document nobody reads again is
how a dropped test order or a missing biopsy result disappears for years.

- **`reports/current/medical-journey.md`** — if the new records change the picture (a new event, a
  new diagnosis, a new result), update the narrative.
- **`reports/current/open-loops.md`** — did a document order a test, recommend a referral, or take
  a biopsy? Add it. Did a pending result finally come back? Close it out.
- **`reports/current/medications-and-cautions.md`** — if the medication list changed.
- **`known-hazards.md`** — if a record reveals that something in the chart is wrong.

⚠️ **When a record quotes the person's own description of a symptom, keep their exact words.** Do
not "clean it up" into clinical language — see the caution in the **log-symptom** skill for why a
single paraphrased word can misdirect care for years.

### 6. Summary

Report: how many files were filed and where; how many lab rows were added; **what changed in the
living documents**; any duplicates preserved in `intake/duplicate-exports/` (and that they're safe
to delete); anything skipped and why; and **confirmation that no data was lost** (counts before
and after).

If one of the filed items was a raw DNA export, let them know it's now in `records/genome/` and they
can say **"analyze my DNA"** whenever they want the genetic report.
