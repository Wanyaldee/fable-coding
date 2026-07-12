# 0008: Allow reading .env template files through the deny hook

(日本語: [0008-env-template-read-exception.ja.md](../ja/0008-env-template-read-exception.ja.md))

## Context

ADR 0001's deny hook blocks `.env` and `.env.*` wholesale, which also blocks `.env.example` and friends — files that by convention hold only the *names* of required secrets, never their values. In practice this hurt: Claude could not tell which secrets a project needs, so it guessed at configuration instead of reading the template. The same over-blocking existed a second time in the user's `~/.claude/settings.json` as a `Read(**/.env.*)` deny rule; since deny rules always beat allow rules, no settings-side allow could carve out an exception — the rule itself had to go.

## Decision

Add an early exit in `hooks/deny-secrets.py`: if the basename starts with `.env` **and** ends with `.example`, `.sample`, or `.template`, allow the read before the deny list is consulted. The exception is scoped to `.env`-prefixed names so template-looking files in otherwise-denied locations (e.g. `~/.aws/credentials.sample`) stay blocked. On the settings side, the redundant `Read(**/.env.*)` deny rule was removed from the user's `~/.claude/settings.json`, keeping `Read(**/.env)` as a fail-safe that still covers the plain `.env` file (including via Bash) if hooks are ever disabled. Version bumped to 2.1.0.

## Alternatives rejected

- **A second user-level hook (`~/.claude/hooks/deny-env-read.py`) layered on top** — built first during diagnosis, then deleted: two hooks enforcing one policy drift apart, and the plugin hook is the copy that travels with the plugin.
- **Enumerating secret-bearing variants in the deny list (`.env.local`, `.env.production`, …) instead of an exception** — enumeration fails open for any unlisted variant (`.env.ci`, `.env.docker`); default-deny with a narrow template exception fails closed.
- **Allowing any `*.example`/`*.sample`/`*.template` basename** — would punch through the `/.aws/` and `*.pem` protections for files like `credentials.sample`; the `.env` prefix guard keeps the exception surgical.

## Consequences

- Claude can read `.env.example` / `.env.sample` / `.env.template` (including chained forms like `.env.local.sample`) and learn which keys a project needs; all value-bearing `.env` variants stay blocked. Verified by piping synthetic hook input for eight paths and by live Read calls (`.env.example` allowed, `.env.local` denied).
- A project that puts real secrets in a file named like a template (e.g. committed `.env.example` with live values) is no longer protected — that file is already leaking via git, so the hook is not its last line of defense.
- ADR 0001's consequence "`.env.example` / `.env.sample` are also blocked; accepted as the safe side" is superseded by this ADR.
- The ceiling from ADR 0001 is unchanged: the hook covers only the Read tool; Bash reads of non-plain-`.env` variants rely on the hook, not settings, since `Read(**/.env.*)` was removed.
