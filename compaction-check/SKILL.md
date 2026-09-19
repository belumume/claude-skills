---
name: compaction-check
description: Answer the operator's compaction question (can I /compact now, is everything compounded and non-stale, is anything outstanding) by re-deriving the answer rather than recalling it. Use whenever he asks whether to compact, whether the session is ready to close, whether everything is compounded, or when he re-sends "compound, compact, handoff.txt"; and unprompted before any planned compaction.
---

# Compaction check

Global. Runs in any project. The **method** here is portable; a project may add its own audit
script, and if it has one, that script runs first and this file is the part it cannot do.

Known project-specific audits, checked by existence and never assumed:
- `DEV/Learning` and `DEV/Learning/vcc-2026`:
  `DEV/Learning/vcc-2026/.venv/Scripts/python.exe DEV/Learning/vcc-2026/research/_compaction_audit.py`
  (ten checks, fails closed; that project's own `.claude/skills/compaction-check/SKILL.md` documents
  them). Do not run it outside those projects: its checks name HANDOFF, MISSION, submission rows and
  science messages, which do not exist elsewhere, and it would ERROR at step one.

## What he is actually asking

Two things, and neither is "have you been diligent":

1. Would compacting **right now lose anything**?
2. Is anything **he could act on** sitting unsaid?

Answer both, with numbers, in plain English. He keeps twelve phrasings of this in
`~/PC/Downloads/compound, compact, handoff.txt`; they reduce to: everything compounded, nothing
stale, nothing outstanding. He asks more than once in an evening because the answer must be
**re-derived each time**. Re-deriving it is the whole job.

## Never answer from recall

Measured repeatedly: the honest answer was reached by checking and would have been wrong from
memory. On 2026-09-19, three consecutive "is it ready to close" asks each turned up something real,
and the third one corrected the second. The check is cheap; his trust in the answer is not.

## The audit, whatever the project

1. **Is every in-flight delegate actually alive?** A task marked in progress behind a dead lane is
   the worst state to compact on. Check the lane; do not infer it. Resume a dead one from its
   transcript, do not relaunch it fresh.
2. **Did anything learned this session belong somewhere more durable than the transcript?** A rule
   that governs future sessions goes in the project's standing doc or `~/.claude/CLAUDE.md`. A
   cross-project lesson goes in a memory file. A thing that must not recur becomes a control or a
   guard, not a paragraph. A caveat living only inside a document's conclusion is invisible.
3. **Was any claim made this session that has not been verified since?** Especially a totality claim
   (all, none, every, clean, N of N), and especially one already sent to him or to an outside surface.
4. **Is a correction owed**, to him or to another surface? Send it before compacting, not after.
5. **Does any operator-inbox row gate on him for something a live page, file or installed skill
   already answers?** Those rows are the defect, not the wall. Probe before leaving one open.
6. **Run the class check on anything fixed this session.** Fixing one instance and leaving the class
   is the most repeated failure in this corpus. Enumerate by SEARCHING THE TREE, never from a list
   you expect to be complete, and remember a skill is a DIRECTORY, a hook may be registered in a
   nested `settings.json`, and a flat `listdir` is not a denominator.
7. **Check the instruments, not just the readings.** Every zero needs a known-positive control in
   the same run. On 2026-09-19 four separate searches returned confident wrong answers in one
   session, each caught only by a control.

## How to answer him

Verdict first, then the evidence, in his terms and not in harness jargon. If yes, say what was
checked and what was fixed in this pass, because "nothing to do" is credible only beside what was
looked at. If no, say precisely what is outstanding and how long it takes. Never close on a question
when the action can be taken.

## If the audit finds something

Fix it, then re-run and quote the clean output. Do not report a finding as acceptable without a
reason he could check. A note about history predating a convention is fine to leave with that reason
stated; anything from this session is work.
