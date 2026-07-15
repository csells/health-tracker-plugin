---
name: log-symptom
description: Record a symptom episode — an attack, a flare, a bad spell, an ER trip — into the health tracker in the detail a specialist actually needs, and flag any time-critical follow-up. Use whenever someone describes an episode in any form: "I had an attack", "another flare last night", "she had another episode", "log this", "I'm recovering from one", "went to the ER again", or any description of a recurring symptom. Offer to log it even when they're just mentioning it in passing. For someone with a recurring undiagnosed problem, this diary is often the single most valuable diagnostic instrument they have.
---

# Log a Symptom Episode

Capture an episode in a form a specialist can actually use.

## Why this matters more than it looks

Clinicians almost never get to see a patient mid-episode. So **what gets written down in the hours
afterward is, in practice, the entire evidence base.** For a recurring, undiagnosed problem, a
well-captured episode log is often worth more than another ER visit — and a diary that shows the
*pattern* across many episodes can reveal what any single visit cannot.

Two failure modes have wrecked real patients' care. This skill exists to prevent both:

1. **Paraphrasing the patient's words into clinical language that means something different.**
   For example, if someone says the floor *"tilts like a boat deck,"* do not rewrite that as
   *"vertigo"* — a sense of tilting and a false sense of spinning point to different causes, and one
   substituted word can steer years of diagnosis toward the wrong conditions. **Quote the person's
   exact words. Do not translate them into medical terms.**
2. **Treating a blank as a negative.** "No headache noted" is not the same as "asked about
   headache — there wasn't one." A symptom's *absence* is only evidence if someone actually asked.
   **Ask about each symptom below and record "asked — absent" rather than leaving it blank.**

## First: check for anything time-critical

Some episodes have a follow-up whose value **decays within hours or days** — a test that only
means something if done right after the episode, while a transient sign is still measurable.
Before anything else, check the person's `PROFILE.md` and `known-hazards.md` for any noted
time-critical follow-up tied to their condition, and if one applies, **surface it at the very top
of your response, not buried at the end.** If nothing specific is recorded, still consider whether
a same-day or next-day test would capture something that will otherwise disappear, and say so.

## What to capture

Work through these with the person. If they don't know, write **"not known"** — don't guess, don't
silently omit.

### The episode itself
- **Date and time it started**, and **what they were doing** at that moment (position and activity
  can matter enormously — lying down, standing, asleep, exerting?)
- **The worst phase** — how long it lasted, and **their exact words** for what it felt like. If it
  was different from their usual pattern, that difference is important; record it.
- **The aftermath** — how long, and which symptoms (nausea/vomiting, sweating, diarrhea, shaking,
  hot vs. cold, weakness, confusion, whatever applies)
- **Time to full recovery**

### Associated symptoms — ask about each, one side/area at a time where relevant
The point is to catch a *one-sided* or *localized* change, which is often the strongest clue to
what's happening. Tailor the list to their condition, but by default ask about:
- Pain — where, how bad, radiating?
- Anything one-sided (hearing, vision, weakness, numbness, ringing, fullness/pressure) — **which
  side?**
- Visual changes, aura, spots, shimmering
- Light or sound sensitivity

### What was observed
- Did anyone else witness it? What did they see?
- **Was anything filmed?** Even ten seconds on a phone can be worth more than any description. If
  it happens again, encourage filming.

### The preceding 24 hours
Sleep · food and drink · alcohol · stress · travel/altitude/flying · missed or changed
medications · menstrual/hormone cycle · weather or barometric change · anything unusual.

### Treatment
What they took, **how much it helped, and how fast.** This is genuinely diagnostic. If their
`known-hazards.md` or `medications-and-cautions.md` notes a metabolizer or dosing issue, factor it
in (e.g. a medication that may be under-performing at standard doses).

### Anything different from their usual episode
New symptoms, longer or shorter phases, a new possible trigger. Deviations from the pattern are
often the most informative thing in the whole entry.

## Where it goes

**Append** a new entry to **`records/personal/symptom-log.md`** — newest entry at the top, directly
under the header. Create the file if it doesn't exist.

`records/` is **source of truth and append-only.** Add the new entry; **never edit or delete a
previous one**, even to fix it. If something was recorded wrong, add a correction note to the new
entry rather than rewriting history — that discipline is exactly what a contradictory medical chart
fails at.

## Then — the part that's easy to skip

1. **Update `reports/current/medical-journey.md`** — add the episode to the timeline, and revise
   the pattern description if this one revealed something new. *A log entry nobody reads again is
   how a follow-up gets lost.*
2. **Update `reports/current/open-loops.md`** if it created a new follow-up.
3. **If they went to the ER**, the paperwork will arrive later — remind them, and use the
   **file-records** skill to file it when it does.

## Close by surfacing the time-critical actions

End your response with the concrete, time-sensitive next steps first — any decaying-window test,
any "film it next time," any new open loop — in that order, not buried under a long summary.

## Entry template

```markdown
## YYYY-MM-DD — Episode

**Onset:** [time] · **Doing what:** [activity/position at onset]

**Worst phase:** [duration] — "[their exact words]"
**Aftermath:** [duration] — [symptoms]
**Recovery to baseline:** [duration]

**Associated symptoms:** [one-sided changes? which side? pain? visual? light/sound?]

**Observed by:** [who, what they saw] · **Filmed:** [yes/no]

**Preceding 24h:** [sleep / food / alcohol / stress / travel / meds / cycle / weather]

**Treatment:** [what, how much it helped, how fast]

**Different from usual:** [anything notable, or "no — matched the usual pattern"]

**Follow-up:** [time-critical test booked? ER visit? new open loops?]
```
