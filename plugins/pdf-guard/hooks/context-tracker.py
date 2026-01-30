#!/usr/bin/env python3
"""
Tracks cumulative file reads across a session.
Warns when approaching estimated context limits.
Suggests compaction or subagent delegation.
"""

import json
import os
import sys
from pathlib import Path

# Thresholds (estimated tokens)
WARN_CUMULATIVE = 100_000  # Warn at ~100K tokens read
BLOCK_CUMULATIVE = 150_000  # Block at ~150K tokens (leave room for conversation)

# State file (per session)
STATE_DIR = Path.home() / ".claude" / "state"
BYTES_PER_TOKEN = 4


def get_session_id() -> str:
    """Get current session ID from hook input."""
    try:
        # Session ID passed in hook data
        data = json.loads(os.environ.get("CLAUDE_HOOK_DATA", "{}"))
        return data.get("session_id", "unknown")
    except Exception:
        return "unknown"


def get_state_file(session_id: str) -> Path:
    """Get state file path for this session."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    return STATE_DIR / f"read_tracker_{session_id}.json"


def load_state(session_id: str) -> dict:
    """Load read tracking state for session."""
    state_file = get_state_file(session_id)
    if state_file.exists():
        try:
            return json.loads(state_file.read_text())
        except Exception:
            pass
    return {"total_bytes": 0, "read_count": 0, "files": []}


def save_state(session_id: str, state: dict):
    """Save read tracking state."""
    state_file = get_state_file(session_id)
    state_file.write_text(json.dumps(state, indent=2))


def get_file_size(path: str) -> int | None:
    """Get file size."""
    try:
        path = os.path.expanduser(path)
        return os.path.getsize(path)
    except Exception:
        return None


def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = data.get("tool_name", "")
    if tool_name != "Read":
        sys.exit(0)

    tool_input = data.get("tool_input", {})
    file_path = tool_input.get("file_path", "")
    session_id = data.get("session_id", "unknown")

    # Skip images and PDFs (handled separately)
    lower_path = file_path.lower()
    if any(
        lower_path.endswith(ext)
        for ext in [".pdf", ".png", ".jpg", ".jpeg", ".gif", ".webp"]
    ):
        sys.exit(0)

    # Get file size
    size = get_file_size(file_path)
    if size is None:
        sys.exit(0)

    # Load session state
    state = load_state(session_id)
    current_total = state["total_bytes"]
    new_total = current_total + size

    estimated_tokens = new_total // BYTES_PER_TOKEN

    # Block if cumulative reads exceed limit
    if estimated_tokens > BLOCK_CUMULATIVE:
        output = {
            "continue": False,
            "stopReason": f"BLOCKED: Cumulative reads approaching context limit.\n\n"
            f"Session stats:\n"
            f"  - Files read: {state['read_count']}\n"
            f"  - Total bytes: {current_total:,}\n"
            f"  - Estimated tokens: {estimated_tokens:,}\n\n"
            f"Options:\n"
            f"1. Run /compact to compress conversation history\n"
            f"2. Delegate remaining work to a subagent (Task tool)\n"
            f"3. Start a new conversation for fresh context\n\n"
            f"This file ({size:,} bytes) would push total to {new_total:,} bytes.",
        }
        print(json.dumps(output))
        sys.exit(0)

    # Warn if approaching limit
    if estimated_tokens > WARN_CUMULATIVE:
        print(
            f"WARNING: High cumulative reads ({state['read_count']} files, ~{estimated_tokens:,} tokens). "
            f"Consider using /compact or delegating to subagents soon.",
            file=sys.stderr,
        )

    # Update state (will be saved by PostToolUse or we save optimistically)
    state["total_bytes"] = new_total
    state["read_count"] += 1
    state["files"].append({"path": file_path, "size": size})
    save_state(session_id, state)

    sys.exit(0)


if __name__ == "__main__":
    main()
