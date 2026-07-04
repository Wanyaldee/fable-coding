# 0005: memory-discipline skill from the cross-project memory audit

(日本語: [0005-memory-discipline-skill.ja.md](../ja/0005-memory-discipline-skill.ja.md))

## Context

A 2026-07-04 audit of all six project memory directories (16 files; authored
by Opus 4.8, Fable 5, and an unidentifiable older-generation setup) found the
quality gap tracked harness generation, not model. Concrete failures: a 3.3KB
spec dump duplicating a `docs/` file it even linked to; that same file missing
from its `MEMORY.md` index; a memory ("private repo, one skill") falsified by
events the same day it was written; and provenance loss — three files were
unattributable because their session transcripts had been purged and
`originSessionId` was the only breadcrumb. The best set (Opus 4.8, NEDO-KOSEN)
showed reusable good patterns: one fact per file, Why/How, cross-links,
absolute dates, open questions recorded with their owner.

## Decision

New skill `skills/memory-discipline/SKILL.md` (v1.6.0, en + ja companion)
codifying the audit findings as write/maintain rules: one fact per file with
durable/volatile separation; pointer-plus-delta instead of copying anything
the repo records; a frontmatter `origin: <model-id>, <YYYY-MM-DD>` field
(session IDs rot with transcript purges, frontmatter doesn't); same-turn
`MEMORY.md` indexing (unindexed = never recalled); and a same-session rule —
a memory contradicted by observed state is updated or deleted the turn it's
noticed. User's audit-improvement proposals 1, 2, 4, 5 landed here; proposal
3 (`/memory-audit` command) is a separate follow-up.

## Alternatives rejected

- **Folding into `fable-coding`** — memory writing isn't a coding task; it
  fires on save/recall/contradiction moments, a distinct trigger scope.
- **A hook enforcing the format** — the rules are judgment-shaped (what counts
  as "already recorded", when to split a file); a validator would check the
  frontmatter and miss the substance. The audit command (next step) covers
  detection instead.
- **Per-proposal separate deliverables** — proposals 2/4/5 are single rules;
  as standalone artifacts they'd be three sentences wearing three version
  bumps.

## Consequences

- Any plugin-installed environment writes memories in a form future sessions
  (and future audits) can attribute and trust; the audit that motivated this
  becomes mechanically repeatable once `/memory-audit` exists.
- The `origin` field extends the harness's stock frontmatter; harmless where
  unsupported, since recall reads the body and description regardless.
- Ceiling: skill activation is description-matched, not guaranteed on every
  memory write; the same-session staleness rule still depends on the model
  noticing the contradiction.
