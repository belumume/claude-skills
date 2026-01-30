#!/usr/bin/env python3
"""
PreToolUse hook to warn about large files that might cause context exhaustion.
Suggests chunked reading or subagent delegation for files over threshold.
"""

import json
import os
import sys

# Thresholds (in bytes)
WARN_SIZE = 100_000  # 100KB - warn and suggest chunking
BLOCK_SIZE = 500_000  # 500KB - block and require explicit handling

# Estimated tokens per byte (rough: 1 token ≈ 4 chars)
BYTES_PER_TOKEN = 4
MAX_READ_TOKENS = 25_000  # Claude Code's hardcoded limit


def get_file_size(path: str) -> int | None:
    """Get file size, return None if file doesn't exist."""
    try:
        # Handle Windows paths
        path = path.replace("/", os.sep).replace("\\", os.sep)
        if path.startswith("~"):
            path = os.path.expanduser(path)
        return os.path.getsize(path)
    except (OSError, FileNotFoundError):
        return None


def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    if tool_name != "Read":
        sys.exit(0)

    file_path = tool_input.get("file_path", "")
    offset = tool_input.get("offset")
    limit = tool_input.get("limit")

    # Skip if already using chunked reading
    if offset is not None or limit is not None:
        sys.exit(0)

    # Skip PDFs (handled by pdf-blocker.py)
    if file_path.lower().endswith(".pdf"):
        sys.exit(0)

    # Skip images (handled differently)
    if any(
        file_path.lower().endswith(ext)
        for ext in [".png", ".jpg", ".jpeg", ".gif", ".webp"]
    ):
        sys.exit(0)

    size = get_file_size(file_path)
    if size is None:
        sys.exit(0)  # File doesn't exist, let Read handle the error

    estimated_tokens = size // BYTES_PER_TOKEN

    # Block very large files
    if size > BLOCK_SIZE or estimated_tokens > MAX_READ_TOKENS:
        output = {
            "continue": False,
            "stopReason": f"BLOCKED: File too large for single read ({size:,} bytes, ~{estimated_tokens:,} tokens).\n\n"
            f"Options:\n"
            f"1. Use chunked reading: Read with offset=0, limit=500 (then continue)\n"
            f"2. Use Grep to search for specific content\n"
            f"3. Delegate to a subagent (Task tool) for fresh context\n\n"
            f"Claude Code limit: {MAX_READ_TOKENS:,} tokens per Read call.",
        }
        print(json.dumps(output))
        sys.exit(0)

    # Warn for medium-large files (feedback to Claude, doesn't block)
    if size > WARN_SIZE:
        # Send warning to stderr (shown to Claude as feedback)
        print(
            f"WARNING: Large file ({size:,} bytes, ~{estimated_tokens:,} tokens). "
            f"Consider using offset/limit params or delegating to subagent if context is limited.",
            file=sys.stderr,
        )

    sys.exit(0)


if __name__ == "__main__":
    main()
