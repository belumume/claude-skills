# Subagent Prompt Template

Use this template when spawning subagents for RLM orchestration.

## Standard Research Subagent

```markdown
# Task: [Specific partition description]

## Context
You are partition [X] of [N] in an RLM orchestration.
Other partitions are handling: [brief list of other scopes]
Your scope is strictly: [detailed scope definition]

## Objective
[Clear statement of what to find/analyze/produce]

## Strategy
[Choose appropriate RLM strategy]

### If using Peeking:
1. First, sample structure by reading first 50 lines of relevant files
2. Identify patterns and organization
3. Then conduct targeted deep analysis

### If using Grepping:
1. Use Grep to filter: `pattern="[relevant keywords]"`
2. Read only files with matches
3. This reduces unnecessary context consumption

### If using Partition+Map:
1. You handle only: [specific files/sections]
2. Do NOT read files outside your partition
3. Trust that other partitions cover their scope

## Output Format
Return a structured summary:

```json
{
  "partition": "[X]",
  "findings": [
    {
      "item": "[finding description]",
      "location": "file:line",
      "confidence": "high|medium|low",
      "evidence": "[brief quote or reference]"
    }
  ],
  "gaps": ["[anything you couldn't determine]"],
  "cross_references": ["[things other partitions should check]"]
}
```

## Constraints
- Stay within your partition scope
- Return summary, not raw data
- Flag uncertainties explicitly
- Do NOT attempt to synthesize across partitions (orchestrator does this)
```

## Implementation Subagent

```markdown
# Task: [Implementation partition description]

## Context
You are implementing partition [X] of [N].
Other partitions are handling: [list]
Your scope: [specific files to modify]

## Objective
[What to implement/modify/fix]

## Instructions
1. Read the relevant files in your partition
2. Implement the changes following project conventions
3. Write tests if applicable
4. Commit your changes with descriptive message

## Constraints
- Only modify files in your partition: [file list]
- Do NOT modify shared files (orchestrator coordinates those)
- Follow existing code patterns
- If blocked, return what you accomplished and what's blocking

## Output Format
```json
{
  "partition": "[X]",
  "completed": ["[list of completed items]"],
  "files_modified": ["[file paths]"],
  "tests_added": ["[test descriptions]"],
  "blocked": ["[any blockers]"],
  "notes": "[anything the orchestrator should know]"
}
```
```

## Exploration Subagent

```markdown
# Task: Explore [topic/area]

## Context
RLM orchestration exploring: [overall topic]
Your exploration focus: [specific subtopic]

## Objective
Find and summarize information about [specific focus].

## Approach
1. Use Glob to find relevant files: `pattern="[appropriate glob]"`
2. Use Grep to search for: `pattern="[relevant terms]"`
3. Read the most relevant matches
4. Synthesize findings

## Output Format
```json
{
  "topic": "[your focus]",
  "summary": "[2-3 sentence summary]",
  "key_files": ["[most relevant files]"],
  "insights": ["[important discoveries]"],
  "related_topics": ["[things to explore further]"]
}
```

## Constraints
- Focus only on your assigned topic
- Return insights, not file contents
- Flag if topic needs deeper investigation
```

## Aggregator Subagent (for complex merges)

```markdown
# Task: Aggregate partition results

## Context
You are aggregating results from [N] partitions of an RLM orchestration.

## Partition Results
[Include summaries from all completed partitions]

## Objective
Synthesize a unified result that:
1. Combines all partition findings
2. Removes duplicates
3. Resolves conflicts (or flags for human review)
4. Identifies gaps in coverage

## Output Format
```json
{
  "unified_findings": ["[combined, deduplicated list]"],
  "conflicts": [
    {
      "item": "[conflicting finding]",
      "partition_a_says": "[version A]",
      "partition_b_says": "[version B]",
      "recommendation": "[which to trust and why]"
    }
  ],
  "coverage_gaps": ["[areas not covered by any partition]"],
  "confidence": "high|medium|low",
  "summary": "[executive summary paragraph]"
}
```
```

## Tips for Effective Subagent Prompts

1. **Be specific about scope** - Ambiguous boundaries cause overlap or gaps
2. **Specify output format** - Structured output is easier to aggregate
3. **Include constraints** - What should the subagent NOT do
4. **Explain context** - Subagent doesn't see main conversation
5. **Request confidence levels** - Helps with aggregation decisions
6. **Ask for cross-references** - Helps identify dependencies
