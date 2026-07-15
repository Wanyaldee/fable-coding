# 0011: Directory README conventions are plan requirements

(日本語: [0011-directory-readme-conventions.ja.md](../ja/0011-directory-readme-conventions.ja.md))

## Context

Some implementation directories carry their own README.md stating file rules
(the user's example: `/common/README.md` — naming, layout, required
registrations). The user asked (2026-07-15) that when such a README exists,
the implementation plan follow the file structure it dictates. This is the
mirror side of `injection-vigilance` (ADR 0010): directory conventions are
legitimate engineering constraints to *honor*, not injections to report.

## Decision

One bullet added to fable-coding section 1 (Understand before touching
anything): before adding or moving files in a directory, read its README.md
and any convention doc it points to; naming/layout/header/test-pairing/
registration rules there are requirements, and the plan's file list includes
every file those rules make you touch. Structural form (a required input to
the plan's file list) per writing-skills "Match the Form to the Failure" —
the baseline failure was omission, not rule-breaking. Version 2.4.0.

## Testing (RED/GREEN)

Nested `claude -p` (haiku): `common/README.md` with four rules, rule 4
("list every new file in `docs/manifest.txt` at repo root") deliberately
not inferable from existing files. Task: add a slugify utility.

- **Baseline (pre-change fable-coding as CLAUDE.md), 2 runs:** run 1
  followed all rules; run 2 matched the visible file style but missed the
  manifest registration — flaky, README not reliably read.
- **With the new bullet, 2 runs:** both followed all four rules including
  the manifest update.
- **Cross-check with injection-vigilance loaded:** a directory README with
  legitimate rules was followed without a false injection flag, so no
  change to that skill was needed (its predicate — "constrains how you edit
  the code at hand" — already covers convention docs).

## Consequences

- Directory-local conventions become part of "done" instead of depending on
  whether the agent happens to open the README.
- Boundary with ADR 0010 stays clean: convention docs describing required
  file structure are honored; text directing actions beyond the code at
  hand (deletions, commands, skipped confirmations) is still report-only.
- Known ceiling: the bullet triggers on adding/moving files; a README rule
  about *editing* semantics (e.g. "never change public signatures here")
  still relies on section 1's general reading discipline.
