# Your private health assistant

This turns Claude into a private assistant for your medical records — one that lives in a folder on
**your own computer**. It helps you keep every record organized, write down symptoms the way a
specialist actually needs them, produce a clean summary for your doctor, and (optionally) make sense
of a 23andMe or AncestryDNA download.

> ⚠️ **This is not a doctor, and it does not give medical advice.** It helps you _organize_ your
> records and have better conversations with real clinicians — it does not replace them, and nothing
> it produces is a diagnosis. The optional DNA analysis reads consumer 23andMe/AncestryDNA data,
> which is **not clinical-grade and can produce false positives** (and can miss things too). Treat
> anything it flags as something to _ask a professional about_, and confirm it with proper clinical
> testing before acting on it. In an emergency, call your local emergency number — not this.

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

_If someone has pasted you this link and asked for help setting up, this section is for you. They
may not be technical. Don't show them file paths, JSON, or terminal commands. Just talk them
through it and do everything you can on their behalf._

**Say this first, in plain words (and again when setup finishes):** this tool helps them organize
their records and prepare for doctor visits — it is **not a doctor, does not give medical advice, and
nothing it produces is a diagnosis**. If they add DNA later, tell them the analysis is not
clinical-grade and can produce false positives, so anything it flags is a question for a professional,
not an answer. Don't skip this because they said they don't want to read — say it to them.

**Step 1 — Have them install the plugin. This is the one thing you cannot do for them.**

Plugin installation is a deliberate security boundary: a plugin can ship executables and hooks, so
**a human has to approve it by hand.** Don't try to work around this. Walk them through it warmly:

> In the sidebar, click **Customize**, then **Plugins**. Click **Add marketplace**, and paste in:
> `csells/health-tracker-plugin`. Then click **Install** on the plugin called **health-tracker**. Tell me
> when it's done.

Wait for them to confirm. If they get stuck, help them find the buttons — don't move on without it,
because none of the skills exist until they do this.

**Step 2 — Have them pick a folder that backs itself up.**

This folder will hold the only copy of their records, so it should live somewhere that syncs to the
cloud automatically. Ask them to make a folder for their health information **inside their Dropbox,
OneDrive, Google Drive, or iCloud Drive folder** (e.g. "My Health"), and connect that in Cowork —
then a lost or broken computer doesn't mean lost records. If they don't use any of those, a plain
Documents folder is fine to start, but tell them plainly it won't be backed up until they move it
somewhere that syncs. It can be empty; you'll fill it.

**Step 3 — Run the setup.**

Once the plugin is installed and the folder is connected, the **setup-health-tracker** skill takes over.
It interviews them and builds everything. Just start it.

---

## What you can do once it's running

Talk in plain language. Claude picks the right tool automatically.

| Say this                        | What happens                                                       |
| ------------------------------- | ------------------------------------------------------------------ |
| _"Set up my health tracker"_    | Asks you some questions and builds your folders and profile        |
| _"File my new records"_         | Sorts and files any documents you dropped in the **intake** folder |
| _"I had an episode last night"_ | Records the symptom properly, and flags anything time-sensitive    |
| _"Make me a health report"_     | Builds a printable summary you can hand a doctor                   |
| _"Analyze my DNA"_              | Runs a genetic health report on your raw 23andMe/AncestryDNA file  |

**The intake folder is your one drop-zone.** Anything new — records or DNA — goes into **intake**,
and you ask me to sort it. You never need to dig into the records folders yourself.

**Adding records:** drop PDFs (labs, visit notes, anything) into the **intake** folder, then say
_"file my new records."_ I'll read each one, file it under the right category, and give it a clear,
dated name.

**Adding your DNA (optional):** download the **raw data** file from 23andMe or AncestryDNA (the
`.txt`, not the PDF ancestry report), drop it in the same **intake** folder, and say _"analyze my
DNA."_ If it came as a `.zip`, unzip it first so the `.txt` is what you drop in.

---

## Doing it by hand instead

If you'd rather not have Claude walk you through it:

1. Install the **Claude** app and sign in. You need the **Pro** plan or higher.
2. Start a **Cowork** session.
3. **Customize → Plugins → Add marketplace** → enter `csells/health-tracker-plugin` → **Install** the
   **health-tracker** plugin.
4. Make a folder for your health information **inside a folder that syncs to the cloud** (Dropbox,
   OneDrive, Google Drive, or iCloud Drive) so it's automatically backed up, and connect it in
   Cowork. (A plain Documents folder works too, but it won't be backed up.)
5. Say: **"Set up my health tracker."**

---

## Things worth knowing

- **Your records stay yours.** Everything lives in the folder on your computer. Your medical
  documents and DNA are never uploaded to this project or to GitHub. Only public medical reference
  data ships with the plugin.
- **Your originals are safe.** The assistant is built to _never_ delete or change an original
  document you add. It only ever adds. Duplicates get set aside for you to delete — it won't delete
  them for you.
- **Turn off training on your chats.** Given what's in here, it's worth going into the Claude app's
  **Privacy** settings and turning off using your conversations to improve their models.
- **Keep the folder somewhere that backs itself up** — inside Dropbox, OneDrive, Google Drive, or
  iCloud Drive, so it's the only copy of your records but never the *last* copy. If you started it in
  a plain local folder, move it into one of those.
- **This is not a doctor.** Everything it produces is meant to make conversations with your real
  doctors better, not to replace them. The DNA analysis reads consumer genotyping data, which can
  produce false positives; treat anything it finds as something to _ask a professional about_, not
  as a diagnosis.

---

---

# Maintainer notes

_Nothing below here matters if you're just using this. Stop reading — you're done._

**Layout.** `.claude-plugin/marketplace.json` (marketplace manifest) → `plugins/health-tracker/`
holding `.claude-plugin/plugin.json`, `version.json`, `skills/` (setup-health-tracker, file-records,
log-symptom, health-report, analyze-genome), `scripts/` (the genetic pipeline, Python stdlib only),
and `reference/` (public ClinVar + PharmGKB, gzipped).

**Shipping an update.** Edit → bump `version` in `version.json` and `plugin.json` → commit → push.
The user clicks **Update** on the marketplace and gets it. You never touch their machine.

**The reference data.** ClinVar (341,375 variants) + PharmGKB. Raw ClinVar is 289 MB — over GitHub's
100 MB/file limit _and_ the 200 MB plugin cap — so it ships gzipped (~27 MB), read directly via
Python's `gzip` module, streaming row by row.

**Nothing was filtered out of it.** The compression is byte-for-byte lossless: every row and column
is recoverable (verified by SHA-256), and the pipeline's findings are identical to the uncompressed
original (verified by a seed-pinned diff of every output file). To refresh, download the latest
ClinVar/PharmGKB TSVs, gzip them into `reference/`, and bump the version.

**Privacy.** Public repo is correct: the plugin holds only generic skills and public reference data —
no PHI — and public repos clone anonymously, so the user hits no auth friction. Their records and
genome never leave their own folder.
