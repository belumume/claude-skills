---
name: compaction-check
description: Answer the operator's compaction question (can I /compact now, is everything compounded and non-stale, is anything outstanding) by re-deriving the answer rather than recalling it. Use whenever he asks whether to compact, whether the session is ready to close, whether everything is compounded, or when he re-sends "compound, compact, handoff.txt"; and unprompted before any planned compaction.
metadata:
  version: 0.2.0
  tags:
    - session-management
    - compaction
    - verification
---

# Compaction check

> **Merged 2026-09-23.** Two documents shared this name and shadowed each other: this user-scope copy
> (`~/.claude/skills/compaction-check/SKILL.md`, local-only, not committed, 2026-09-19) and a project-scope copy at
> `~/DEV/Learning/.claude/skills/compaction-check/SKILL.md` (2026-09-16), which never
> loaded because a personal skill wins a name collision (A430, Gap 1). The project copy's frontmatter
> read, verbatim: `description: Answer the operator's compaction question (can I /compact now, is everything compounded and non-stale, is anything outstanding) with a full audit rather than recall. Use whenever he asks whether to compact or close the session, whenever he re-sends the twelve-question file, and unprompted before any planned compaction.`
> A third file, `~/DEV/Learning/vcc-2026/.claude/skills/compaction-check/MOVED.md`
> (2026-09-16, 232 bytes), read in full: `Moved to ~/DEV/Learning/.claude/skills/compaction-check/ on 2026-09-16, because Claude Code registers skills from the project root (DEV/Learning), not from this sub-project. This directory is kept only as this pointer.`
> Both project files are deleted; every text run of 40 or more characters from both SKILL.md copies
> is present here, proof and must-fail control in
> `~/.claude/solutions/vcc-2026-harvest/records/A431-SKILL-MERGE-2026-09-23.md` (copied out of the vcc-2026 project before its deletion). Where the two
> disagreed, BOTH statements are kept with dates under a **CONTRADICTION** marker.

Global. Runs in any project. The **method** here is portable; a project may add its own audit
script, and if it has one, that script runs first and this file is the part it cannot do.

The audit script ships with this skill since 2026-11-10 and runs in any project:

    python ~/.claude/skills/compaction-check/compaction_audit.py --root <project> [--tasks-dir ~/.claude/tasks/<list>]
    python ~/.claude/skills/compaction-check/compaction_audit.py --selftest

A project may still add its own audit script; if it has one, that script runs first, then this one, and this
file is the part neither can do. Until 2026-11-10 this section pointed at vcc-2026's 1,698-line
`research/_compaction_audit.py`; that project left this PC, its verbatim copy is in
`~/.claude/solutions/vcc-2026-harvest/code-snapshot/research/`, and the checks that apply to any project were
re-implemented in `compaction_audit.py` here.

## Where this skill lives, and a superseded claim kept as a record

The project copy opened with this sentence, kept verbatim and dated 2026-09-16:

> This skill lives at the Learning project root because that is the directory Claude Code registers skills from; the audit it runs belongs to the vcc-2026 sub-project and the command above names it by absolute path.

> **CONTRADICTION, dated.** That claim (2026-09-16, and the MOVED.md pointer of the same day) is the
> inverse of the documented rule, read from code.claude.com on 2026-09-23 (A430): skills load from the
> directory a session STARTS in and from its parent directories, and on a name collision the order is
> Enterprise, then Personal, then Project. A copy at the Learning root therefore loaded only for a
> session started in or under `DEV/Learning`, and even then lost the collision to this user-scope file,
> so from 2026-09-19 (when this file was written) to 2026-09-23 the project copy reached no session.
> The user scope is the location that loads everywhere; that is why the merge landed here.

## What he is actually asking

Two things, and neither is "have you been diligent":

1. Would compacting **right now lose anything**?
2. Is anything **he could act on** sitting unsaid?

Answer both, with numbers, in plain English. He keeps twelve phrasings of this in
`~/PC/Downloads/compound, compact, handoff.txt`; they reduce to: everything compounded, nothing
stale, nothing outstanding. He asks more than once in an evening because the answer must be
**re-derived each time**. Re-deriving it is the whole job.

The project copy put the same two points this way (2026-09-16):

He keeps twelve questions in `~/PC/Downloads/compound, compact, handoff.txt`. They are twelve
phrasings of three: **is everything worth compounding compounded, is anything stale, is anything
outstanding.** He has asked in the same evening more than once because the answer must be re-derived
each time, not remembered. Re-deriving it is the whole job.

Not "have you been diligent". He is asking whether a compaction right now would **lose** anything, and
whether anything he could act on is sitting unsaid. Answer those two, with numbers.

## Never answer from recall

Measured repeatedly: the honest answer was reached by checking and would have been wrong from
memory. On 2026-09-19, three consecutive "is it ready to close" asks each turned up something real,
and the third one corrected the second. The check is cheap; his trust in the answer is not.

**Never answer from recall.** Twice in one evening the honest answer was reached by checking and would
have been wrong from memory. The check is cheap; his trust in the answer is not.

## Run this first, always

    python ~/.claude/skills/compaction-check/compaction_audit.py --root <project> [--tasks-dir <dir>]

Six checks, every line produced by a command in the same run, failing closed: a check that cannot run reports
ERROR and ERROR counts as a blocker; an input the project does not have (no inbox, no HANDOFF, no memory
directory) is skipped with a printed line. The carriage-return sweep carries its own known-positive control,
because a zero from a filter is not evidence until that filter has caught a positive in the same run.
`--selftest` plants one positive per check plus an absent root and a missing task directory, and prints its own
pass count.

It covers: open tasks in the task list (`--tasks-dir`, else `$CLAUDE_CODE_TASK_LIST_ID`); open anti-drop ledger
commitments for the root and its parents; OPEN operator-inbox rows; HANDOFF's line endings and newest dated
section; line endings across `.md`/`.py` files touched in 24 hours; and memory files missing from the index.

The vcc-2026 version also checked science-surface messages, submission rows, armed submissions and the
operator-notes follow-through; those were that project's and are not ported. Its routine half (his words
2026-09-29: "at every turn or end of long/focused run/work/checkpoint/chunk/stretch/, do/run/check
/compaction-check and "everything objectively best" automatically/routinely/periodically without me needing to be in
the loop.") ran as the scheduled task `VCC2026-CompactionAudit`, deleted with the project on 2026-11-10; record
`~/.claude/solutions/vcc-2026-harvest/records/ROUTINE-COMPACTION-CHECK-2026-09-29.md`. His later words (2026-10-09):
"if it gonna be happening, you might as well autoconfigure/force full /compaction-check before idles."

**Surface the blockers at SessionStart with source `compact`, not at PreCompact.** Measured in that project
(2026-09-29): text a PreCompact hook printed reached the post-compaction context in 0 of 24 automatic compactions
(7 of 7 manual ones), while SessionStart with source `compact` reached 24 of 24. Idle compaction exists too and is
logged as trigger "manual" (setting `idleCompaction`), so nothing typed precedes it. The hook that does this ships
here: `session_start_compact.py` (runs `compaction_audit.py --root <cwd> --own-ledger-only`, adds `--no-cr-sweep`
for the home folder, `~/.claude` and AppData, and prints the ERROR/BLOCK/NOTE counts plus a few items each into the
fresh context; a 25 s limit; fails open; `--selftest`). It is registered in `~/.claude/settings.json` under
SessionStart with matcher `compact`, through `~/.claude/hooks/interop-guard-shim.py --timeout=60` so a moved file is a
quiet allow. To prove it fires: `claude -p` once with `--output-format json`, then `claude -p "/compact" --resume
<session_id>` (prefix `MSYS_NO_PATHCONV=1` in Git Bash), and look for "compaction-check after compaction" in that
session's transcript after the `compact_boundary` record and not in its startup records. The audit's CR checks skip a
file whose committed copy is LF, since `core.autocrlf` is true on this PC. Records:
`~/.claude/solutions/hook-architecture/hook-delivery-channels-and-registration.md` section 1;
`~/.claude/solutions/claude-code-tooling/compaction-memory-index-and-operator-message-shapes.md` section 1.

**Enumerate the whole window, not the recent end.** His words, pasted at least ten times 2026-09-10 to 10-03: "i
really mean the whole arc/transcript/work/progress/journey/prompts/lessons/failure-modes, not just recent bias
where your attention/recall is more strong/recent". Enumerate the window from its first record by script or
indexed read; recall weights the recent end.

**Read its NOTES as well as its blockers.** A NOTE is where an input that was skipped shows up; a skipped
input read as "nothing to report" is how a lost record goes unnoticed.

## Then do the part the script cannot

Each of these needs a command or a read, not a memory. Items 1 to 4 came from the original project's audit;
5 to 7 were added 2026-09-19.

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

## If the audit reports something

Fix it, then re-run the script and quote the clean output. Do not report a finding as acceptable
without a reason he could check. A NOTE about history (rows predating a convention) is fine to leave
with that reason stated; a NOTE about anything from this session is work.
