---
name: memory-discipline
description: Rules for writing and maintaining persistent auto-memory (memory/*.md + MEMORY.md index). Use when saving a lesson, preference, decision, or project fact to memory, when updating or reorganizing existing memories, or when a recalled memory contradicts the current state of the code or environment.
---

# Memory discipline

Memory is only useful if a future session can trust it. Every rule here exists
because its violation was observed in a real memory audit (2026-07-04): spec
dumps that duplicated the repo, files missing from the index, and a memory
that became false the same day it was written.

## What goes in (and what doesn't)

- One fact per file. A file that mixes durable setup facts with volatile
  status will rot partially; split them. Volatile state (progress, current
  decisions under review) gets its own file that is *expected* to be
  rewritten.
- Never save what the repo, git history, CLAUDE.md, or chat history already
  records. A spec, architecture, or plan that lives in `docs/` gets a pointer
  and the non-obvious delta, not a copy.
- Do save: user corrections and confirmed approaches (with why), project
  facts not derivable from the code, pointers to external resources, and
  open questions **with their owner** ("pending: Okada-san confirming X") —
  an unresolved point recorded with who resolves it is a first-class fact.

## Format

```markdown
---
name: <kebab-case-slug>
description: <one line — this is what recall matching runs on>
metadata:
  type: user | feedback | project | reference
  origin: <model-id>, <YYYY-MM-DD>
---

<the fact>

**Why:** <why it matters / where it came from>
**How to apply:** <what to do differently>
```

- `origin` carries the model and an absolute date directly: session IDs rot
  when transcripts are purged; frontmatter doesn't.
- Absolute dates only, everywhere. "Last week" is meaningless in three weeks.
- Link related memories with `[[name]]`. A link to a not-yet-written memory
  marks something worth writing, not an error.
- Why / How to apply are required for `feedback` and `project` types.

## The index

- `MEMORY.md` gets its one-line entry (`- [Title](file.md) — hook`) **in the
  same turn** the memory file is written. An unindexed memory is never
  recalled — it might as well not exist.
- One line per memory, never content. The hook after the dash is what earns
  the file a read: write it as the reason to open the file.

## Maintenance — the same-session rule

- A memory contradicted by what you just observed gets updated or deleted
  **in that session, the turn you notice** — not flagged for later. Stale
  memory is worse than no memory: it is trusted and wrong.
- Update the existing file rather than writing a near-duplicate; append a
  dated correction if the history matters, rewrite if it doesn't.
- Wrong memory → delete the file and its index line. Superseded plan →
  delete or shrink to a pointer at the superseding document.
- Before saving, check the index for an existing file that covers the topic.
