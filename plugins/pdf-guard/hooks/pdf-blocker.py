#!/usr/bin/env python3
"""
PreToolUse hook to block direct PDF reads.
Forces Claude to use extraction scripts instead of Read tool on PDFs.
"""

import json
import sys


def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)  # Allow if can't parse

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    # Only check Read tool
    if tool_name != "Read":
        sys.exit(0)

    file_path = tool_input.get("file_path", "")

    # Block PDF reads
    if file_path.lower().endswith(".pdf"):
        # Output JSON to block the call and provide feedback
        output = {
            "continue": False,
            "stopReason": f"BLOCKED: Direct PDF read not allowed. Use extraction script instead:\n\n"
            f'  python ~/.claude/scripts/pdf_extract.py "{file_path}"\n\n'
            f"Or for unified (text + image refs):\n\n"
            f'  python ~/.claude/scripts/pdf_extract_unified.py "{file_path}"\n\n'
            f"Then read the extracted .txt or _unified.md file.",
        }
        print(json.dumps(output))
        sys.exit(0)

    # Allow all other reads
    sys.exit(0)


if __name__ == "__main__":
    main()
