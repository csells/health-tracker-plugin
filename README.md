# Your private health assistant

This turns Claude into a private assistant for your medical records — one that lives in a folder on
**your own computer**. It helps you keep every record organized, write down symptoms the way a
specialist actually needs them, produce a clean summary for your doctor, and (optionally) make sense
of a 23andMe or AncestryDNA download.

**You don't need to be technical. You don't need to read this whole page.**

---

## 👉 The easy way: let Claude set it up for you

1. Open the **Claude** app on your computer (get it at [claude.ai/download](https://claude.ai/download);
   you'll need the **Pro** plan, which includes the feature we use, called **Cowork**).
2. Start a **Cowork** session.
3. Paste this into the chat:

   > **Set me up with this health assistant: https://github.com/csells/health-tracker-plugin — read the
   > page and walk me through it.**

Claude will read this page and take it from there — it'll tell you exactly what to click, ask you
the questions it needs, and build your health folder for you. **You can just talk to it.**

If you'd rather do it by hand, the steps are spelled out further down.

---

## 🤖 For Claude: how to onboard this person

*If someone has pasted you this link and asked for help setting up, this section is for you. They
are **not technical**. Don't show them file paths, JSON, or terminal commands. Just talk them
through it and do everything you can on their behalf.*

**Step 1 — Have them install the plugin. This is the one thing you cannot do for them.**

Plugin installation is a deliberate security boundary: a plugin can ship executables and hooks, so
**a human has to approve it by hand.** Don't try to work around this. Walk them through it warmly:

> In the sidebar, click **Customize**, then **Plugins**. Click **Add marketplace**, and paste in:
> `csells/health-tracker-plugin`. Then click **Install** on the plugin called **health-tracker**. Tell me
> when it's done.

Wait for them to confirm. If they get stuck, help them find the buttons — don't move on without it,
because none of the skills exist until they do this.

**Step 2 — Have them pick a folder.**

Ask them to make a folder for their health information (Documents → "My Health" is a fine default),
and connect it in Cowork. It can be empty; you'll fill it.

**Step 3 — Run the setup.**

Once the plugin is installed and the folder is connected, the **setup-health-tracker** skill takes over.
It interviews them and builds everything. Just start it.

---

## What you can do once it's running

Talk in plain language. Claude picks the right tool automatically.

| Say this | What happens |
|---|---|
| *"Set up my health tracker"* | Asks you some questions and builds your folders and profile |
| *"File my new records"* | Sorts and files any documents you dropped in the **intake** folder |
| *"I had an episode last night"* | Records the symptom properly, and flags anything time-sensitive |
| *"Make me a health report"* | Builds a printable summary you can hand a doctor |
| *"Analyze my DNA"* | Runs a genetic health report on your raw 23andMe/AncestryDNA file |

**Adding records:** drop PDFs (labs, visit notes, anything) into the **intake** folder, then say
*"file my new records."*

**Adding your DNA (optional):** download the **raw data** file from 23andMe or AncestryDNA, put it
in **records → genome**, and say *"analyze my DNA."* If it came as a `.zip`, unzip it first.

---

## Doing it by hand instead

If you'd rather not have Claude walk you through it:

1. Install the **Claude** app and sign in. You need the **Pro** plan or higher.
2. Start a **Cowork** session.
3. **Customize → Plugins → Add marketplace** → enter `csells/health-tracker-plugin` → **Install** the
   **health-tracker** plugin.
4. Make a folder for your health information and connect it in Cowork.
5. Say: **"Set up my health tracker."**

---

## Things worth knowing

- **Your records stay yours.** Everything lives in the folder on your computer. Your medical
  documents and DNA are never uploaded to this project or to GitHub. Only public medical reference
  data ships with the plugin.
- **Your originals are safe.** The assistant is built to *never* delete or change an original
  document you add. It only ever adds. Duplicates get set aside for you to delete — it won't delete
  them for you.
- **Turn off training on your chats.** Given what's in here, it's worth going into the Claude app's
  **Privacy** settings and turning off using your conversations to improve their models.
- **Put the folder somewhere backed up** — the same place your other important documents live.
- **This is not a doctor.** Everything it produces is meant to make conversations with your real
  doctors better, not to replace them. The DNA analysis reads consumer genotyping data, which can
  produce false positives; treat anything it finds as something to *ask a professional about*, not
  as a diagnosis.

---
---

# Maintainer notes

*Nothing below here matters if you're just using this. Stop reading — you're done.*

**Layout.** `.claude-plugin/marketplace.json` (marketplace manifest) → `plugins/health-tracker/`
holding `.claude-plugin/plugin.json`, `version.json`, `skills/` (setup-health-tracker, file-records,
log-symptom, health-report, analyze-genome), `scripts/` (the genetic pipeline, Python stdlib only),
and `reference/` (public ClinVar + PharmGKB, gzipped).

**Shipping an update.** Edit → bump `version` in `version.json` and `plugin.json` → commit → push.
The user clicks **Update** on the marketplace and gets it. You never touch their machine.

**The reference data.** ClinVar (341,375 variants) + PharmGKB. Raw ClinVar is 289 MB — over GitHub's
100 MB/file limit *and* the 200 MB plugin cap — so it ships gzipped (~27 MB), read directly via
Python's `gzip` module, streaming row by row.

**Nothing was filtered out of it.** The compression is byte-for-byte lossless: every row and column
is recoverable (verified by SHA-256), and the pipeline's findings are identical to the uncompressed
original (verified by a seed-pinned diff of every output file). To refresh, download the latest
ClinVar/PharmGKB TSVs, gzip them into `reference/`, and bump the version.

**Privacy.** Public repo is correct: the plugin holds only generic skills and public reference data —
no PHI — and public repos clone anonymously, so the user hits no auth friction. Their records and
genome never leave their own folder.
