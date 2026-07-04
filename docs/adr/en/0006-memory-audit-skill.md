# 0006: /memory-audit command skill, report-only with a mechanical --fix

(日本語: [0006-memory-audit-skill.ja.md](../ja/0006-memory-audit-skill.ja.md))

## Context

ADR 0005 codified memory-writing rules but left detection manual: the
2026-07-04 audit that motivated it was done by hand (enumerate dirs, diff
index vs files, resolve `originSessionId` → model via session transcripts,
verify claims against current state). The user wants it repeatable
(improvement proposal 3 of that audit).

## Decision

New skill `skills/memory-audit/SKILL.md` (v1.7.0, en + ja companion): a
procedure skill that replays the manual audit — enumerate, index diff,
attribution resolution, per-file checks in severity order (contradicted >
repo-duplication > unindexed > mixed volatility > format), grouped report.
Report-only by default. `--fix` applies exactly four mechanical repairs
(add/remove index lines, backfill `origin:`, absolutize dates) and never
touches memory body content; deletions, pointer-shrinking, and file splits
are always listed for the user instead. The skill embeds the two
operational gotchas the manual audit hit: project dir names start with `-`
(glob/ls option injection) and transcripts get purged (resolve provenance
while possible).

## Alternatives rejected

- **Folding the procedure into `memory-discipline`** — wrong trigger: that
  skill fires while writing memories; the audit is an explicitly invoked
  one-shot. Merging would bloat every memory-write with audit steps.
- **A standalone script (`hooks/`-style Python)** — half the checks are
  judgment (is this a spec dump? is this claim contradicted?); a script
  covers only index/frontmatter and would give false confidence. The
  mechanical subset stays as inline greps the model runs.
- **Auto-fix by default** — deleting or rewriting memories on pattern-match
  contradicts the user's human-in-the-loop philosophy; stale-looking can be
  intentional.

## Consequences

- The audit becomes a command; pairing it with `memory-discipline` closes
  the loop (rules at write time, detection on demand).
- Report-only default means findings recur until acted on; that is the
  intended pressure, not a bug.
- Ceiling: repo-duplication and staleness checks are only as good as what
  the model can cheaply verify in-session; a periodic scheduled run is
  possible later via the schedule skill if wanted.
