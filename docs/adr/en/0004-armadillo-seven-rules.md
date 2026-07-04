# 0004: Fold @armadillo_ai's seven agent-discipline rules into the coding skill

(日本語: [0004-armadillo-seven-rules.ja.md](../ja/0004-armadillo-seven-rules.ja.md))

## Context

The user supplied a set of seven agent-discipline rules from an X post
(`x.com/armadillo_ai/status/2072909284992786535`) and asked for them to be
incorporated, noting probable overlap with their own philosophy: (1) define
"done" mechanically before starting, (2) don't silently pick one reading of an
ambiguous instruction, (3) no drive-by improvements, (4) report "verified"
with evidence, not "works", (5) at most two fix attempts per error, (6)
fresh-eyes self-review before completion, (7) confidence levels and
three-point progress reports.

## Decision

Folded into `skills/fable-coding/SKILL.md` (v1.5.0) at the sections where each
rule belongs, rather than as a separate block: rules 1–2 into §0 (plan), rule 5
into §2 (diagnosis), rule 3 into §3 (minimal change), rules 4 and 6 into §5
(verification), rule 7 into §7 (response style); four new anti-patterns. The
JA translation follows.

Two rules needed reconciliation with existing content:

- **Rule 2 vs "pick one and proceed" (§9).** Not a conflict once split by
  level: ambiguity in *what the user wants* (readings that change the
  deliverable) → enumerate + recommend + confirm; ties in *how to build it* →
  pick one and go. Both bullets now cross-reference each other.
- **Rule 7's "ask when confidence is medium/low" vs "gather it, don't ask"
  (§9).** Narrowed to uncertainty only the user can resolve; everything
  gatherable stays gather-first. Confidence labels themselves apply
  unconditionally.

Rules 3 and 4 substantially overlapped existing §3/§5 text; they were merged
as sharpenings (proposals-not-implementations for adjacent improvements;
evidence-in-the-report, skip-reasons) rather than duplicated.

## Alternatives rejected

- **A separate skill** — wrong scope: all seven rules fire on ordinary coding
  tasks, exactly where `fable-coding` already triggers.
- **Verbatim block quoting the post** — the rules restate or sharpen existing
  sections; a parallel block would create two competing sources of truth in
  one skill.

## Consequences

- The skill now has an explicit definition-of-done gate, a two-strike rule on
  repeated fixes, and a mandated skeptical self-review — the main genuinely
  new mechanics.
- Aligned with the user's dev-philosophy (human-in-the-loop: interpretation
  confirmation and confidence-gated asks are concretizations of it).
- Ceiling: the two-strike rule counts "same error" informally; the model
  judges sameness. Source is a snapshot of a third-party post; provenance
  recorded here.
