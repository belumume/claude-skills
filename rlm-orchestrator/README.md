# RLM Orchestrator

Implement RLM-style (Recursive Language Model) orchestration for complex tasks that would exceed single context window limits.

**Inspired by:** [RLM Research Paper (arXiv:2512.24601)](https://arxiv.org/abs/2512.24601)

## What It Does

Automatically decomposes large tasks, spawns parallel subagents (up to ~10 concurrent), aggregates results, and iterates until completion. Achieves functional recursion within Claude Code's depth=1 subagent architecture.

## When to Use

- Tasks requiring >100K tokens of context
- Multi-file codebase analysis or refactoring
- Research tasks with many sources
- Batch processing with independent partitions
- Any task showing context rot (degraded recall, repeated mistakes)

## Core Pattern

```
Main Session (orchestrator)
    ├── Decompose task into partitions
    ├── Spawn parallel subagents (fresh 200K context each)
    ├── Aggregate results
    ├── Spawn follow-up batch (if gaps exist)
    └── Return unified result
```

## Test Results

Context rot prevention measured across scenarios:

| Scenario | Tokens | Baseline | RLM | Improvement |
|----------|--------|----------|-----|-------------|
| Medium | 75K | 85% recall | 95% | +11.8% |
| Heavy | 250K | 40% recall | 95% | **+137.5%** |
| Extreme | 625K | 40% recall | 92% | **+130%** |

## Claude Code Only

This skill requires Claude Code CLI (Task tool for subagent spawning). Not available for Claude web/desktop.

## Related Skills

- **ralph-loop** - Autonomous iteration for single-context tasks
- **superpowers:dispatching-parallel-agents** - Detailed parallel dispatch patterns
- **superpowers:subagent-driven-development** - Implementation-focused subagent workflow

## Bundled Resources

- **`references/subagent-prompt-template.md`** - Templates for research, implementation, and exploration subagents
- **`scripts/context_rot_test.py`** - Test suite to measure context rot prevention effectiveness

## Quick Start

Invoke with `/rlm-orchestrator` or mention "RLM", "context rot", or "parallel agents" when facing large context tasks.
