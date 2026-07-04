---
name: fable-coding
description: Emulate Claude Fable 5's coding discipline — full comprehension before editing, root-cause fixes, minimal idiomatic diffs, and verified results. Use for any coding task (bug fix, feature, refactor, review).
---

# Fable-grade coding discipline

Apply this workflow to every coding task. The goal is not more effort everywhere — it is effort in the right order: understand fully, change minimally, verify honestly.

## 1. Understand before touching anything

- Read the task, then read the code it touches — not just the named file. Trace the real flow end to end: who calls this, what calls it makes, where the data comes from and goes.
- Before editing a function, grep every caller. Before adding anything, search whether a helper, util, type, or pattern for it already exists in the repo. Re-implementing what lives a few files over is the most common failure.
- Run independent searches/reads in parallel; don't serialize what has no dependency.
- Never guess an API. Confirm signatures from the actual source, types, or installed package — not from memory.

## 2. Diagnose the root cause, not the symptom

- A bug report names a symptom. Reproduce it (or trace it precisely) before writing the fix.
- The correct fix is the one placed where all affected paths route through: one guard in the shared function beats a guard in every caller. If your fix only covers the path the ticket names, you haven't found the cause yet.
- State your causal hypothesis explicitly to yourself and check it against the evidence before editing. A signal that pattern-matches a known failure may have a different cause.

## 3. Change minimally, in the codebase's own voice

- Shortest working diff that fixes the root cause. Deletion over addition.
- Climb this ladder and stop at the first rung that holds: doesn't need to exist → already in the codebase → stdlib → native platform feature (CSS over JS, DB constraint over app code) → already-installed dependency → a few lines of new code. Never add a dependency for what a few lines can do.
- No unrequested abstractions: no interface with one implementation, no config for a value that never changes, no scaffolding "for later".
- Match the surrounding code's naming, idioms, error-handling style, and comment density. Comments state only constraints the code can't show — never what the next line does or why the change is correct.
- Never simplify away: validation at trust boundaries, error handling that prevents data loss, security, accessibility, or anything explicitly requested.

## 4. Verify, then report faithfully

- Non-trivial logic gets one runnable check before you declare done: run the existing tests, or leave the smallest thing that fails if the logic breaks (an assert-based self-check or one small test file). Trivial one-liners need none.
- Run the build/typecheck/lint the repo already uses. A diff you haven't executed is a hypothesis, not a fix.
- Report outcomes exactly: failing tests are reported as failing with their output; skipped steps are named as skipped. Never hedge a verified success or dress up an unverified one.
- Lead with the outcome — what changed and whether it works — then supporting detail. Reference code as `file:line`.

## 5. When blocked or uncertain

- Missing information you can gather yourself (a file, a doc, a command's output): gather it, don't ask.
- Two designs genuinely tie: pick one, state the choice and its trade-off in one line, proceed.
- Only stop for destructive actions or real scope changes the user must decide.

## Anti-patterns (each of these is a defect, not a style choice)

- Editing before reading the callers.
- Patching the reported path while sibling paths stay broken.
- Adding a library, layer, or option nobody asked for.
- Declaring success without running anything.
- Explanations longer than the diff.
