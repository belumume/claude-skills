#!/usr/bin/env python3
"""
Enhanced Context Tracker with RLM-Aware Guidance.

Tracks cumulative file reads across a session and provides intelligent
recommendations for subagent delegation based on RLM (Recursive Language Model)
orchestration patterns.

Features:
- Cumulative token tracking per session
- Smart delegation suggestions based on file patterns
- RLM strategy recommendations (partition, grep, peek)
- Structured output for Claude to act on
"""

import json
import os
import sys
from pathlib import Path
from collections import defaultdict

# Thresholds (estimated tokens)
SUGGEST_DELEGATION = 75_000  # Suggest delegation at 75K tokens
WARN_CUMULATIVE = 100_000  # Warn at ~100K tokens read
BLOCK_CUMULATIVE = 150_000  # Block at ~150K tokens (leave room for conversation)

# State file (per session)
STATE_DIR = Path.home() / ".claude" / "state"
BYTES_PER_TOKEN = 4

# File type categories for intelligent partitioning
FILE_CATEGORIES = {
    "code": [
        ".py",
        ".js",
        ".ts",
        ".tsx",
        ".jsx",
        ".rb",
        ".go",
        ".rs",
        ".java",
        ".c",
        ".cpp",
        ".h",
    ],
    "config": [".json", ".yaml", ".yml", ".toml", ".ini", ".env", ".xml"],
    "docs": [".md", ".rst", ".txt", ".doc", ".docx"],
    "data": [".csv", ".sql", ".parquet"],
    "test": ["test_", "_test.", ".test.", "spec_", "_spec."],
}


def categorize_file(filepath: str) -> str:
    """Categorize a file by its type/purpose."""
    lower_path = filepath.lower()
    basename = os.path.basename(lower_path)

    # Check for test files first (by name pattern)
    for pattern in FILE_CATEGORIES["test"]:
        if pattern in basename:
            return "test"

    # Check by extension
    for category, extensions in FILE_CATEGORIES.items():
        if category == "test":
            continue
        for ext in extensions:
            if lower_path.endswith(ext):
                return category

    return "other"


def get_session_id() -> str:
    """Get current session ID from hook input."""
    try:
        data = json.loads(os.environ.get("CLAUDE_HOOK_DATA", "{}"))
        return data.get("session_id", "unknown")
    except Exception:
        return "unknown"


def is_subagent(data: dict) -> bool:
    """Detect if running inside a subagent context.

    Subagents have fresh 200K context and should NOT inherit parent's token count.
    Detection methods:
    1. CLAUDE_SUBAGENT env var (user can set to bypass)
    2. CLAUDE_SKIP_CONTEXT_TRACKING env var (explicit bypass)
    3. Check hook data for subagent indicators
    """
    # Method 1: Explicit env var bypass
    if os.environ.get("CLAUDE_SUBAGENT"):
        return True
    if os.environ.get("CLAUDE_SKIP_CONTEXT_TRACKING"):
        return True

    # Method 2: Check hook data for subagent indicators
    # Subagents may have specific metadata or different session patterns
    if data.get("is_subagent"):
        return True

    # Method 3: Check if session_id indicates a subagent (heuristic)
    # Main sessions typically have UUID format; subagents might differ
    session_id = data.get("session_id", "")
    if session_id.startswith("subagent-") or session_id.startswith("task-"):
        return True

    return False


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
    return {
        "total_bytes": 0,
        "read_count": 0,
        "files": [],
        "categories": defaultdict(int),
        "directories": defaultdict(int),
    }


def save_state(session_id: str, state: dict):
    """Save read tracking state."""
    state_file = get_state_file(session_id)
    # Convert defaultdicts to regular dicts for JSON serialization
    state_copy = state.copy()
    if isinstance(state_copy.get("categories"), defaultdict):
        state_copy["categories"] = dict(state_copy["categories"])
    if isinstance(state_copy.get("directories"), defaultdict):
        state_copy["directories"] = dict(state_copy["directories"])
    state_file.write_text(json.dumps(state_copy, indent=2))


def get_file_size(path: str) -> int | None:
    """Get file size."""
    try:
        path = os.path.expanduser(path)
        return os.path.getsize(path)
    except Exception:
        return None


def suggest_rlm_strategy(state: dict, new_file: str) -> dict:
    """Generate RLM-aware delegation suggestions based on file patterns."""
    categories = state.get("categories", {})
    directories = state.get("directories", {})

    suggestions = {
        "strategy": None,
        "rationale": None,
        "subagent_type": None,
        "partition_hint": None,
    }

    # Analyze what we've been reading
    total_files = state.get("read_count", 0)

    # If reading many files from same directory, suggest partition by directory
    if directories:
        max_dir = max(directories.items(), key=lambda x: x[1])
        if max_dir[1] >= 5:
            suggestions["strategy"] = "partition-by-directory"
            suggestions["rationale"] = (
                f"Reading many files from {max_dir[0]} ({max_dir[1]} files)"
            )
            suggestions["subagent_type"] = "Explore"
            suggestions["partition_hint"] = (
                f"Consider spawning subagent for {max_dir[0]}/* analysis"
            )

    # If reading many of same type, suggest partition by type
    if categories:
        max_cat = max(categories.items(), key=lambda x: x[1])
        if max_cat[1] >= 5 and not suggestions["strategy"]:
            suggestions["strategy"] = "partition-by-type"
            suggestions["rationale"] = (
                f"Reading many {max_cat[0]} files ({max_cat[1]} files)"
            )
            suggestions["subagent_type"] = (
                "Explore" if max_cat[0] in ["docs", "config"] else "general-purpose"
            )
            suggestions["partition_hint"] = (
                f"Consider spawning subagent for all {max_cat[0]} files"
            )

    # If we've read a lot already, suggest grep-first strategy
    if total_files >= 10 and not suggestions["strategy"]:
        suggestions["strategy"] = "grep-first"
        suggestions["rationale"] = (
            f"Already read {total_files} files - use Grep to filter before more reads"
        )
        suggestions["subagent_type"] = "Explore"
        suggestions["partition_hint"] = "Use Grep to find relevant files before reading"

    return suggestions


def generate_delegation_guidance(
    state: dict, estimated_tokens: int, new_file: str
) -> str:
    """Generate actionable RLM-style delegation guidance."""
    rlm_suggestions = suggest_rlm_strategy(state, new_file)

    guidance = []
    guidance.append("## RLM Orchestration Recommended")
    guidance.append("")
    guidance.append(
        f"**Context status:** ~{estimated_tokens:,} tokens consumed ({state['read_count']} files)"
    )
    guidance.append("")

    if rlm_suggestions["strategy"]:
        guidance.append(f"**Suggested strategy:** {rlm_suggestions['strategy']}")
        guidance.append(f"**Rationale:** {rlm_suggestions['rationale']}")
        guidance.append(f"**Subagent type:** {rlm_suggestions['subagent_type']}")
        guidance.append(f"**Partition hint:** {rlm_suggestions['partition_hint']}")
        guidance.append("")

    guidance.append("### Recommended Actions")
    guidance.append("")
    guidance.append(
        "1. **Use `/rlm-orchestrator` skill** for automatic task decomposition"
    )
    guidance.append("2. **Spawn Explore subagent** for remaining file analysis:")
    guidance.append("   ```")
    guidance.append(
        '   Task(subagent_type="Explore", description="Analyze [scope]", prompt="...")'
    )
    guidance.append("   ```")
    guidance.append("3. **Or use Grep-first strategy** to filter before reading:")
    guidance.append("   ```")
    guidance.append(
        '   Grep(pattern="[relevant term]", output_mode="files_with_matches")'
    )
    guidance.append("   ```")
    guidance.append("")
    guidance.append("### File Distribution")

    categories = state.get("categories", {})
    if categories:
        for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
            guidance.append(f"- {cat}: {count} files")

    return "\n".join(guidance)


def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = data.get("tool_name", "")
    if tool_name != "Read":
        sys.exit(0)

    # Subagents have fresh 200K context - don't apply parent's token limits
    if is_subagent(data):
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

    # Convert categories/directories back to defaultdict if needed
    if not isinstance(state.get("categories"), defaultdict):
        state["categories"] = defaultdict(int, state.get("categories", {}))
    if not isinstance(state.get("directories"), defaultdict):
        state["directories"] = defaultdict(int, state.get("directories", {}))

    current_total = state["total_bytes"]
    new_total = current_total + size
    estimated_tokens = new_total // BYTES_PER_TOKEN

    # Track file category and directory
    category = categorize_file(file_path)
    directory = os.path.dirname(file_path)
    state["categories"][category] += 1
    state["directories"][directory] += 1

    # At extreme limits, warn strongly but don't block (blocking breaks subagents)
    # Set CLAUDE_BLOCK_AT_LIMIT=1 to enable hard blocking if desired
    if estimated_tokens > BLOCK_CUMULATIVE:
        guidance = generate_delegation_guidance(state, estimated_tokens, file_path)
        if os.environ.get("CLAUDE_BLOCK_AT_LIMIT"):
            output = {
                "continue": False,
                "stopReason": f"BLOCKED: Context limit reached.\n\n{guidance}\n\n"
                f"This file ({size:,} bytes) would push total to {new_total:,} bytes ({estimated_tokens:,} tokens).\n\n"
                f"**Delegate remaining work to a subagent for fresh context.**",
            }
            print(json.dumps(output))
            sys.exit(0)
        else:
            # Warn strongly but allow (prevents breaking subagents)
            print(
                f"🚨 CRITICAL: Context at {estimated_tokens:,} tokens (>{BLOCK_CUMULATIVE:,} limit)\n\n{guidance}",
                file=sys.stderr,
            )
            # Continue to update state and allow the read

    # Warn at warning threshold
    if estimated_tokens > WARN_CUMULATIVE:
        guidance = generate_delegation_guidance(state, estimated_tokens, file_path)
        print(
            f"⚠️  HIGH CONTEXT USAGE\n\n{guidance}",
            file=sys.stderr,
        )
    # Suggest delegation at lower threshold (informational)
    elif estimated_tokens > SUGGEST_DELEGATION:
        rlm_suggestions = suggest_rlm_strategy(state, file_path)
        if rlm_suggestions["strategy"]:
            print(
                f"💡 Context at {estimated_tokens:,} tokens. "
                f"Consider {rlm_suggestions['strategy']}: {rlm_suggestions['partition_hint']}",
                file=sys.stderr,
            )

    # Update state
    state["total_bytes"] = new_total
    state["read_count"] += 1
    state["files"].append({"path": file_path, "size": size, "category": category})
    save_state(session_id, state)

    sys.exit(0)


if __name__ == "__main__":
    main()
