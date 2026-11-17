"""SessionStart(source=compact) hook: put the compaction audit's blockers into the fresh context.

Why SessionStart and not PreCompact: in one project's transcripts (2026-09-29) text printed by a PreCompact hook
reached the post-compaction context in 0 of 24 automatic compactions, while SessionStart with source "compact"
reached 24 of 24 (record: ~/.claude/solutions/vcc-2026-harvest/records/ROUTINE-COMPACTION-CHECK-2026-09-29.md).

Registered under SessionStart with matcher "compact", through hooks/interop-guard-shim.py so a moved file is a quiet
allow. It runs compaction_audit.py --root <payload cwd> --own-ledger-only (other sessions' commitment ledgers are not
this session's; hooks/commitment-surfacer.py re-injects the session's own), adds --no-cr-sweep when the root is the
home folder, ~/.claude or AppData (trees too large to walk in time), and prints the VERDICT counts always, then at
most a few items per severity, as additionalContext. Fails open: a timeout or any failure emits a one-line note
saying how to run the audit by hand, and exits 0, so it can never block a session start.

    python session_start_compact.py            (reads the hook payload on stdin)
    python session_start_compact.py --selftest
"""

import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIT = os.path.join(HERE, "compaction_audit.py")
TIMEOUT = 25
PER_SEVERITY = 6


def norm(p: str) -> str:
    return os.path.normcase(os.path.abspath(p)).replace("\\", "/").rstrip("/")


def large_tree(root: str) -> bool:
    home = norm(os.path.expanduser("~"))
    r = norm(root)
    big = [home + "/.claude", home + "/appdata"]
    return r == home or any(r == b or r.startswith(b + "/") for b in big)


def manual(cwd: str) -> str:
    return "python %s --root %s" % (AUDIT, cwd)


def summarise(stdout: str) -> list[str]:
    lines = stdout.splitlines()
    try:
        start = max(i for i, x in enumerate(lines) if x.strip() == "VERDICT")
    except ValueError:
        return []
    groups: dict[str, list[str]] = {}
    order: list[str] = []
    cur = None
    for x in lines[start + 2 :]:
        s = x.strip()
        if not s or x.startswith("="):
            continue
        head = s.split(":", 1)[0]
        if head in ("ERROR", "BLOCK", "NOTE") and s[len(head) + 1 :].strip().isdigit():
            cur = s
            order.append(cur)
            groups[cur] = []
        elif cur and s.startswith("- "):
            groups[cur].append(x.rstrip())
    out: list[str] = []
    for c in order:
        out.append("   " + c)
        items = groups[c]
        out += items[:PER_SEVERITY]
        if len(items) > PER_SEVERITY:
            out.append("      ... %d more" % (len(items) - PER_SEVERITY))
    return out


def build_context(cwd: str, timeout: int = TIMEOUT) -> str:
    args = [sys.executable, AUDIT, "--root", cwd, "--own-ledger-only"]
    if large_tree(cwd):
        args.append("--no-cr-sweep")
    try:
        proc = subprocess.run(
            args, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout
        )
    except subprocess.TimeoutExpired:
        return "compaction-check: the audit of %s ran past %d s and was skipped; run it by hand: %s" % (
            cwd,
            timeout,
            manual(cwd),
        )
    block = summarise(proc.stdout)
    if not block:
        return "compaction-check: audit printed no VERDICT (rc %d); run it by hand: %s" % (proc.returncode, manual(cwd))
    head = "compaction-check after compaction (audit of %s, rc %d; full list: %s):" % (
        cwd,
        proc.returncode,
        manual(cwd),
    )
    return "\n".join([head] + block)


def emit(context: str) -> None:
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": context}}))


def main() -> int:
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
        if payload.get("source", "compact") != "compact":
            return 0
        cwd = payload.get("cwd") or os.getcwd()
        emit(build_context(cwd))
    except Exception as exc:  # fail open by design
        print("compaction-check hook skipped: %s" % exc, file=sys.stderr)
    return 0


def run_hook(payload: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, os.path.abspath(__file__)], input=payload, capture_output=True, text=True
    )


def selftest() -> int:
    results = []
    with tempfile.TemporaryDirectory() as root:
        with open(os.path.join(root, "OPERATOR-INBOX.md"), "w", encoding="utf-8") as fh:
            fh.write("## OPEN\n### OPEN 2026-01-01: planted row\n## CLOSED\n")
        ctx = build_context(root)
        results.append(("planted OPEN inbox row surfaces in the context", "planted row" in ctx))
    with tempfile.TemporaryDirectory() as root:
        ctx = build_context(root)
        results.append(
            (
                "empty root: all three counts present, no planted row",
                all(k + ":" in ctx for k in ("ERROR", "BLOCK", "NOTE")) and "planted row" not in ctx,
            )
        )
        many = "\n".join(["   ERROR: 0", "   BLOCK: 9"] + ["      - item %d" % i for i in range(9)] + ["   NOTE: 2"])
        many += "\n      - n1\n      - n2\n"
        s = "\n".join(summarise("=" * 5 + "\nVERDICT\n" + "=" * 5 + "\n" + many))
        results.append(
            (
                "a long BLOCK list never hides the NOTE count",
                "NOTE: 2" in s and "item 5" in s and "item 6" not in s and "3 more" in s,
            )
        )
        ctx = build_context(root, timeout=0)
        results.append(("timeout emits a by-hand note, no exception", "ran past 0 s" in ctx and "--root" in ctx))
    results.append(("home folder is treated as a large tree", large_tree(os.path.expanduser("~"))))
    results.append(("a normal project is not", not large_tree(os.path.join(os.path.expanduser("~"), "DEV", "x"))))
    p = run_hook(json.dumps({"source": "startup", "cwd": "C:/nonexistent"}))
    results.append(("source=startup prints nothing, rc 0", p.returncode == 0 and p.stdout.strip() == ""))
    p = run_hook("not json")
    results.append(("bad payload fails open, rc 0", p.returncode == 0 and p.stdout.strip() == ""))
    for name, ok in results:
        print("   %-50s %s" % (name, "PASS" if ok else "FAIL"))
    allok = all(ok for _n, ok in results)
    print("SELFTEST %s: %d of %d" % ("ALL_PASS" if allok else "FAILED", sum(ok for _n, ok in results), len(results)))
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main())
