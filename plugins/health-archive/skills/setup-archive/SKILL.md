---
name: setup-archive
description: Set up a new personal health archive — the folder structure, the patient profile, and the living documents — by interviewing the person about themselves. Use when someone is starting out with the health archive, says "set up my health archive", "get me started", "I just installed this", "help me begin", "create my health folder", or when any other health-archive skill runs and finds no archive (no records/ folder, no PROFILE.md) in the current folder. This is the first thing a new user does; it replaces having a technical person configure everything by hand.
---

# Set Up a Health Archive

Your job here is to stand in for the friend who would otherwise have set this up by hand.
The person you're talking to is **not technical**. Do not mention git, terminals, JSON, or file
paths unless they ask. Talk like a helpful medical assistant, not a computer program.

By the end, the folder they connected will contain their profile, an empty-but-organized place
for every record, and the living documents that make this archive worth more than a pile of PDFs.

## Before you start

Confirm you're in the right place. You should be working inside the folder the person connected
(in Cowork, the folder they picked; the current working directory). If there's already a
`records/` folder and a `PROFILE.md` here, an archive exists — **stop and don't overwrite it.**
Ask whether they want to review or update it instead, and hand off to the relevant skill.

## 1. Interview them — warmly, a few questions at a time

Don't fire all of this at once. Ask in small, friendly batches. If they don't know an answer or
would rather skip it, that's fine — write "not provided" and move on. Nothing here is required to
get started; they can always add more later.

**Who they are**
- Name they want on reports
- Date of birth
- Anything they want a new doctor to know in the first thirty seconds

**Their main health picture**
- What's the main thing going on health-wise? The reason they wanted this.
- Any diagnoses they already carry?
- Any recurring episodes or symptoms they're tracking? (If yes, note it — the **log-symptom**
  skill is built for exactly this.)

**Safety essentials** (these go in medications-and-cautions and matter most)
- Medications they take now
- Drug allergies or bad reactions
- Anything a doctor should never prescribe them, and why

**Chart errors — explain this one, it's important**
Ask, in plain words: *"Is there anything in your medical records that is just wrong — a
diagnosis you don't actually have, an event a doctor wrote down incorrectly, or something
important that's missing?"* Explain why you're asking: records get copied forward for decades,
and a single wrong word can misdirect care for years. Whatever they say goes into
`known-hazards.md` so every future report guards against it. If they can't think of anything,
that's fine — the file starts empty and grows as they discover things.

**Their DNA data (optional)**
- Do they have a raw DNA download from 23andMe or AncestryDNA? If so, they can drop the `.txt`
  file into `records/genome/` and you can run a genetic analysis later (the **analyze-genome**
  skill). If not, skip it entirely — everything else works without it.

## 2. Build the folder structure

Create this layout in the current folder. Create every directory even if it's empty — the empty
folders tell the person (and you, later) where things go.

```
.health-archive          ← marker file (see below); this is what identifies the archive
PROFILE.md               ← who they are, from the interview
known-hazards.md         ← known errors in their chart; may start empty
records/                 ← SOURCE OF TRUTH. Append-only. Never edit or delete anything here.
  clinical/              ← anything from a provider or lab
    blood-work/
    cardiac/
    brain-and-neuro/
    gi-health/
    thyroid/
    womens-health/
    visits/              ← ER visits, admissions, visit notes
    insurance/
  personal/              ← things THEY wrote: symptom diaries, questions, concerns
  genome/                ← raw DNA export (.txt), if they have one
reports/                 ← what we generate, for humans
  current/               ← LIVING documents — maintained over time, not regenerated
intake/                  ← drop-zone for new files waiting to be filed
```

Write a short `.health-archive` marker file containing a single line like
`health-archive workspace — created <the date the person tells you, or leave undated>`.
Do not invent a date; if you don't know today's date, ask or leave it out.

## 3. Write PROFILE.md

Fill in what you learned. Keep it to what a doctor would want up front. Example shape:

```markdown
# Health Profile — <Name>

**DOB:** <date>  ·  **Created:** <date>

## In one paragraph
<The thirty-second version a new doctor should hear first.>

## Current diagnoses
- ...

## Current medications
- ...

## Allergies & prescribing cautions
- ...

## What I'm tracking
<Main recurring concern, if any.>
```

## 4. Seed the living documents

These are the heart of the archive. Create each one in `reports/current/`, pre-filled with
whatever the interview gave you and clearly marked where more will accrue:

- **`medical-journey.md`** — the ongoing narrative. Start it with their one-paragraph summary and
  a dated "Archive started" note. This is the document they hand a new doctor. It is *maintained*,
  never replaced with a new dated file.
- **`open-loops.md`** — outstanding tests, referrals, results not yet back. Start empty with a
  short header explaining what belongs here.
- **`medications-and-cautions.md`** — their meds, allergies, and prescribing cautions from the
  interview.
- **`lab-timeline.csv`** — header row only: `Date,Test,Value,Units,Reference Range,Flag,Source File`.
  It fills in as records get filed.
- **`for-next-appointment.md`** — the handoff packet for their next visit. Start with a short
  header.

## 5. Write known-hazards.md

If they named any chart errors, record each one the way this archive records everything:
what the chart says, what's actually true, and the evidence. If they named none, write a short
file explaining what it's for so it's ready when they find something:

```markdown
# Known Hazards in My Record

Errors in my medical chart that must not be repeated in any report. Records get copied forward
for years; a wrong word here can misdirect care. When you find one, add it as:

- **What the chart says:** ...
- **What's actually true:** ...
- **Evidence:** ...

(none recorded yet)
```

## 6. Tell them what just happened, and what they can do next

In plain language, no jargon. Something like:

> Your health archive is set up. Here's what you can do now:
> - **"I have new records to file"** — drop PDFs into the `intake` folder and I'll sort and file them.
> - **"Log a symptom"** — tell me about an episode and I'll record it properly.
> - **"Make me a health report"** — I'll build a printable summary for a doctor.
> - **"Analyze my DNA"** — if you added a DNA file, I'll run a genetic health report.
>
> The one folder that matters most is **records** — it's the original copy of everything, and I
> will never change or delete anything in it.

## The rules that protect them (apply these in every session, forever)

- **`records/` is sacred: append-only.** Never edit, never delete, never overwrite anything a
  person or a provider put there. If something was recorded wrong, add a correction alongside it —
  never rewrite history.
- **Quote their words verbatim.** Never paraphrase a symptom into clinical language.
- **The living documents in `reports/current/` are maintained, not regenerated.**
- **Duplicates are preserved, never deleted** — move extras to `intake/duplicate-exports/` and let
  the person delete them.
