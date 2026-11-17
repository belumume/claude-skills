"""Portable compaction audit: the checks from vcc-2026's research/_compaction_audit.py that apply to any project.

Written 2026-11-10 when vcc-2026 (whose 1,698-line audit this skill used to run) left this PC; the verbatim original is
~/.claude/solutions/vcc-2026-harvest/code-snapshot/research/_compaction_audit.py. Same contract: every line comes from a
command in this run, a check that cannot run is ERROR, and ERROR counts as a blocker. It reports; it never edits.

    python compaction_audit.py [--root <project>] [--tasks-dir <dir>] [--hours 24]
    python compaction_audit.py --selftest

Checks (each skips with a printed reason when its input does not exist in this project):
  1. open tasks in the Claude Code task list (--tasks-dir, else ~/.claude/tasks/$CLAUDE_CODE_TASK_LIST_ID)
  2. anti-drop ledger commitments still open (~/.claude/.commitments/<slug>.jsonl for the root and its parents)
  3. OPEN rows in <root>/OPERATOR-INBOX.md
  4. HANDOFF.md: carriage returns and the newest dated '## ' section
  5. carriage returns in .md/.py files modified in the last --hours, with a known-positive control
  6. project memory files missing from MEMORY.md (~/.claude/projects/<slug>/memory)
"""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import time

CR = chr(13).encode()
SKIP_DIRS = ("/.venv", "/.git", "/node_modules", "/__pycache__", "/.ruff_cache")


def slug(path: str) -> str:
    return re.sub(r"[^A-Za-z0-9-]", "-", os.path.abspath(path))


class Audit:
    def __init__(self, root: str, home: str, tasks_dir: str | None, hours: float,
                 own_ledger_only: bool = False, cr_sweep: bool = True):
        self.root = os.path.abspath(root).replace(os.sep, "/")
        self.home = home
        self.tasks_dir = tasks_dir
        self.hours = hours
        self.own_ledger_only = own_ledger_only
        self.cr_sweep = cr_sweep
        self.findings: list[tuple[str, str]] = []

    def git_lf(self) -> set[str]:
        """Paths (relative, /-separated) whose committed copy is LF. With core.autocrlf true, git writes CRLF
        into the working copy of every such file, so a CR there is a checkout artefact, not a defect."""
        if not hasattr(self, "_git_lf"):
            self._git_lf: set[str] = set()
            try:
                out = subprocess.run(["git", "-C", self.root, "ls-files", "--eol"], capture_output=True,
                                     text=True, encoding="utf-8", errors="replace", timeout=20).stdout
                for line in out.splitlines():
                    parts = line.split("\t", 1)
                    if len(parts) == 2 and parts[0].startswith("i/lf "):
                        self._git_lf.add(parts[1].strip())
            except (OSError, subprocess.SubprocessError):
                pass
        return self._git_lf

    def add(self, sev: str, line: str) -> None:
        self.findings.append((sev, line))

    def head(self, t: str) -> None:
        print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)

    def check_tasks(self) -> None:
        self.head("1. TASKS: open items in the task list")
        d = self.tasks_dir
        if not d:
            lid = os.environ.get("CLAUDE_CODE_TASK_LIST_ID")
            d = os.path.join(self.home, ".claude", "tasks", lid) if lid else None
        if not d:
            print("   no --tasks-dir and no CLAUDE_CODE_TASK_LIST_ID: skipped (say so in the answer)")
            self.add("NOTE", "task list not audited: no --tasks-dir and no CLAUDE_CODE_TASK_LIST_ID")
            return
        if not os.path.isdir(d):
            self.add("ERROR", "task directory %s is missing" % d)
            print("   ERROR: no task directory %s" % d)
            return
        names, skipped, rows = [], [], []
        for x in os.listdir(d):
            stem, ext = os.path.splitext(x)
            (names if ext == ".json" and stem.isdigit() else skipped).append(x)
        for f in sorted(names, key=lambda x: int(os.path.splitext(x)[0])):
            try:
                t = json.load(io.open(os.path.join(d, f), encoding="utf-8"))
            except Exception as exc:  # noqa: BLE001
                self.add("ERROR", "task file %s unreadable: %s" % (f, exc))
                continue
            if t.get("status") != "completed":
                rows.append((str(t.get("id")), str(t.get("status")), (t.get("subject") or "")[:88]))
        print("   %d task file(s) read | %d non-task file(s) skipped%s" % (len(names), len(skipped),
              (": " + ", ".join(sorted(skipped))) if skipped else ""))
        print("   %d not completed" % len(rows))
        for i, s, subj in rows:
            print("   %-5s %-12s %s" % (i, s, subj))
        print("   VERIFY BY HAND: is every in_progress task's delegate actually alive?")

    def ledgers(self) -> list[str]:
        out, p = [], self.root
        while True:
            f = os.path.join(self.home, ".claude", ".commitments", slug(p) + ".jsonl")
            if os.path.isfile(f):
                out.append(f)
            if self.own_ledger_only:
                return out
            parent = os.path.dirname(p)
            if parent == p:
                return out
            p = parent

    def check_ledger(self) -> None:
        self.head("2. ANTI-DROP LEDGER: commitments still open")
        files = self.ledgers()
        if not files:
            print("   no ledger for this root or its parents (fine if none was ever written)")
            return
        status: dict[str, str] = {}
        text: dict[str, str] = {}
        for f in files:
            for line in io.open(f, encoding="utf-8", errors="replace"):
                try:
                    d = json.loads(line)
                except Exception:  # noqa: BLE001
                    continue
                h = d.get("h")
                if h:
                    status[h] = d.get("status", status.get(h, "open"))
                    if d.get("text"):
                        text[h] = " ".join(str(d["text"]).split())
        openh = [h for h, s in status.items() if s != "done"]
        print("   ledgers: %s | %d commitments, %d open" % (", ".join(os.path.basename(f) for f in files), len(status), len(openh)))
        for h in openh:
            self.add("BLOCK", "anti-drop commitment still open: %s %s" % (h, text.get(h, "")[:80]))
            print("   OPEN %s %s" % (h, text.get(h, "")[:90]))

    def check_inbox(self) -> None:
        self.head("3. OPERATOR INBOX: OPEN rows")
        p = self.root + "/OPERATOR-INBOX.md"
        if not os.path.isfile(p):
            print("   no OPERATOR-INBOX.md in this project")
            return
        t = io.open(p, encoding="utf-8", errors="replace").read()
        open_block = re.split(r"(?m)^## CLOSED[ \t]*$", t)[0]
        rows = re.findall(r"^### (OPEN\b.*)$", open_block, re.M)
        print("   %d OPEN row(s)" % len(rows))
        for r in rows:
            self.add("NOTE", "operator inbox row open: " + r[:110])
            print("   OPEN: " + r[:110])

    def check_handoff(self) -> None:
        self.head("4. HANDOFF.md: line endings and newest dated section")
        p = self.root + "/HANDOFF.md"
        if not os.path.isfile(p):
            print("   no HANDOFF.md in this project")
            return
        b = io.open(p, "rb").read()
        text = b.decode("utf-8", "replace")
        heads = re.findall(r"^## (.*)$", text, re.M)
        dated = sorted(m.group(1) for h in heads for m in [re.search(r"(\d{4}-\d\d-\d\dT\d\d:\d\d(?::\d\d)?Z?)", h)] if m)
        print("   %d B | CR %d | %d '## ' sections | newest stamp: %s" % (len(b), b.count(CR), len(heads), dated[-1] if dated else "none"))
        if b.count(CR) and "HANDOFF.md" in self.git_lf():
            print("   CR is git's autocrlf checkout of an LF-committed file: not flagged")
        elif b.count(CR):
            self.add("BLOCK", "HANDOFF.md carries %d carriage returns" % b.count(CR))

    def check_cr(self) -> None:
        self.head("5. LINE ENDINGS in files modified in the last %g h, with a known positive" % self.hours)
        if not self.cr_sweep:
            print("   skipped (--no-cr-sweep)")
            return
        ctrl = ("a" + chr(13) + chr(10) + "b" + chr(13) + chr(10)).encode()
        ok = ctrl.count(CR) == 2
        print("   control: a 2-CR string reads as %d CR -> instrument works: %s" % (ctrl.count(CR), ok))
        if not ok:
            self.add("ERROR", "the CR detector failed its own control; its zero means nothing")
            return
        cutoff = time.time() - self.hours * 3600
        targets, bad, vendored = [], [], []
        for d, dirs, files in os.walk(self.root):
            dn = d.replace(os.sep, "/")
            if dn != self.root and ".git" in dirs + files:
                vendored.append(dn[len(self.root) + 1:])
                dirs[:] = []
                continue
            if any(x in dn + "/" for x in (s + "/" for s in SKIP_DIRS)):
                dirs[:] = []
                continue
            for f in files:
                if f.endswith((".md", ".py")):
                    p = os.path.join(d, f)
                    try:
                        if os.path.getmtime(p) > cutoff:
                            targets.append(p)
                            rel = os.path.relpath(p, self.root).replace(os.sep, "/")
                            if io.open(p, "rb").read().count(CR) and rel not in self.git_lf():
                                bad.append(p)
                    except OSError as exc:
                        self.add("NOTE", "not swept (%s): %s" % (type(exc).__name__, p))
        print("   %d file(s) modified | %d with carriage returns | %d nested git checkout(s) skipped: %s"
              % (len(targets), len(bad), len(vendored), ", ".join(vendored) or "none"))
        for p in bad[:20]:
            rel = os.path.relpath(p, self.root)
            self.add("NOTE", "carriage returns in " + rel)
            print("   CR: " + rel)

    def check_memory(self) -> None:
        self.head("6. PROJECT MEMORY: index and files agree")
        mem = os.path.join(self.home, ".claude", "projects", slug(self.root), "memory")
        if not os.path.isdir(mem):
            print("   no memory directory %s" % mem)
            return
        idx = os.path.join(mem, "MEMORY.md")
        t = io.open(idx, encoding="utf-8", errors="replace").read() if os.path.isfile(idx) else ""
        files = [f for f in os.listdir(mem) if f.endswith(".md") and f != "MEMORY.md"]
        named = set(re.findall(r"\]\(([^)\s]+\.md)\)", t)) | set(re.findall(r"(?<![\w.-])([\w.-]+\.md)(?![\w.-])", t))
        unindexed = [f for f in files if f not in named]
        print("   %d memory file(s), %d not named in MEMORY.md" % (len(files), len(unindexed)))
        for f in unindexed:
            self.add("NOTE", "memory file not in the index: " + f)
            print("   UNINDEXED: " + f)

    def run(self) -> int:
        print("COMPACTION AUDIT (portable)  %s\nproject: %s" % (time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), self.root))
        if not os.path.isdir(self.root):
            self.add("ERROR", "project root %s does not exist" % self.root)
        else:
            for fn in (self.check_tasks, self.check_ledger, self.check_inbox, self.check_handoff, self.check_cr, self.check_memory):
                try:
                    fn()
                except Exception as exc:  # noqa: BLE001
                    self.add("ERROR", "%s raised %s: %s" % (fn.__name__, type(exc).__name__, exc))
        self.head("VERDICT")
        for label in ("ERROR", "BLOCK", "NOTE"):
            items = [x for s, x in self.findings if s == label]
            print("   %s: %d" % (label, len(items)))
            for x in items:
                print("      - " + x)
        blocked = any(s in ("ERROR", "BLOCK") for s, _ in self.findings)
        print("\n   " + ("NOT READY. Clear the ERROR and BLOCK items, then re-run." if blocked else
              "No blockers found by these checks. THIS IS NOT THE ANSWER: judge by hand that every in_progress delegate "
              "is alive, that lessons went somewhere durable, that no claim is unverified, and that no correction is owed."))
        return 1 if blocked else 0


def selftest() -> int:
    results = []
    with tempfile.TemporaryDirectory() as td:
        home = os.path.join(td, "home")
        root = os.path.join(td, "proj")
        tasks = os.path.join(td, "tasks")
        for d in (root, tasks):
            os.makedirs(d)
        clean = Audit(root, home, tasks, 24)
        io.open(os.path.join(root, "a.md"), "w", newline="\n").write("ok\n")
        clean.run()
        results.append(("clean project: no BLOCK, no ERROR, no NOTE", not clean.findings))
        io.open(os.path.join(root, "b.md"), "wb").write(b"x\r\ny\r\n")
        io.open(os.path.join(root, "HANDOFF.md"), "wb").write(b"## 2026-01-01T00:00Z one\r\nbody\r\n")
        io.open(os.path.join(root, "OPERATOR-INBOX.md"), "w").write("## OPEN\n### OPEN 2026-01-01: thing\n## CLOSED\n")
        json.dump({"id": 1, "status": "in_progress", "subject": "s"}, io.open(os.path.join(tasks, "1.json"), "w"))
        io.open(os.path.join(tasks, "1.json.bak"), "w").write("{}")
        led = os.path.join(home, ".claude", ".commitments")
        os.makedirs(led)
        io.open(os.path.join(led, slug(root) + ".jsonl"), "w").write(json.dumps({"h": "abc", "text": "do x"}) + "\n")
        mem = os.path.join(home, ".claude", "projects", slug(root), "memory")
        os.makedirs(mem)
        io.open(os.path.join(mem, "MEMORY.md"), "w").write("# index\n")
        io.open(os.path.join(mem, "orphan.md"), "w").write("x\n")
        dirty = Audit(root, home, tasks, 24)
        rc = dirty.run()
        txt = "\n".join(x for _s, x in dirty.findings)
        results += [
            ("planted CR in b.md caught", "carriage returns in b.md" in txt),
            ("planted CR in HANDOFF.md is a BLOCK", ("BLOCK", "HANDOFF.md carries 2 carriage returns") in dirty.findings),
            ("planted open inbox row caught", "operator inbox row open" in txt),
            ("planted open ledger commitment is a BLOCK", any(s == "BLOCK" and "abc" in x for s, x in dirty.findings)),
            ("planted unindexed memory file caught", "orphan.md" in txt),
            ("dirty project exits 1", rc == 1),
        ]
        io.open(os.path.join(led, slug(td) + ".jsonl"), "w").write(json.dumps({"h": "zzz", "text": "parent"}) + "\n")
        walk = Audit(root, home, tasks, 24)
        walk.run()
        own = Audit(root, home, tasks, 24, own_ledger_only=True, cr_sweep=False)
        own.run()
        wt = "\n".join(x for _s, x in walk.findings)
        ot = "\n".join(x for _s, x in own.findings)
        results += [
            ("default mode reads the parent's ledger", "zzz" in wt),
            ("--own-ledger-only keeps own row, drops the parent's", "abc" in ot and "zzz" not in ot),
            ("--no-cr-sweep drops the CR notes", "carriage returns in b.md" in wt and "carriage returns in b.md" not in ot),
        ]
        g = os.path.join(td, "gitproj")
        os.makedirs(g)
        q = {"capture_output": True, "cwd": g}
        subprocess.run(["git", "init", "-q"], **q)
        subprocess.run(["git", "config", "core.autocrlf", "false"], **q)
        io.open(os.path.join(g, "c.md"), "wb").write(b"x\ny\n")
        subprocess.run(["git", "add", "c.md"], **q)
        subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "t"], **q)
        io.open(os.path.join(g, "c.md"), "wb").write(b"x\r\ny\r\n")
        io.open(os.path.join(g, "u.md"), "wb").write(b"x\r\ny\r\n")
        ga = Audit(g, home, tasks, 24)
        ga.run()
        gt = "\n".join(x for _s, x in ga.findings)
        results += [
            ("LF-committed file with CRLF working copy not flagged", "c.md" not in gt),
            ("untracked CRLF file still flagged", "carriage returns in u.md" in gt),
        ]
        missing = Audit(os.path.join(td, "nope"), home, None, 24)
        results.append(("absent root is an ERROR, exit 1", missing.run() == 1 and missing.findings[0][0] == "ERROR"))
        gone = Audit(root, home, os.path.join(td, "no-tasks"), 24)
        gone.run()
        results.append(("missing task dir is an ERROR (fails closed)", any(s == "ERROR" and "task directory" in x for s, x in gone.findings)))
    print("\n" + "-" * 78)
    for name, ok in results:
        print("   %-60s %s" % (name, "PASS" if ok else "FAIL"))
    allok = all(ok for _n, ok in results)
    print("SELFTEST %s: %d of %d" % ("ALL_PASS" if allok else "FAILED", sum(ok for _n, ok in results), len(results)))
    return 0 if allok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").split("\n")[0])
    ap.add_argument("--root", default=os.getcwd())
    ap.add_argument("--tasks-dir")
    ap.add_argument("--hours", type=float, default=24.0)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--own-ledger-only", action="store_true",
                    help="read only this root's commitment ledger, not its parents' (hook mode)")
    ap.add_argument("--no-cr-sweep", action="store_true", help="skip the line-ending sweep of the whole tree")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    return Audit(a.root, os.path.expanduser("~"), a.tasks_dir, a.hours,
                 own_ledger_only=a.own_ledger_only, cr_sweep=not a.no_cr_sweep).run()


if __name__ == "__main__":
    sys.exit(main())
