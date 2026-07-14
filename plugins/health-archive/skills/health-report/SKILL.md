---
name: health-report
description: Generate a comprehensive, printable health assessment from the medical records in the archive. Use when someone asks to create a health report, generate a medical summary, produce a health assessment, make a PDF for a doctor, or wants a printable overview of their records. Triggers on "generate a report", "create a health report", "make a PDF report", "health assessment", "summary for my doctor".
---

# Health Report Generator

Generate a formatted, printable health assessment from the medical records in this archive.

## ⚠️ Read this before anything else

**The failure mode of this skill is paraphrasing a primary source into something that sounds more
clinical and means something different.** This is not hypothetical: in one real archive, a
patient's own words — *"a snow globe being shaken"* — were rewritten in a report as *"rotational
vertigo,"* nearly the opposite sensation. That single paraphrase propagated into every downstream
document and misdirected the patient's care for two decades. Guard against it explicitly:

1. **Never paraphrase a patient-reported symptom. Quote it verbatim** from `records/personal/`, in
   quotation marks, and cite the file.
2. **Cite every factual claim** to the source document it came from. If you cannot cite it, do not
   assert it.
3. **Re-derive from primary sources.** Do NOT restate a prior report's conclusion just because a
   prior report said it — prior reports can carry forward errors.
4. **Distinguish "not found" from "not looked for."** A test never performed is not a negative
   result. Say which it is.

## Process

### 1. Orient — read these FIRST, in this order

| Read | Why |
|---|---|
| **`reports/current/medical-journey.md`** | The corrected, current clinical picture. **Start here.** |
| **`reports/current/open-loops.md`** | What has never been done or never came back |
| **`reports/current/medications-and-cautions.md`** | Allergies, cautions, prescribing hazards |
| **`known-hazards.md`** | Known errors in this person's chart that must not be repeated |
| **`PROFILE.md`** | Who they are, in brief |
| **`records/personal/`** | **The person's own words.** These outrank every clinician's paraphrase. |

### 2. Read the source records

Read the documents across the category folders under `records/clinical/` (`blood-work/`,
`thyroid/`, `cardiac/`, `gi-health/`, `womens-health/`, `brain-and-neuro/`, `visits/`). Also read
`reports/current/lab-timeline.csv` for lab trends at a glance.

For large PDFs (>10 pages), read in batches using the `pages` parameter. **Do not skip long
historical records** — a critical admission buried at the end of a long scanned document is often
the most important thing in the archive.

### 3. Synthesize findings

Organize into:
- **Patient Summary** — demographics, allergies, current medications, family history
- **Active Diagnoses** — each with supporting lab values, trends over time, and clinical
  significance. Use tables for trending data. **Cite the source document for each.**
- **What has been excluded** — tests that came back negative, so nobody re-orders them
- **What has never been done** — from `open-loops.md`. Distinguish clearly from the above.
- **Prognosis** — honest, split into "good news" and "concerns"
- **Recommended Plan** — by urgency: Urgent (2–4 weeks) / Short-term (1–3 months) / Ongoing

### 4. Generate the HTML report

Read the template at `assets/report-template.html` (in this skill's folder) for the CSS. Create a
complete HTML file at `reports/YYYY-MM-DD Health Assessment.html` using the template's `<style>`
block and your synthesized content as the `<body>`.

CSS classes available: `highlight` (abnormal/HIGH, red), `good` (normal, green), `disclaimer`
(the AI-generated notice), `summary-box` (patient summary), `section-urgent` / `section-short` /
`section-ongoing` (recommendations by urgency), `bottom-line` (concluding synthesis),
`page-break`, `footer`.

Include the AI-generated disclaimer at the top and a footer with the report date.

### 5. Convert to PDF

Run the bundled converter (it tries whatever PDF engine is available and tells you which it used):

```bash
bash scripts/html_to_pdf.sh "reports/YYYY-MM-DD Health Assessment.html" "reports/YYYY-MM-DD Health Assessment.pdf"
```

If no PDF engine is available in the environment, the script says so and **leaves the HTML file in
place** — it opens in any browser and prints to PDF from there. Do not treat a missing PDF engine
as a failure of the report; the HTML *is* the report.

### 6. Verify and update the living documents

- If a PDF was produced, read it back to confirm it rendered, then remove the intermediate HTML.
  If only HTML was produced, keep it and tell the person how to print it.
- **If the report surfaced anything new, update `reports/current/medical-journey.md` and
  `reports/current/open-loops.md`.** A dated report not reflected in the living documents will be
  lost.
- Report the file path.

## Output

Final file: `reports/YYYY-MM-DD Health Assessment.pdf` (or `.html` if no PDF engine is present).

**A dated assessment is a snapshot, not the source of truth.** The living documents in
`reports/current/` are.
