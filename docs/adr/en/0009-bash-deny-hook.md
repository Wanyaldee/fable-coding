# 0009: Deny dangerous Bash commands (secret reads, rm -rf, direct DB access)

(日本語: [0009-bash-deny-hook.ja.md](../ja/0009-bash-deny-hook.ja.md))

## Context

ADR 0001 deliberately scoped the deny hook to the Read tool and left Bash coverage to settings-level `permissions.deny` rules. The user now wants the Bash side closed by the plugin itself — `cat .env`-style secret reads, catastrophic commands like `rm -rf`, and direct database manipulation — so the protection travels with the plugin and enforces fable-coding section 4 (DB operations are reported to the user, not executed) by mechanism rather than by skill text.

## Decision

Add `hooks/deny-bash.py` as a second `PreToolUse` hook (matcher `Bash`) in `hooks/hooks.json`. It denies, in order:

1. **`.env` references** — any `.env`/`.env.*` token in the command text, except template suffixes `.example`/`.sample`/`.template` (same policy as ADR 0008).
2. **Destructive commands** — `rm` with both recursive and force flags (short, long, combined, `sudo`-prefixed, and via `xargs`/`find -exec`), any `mkfs*`, and `dd` writing to `of=/dev/*`.
3. **Direct DB access** — `mysql`, `mariadb`, `psql`, `sqlite3`, `mongosh`, `mongo`, `redis-cli` at a pipeline-segment start, plus `wrangler d1 execute` / `wrangler d1 migrations apply`. The deny reason instructs Claude to report the exact statement to the user for execution (fable-coding section 4).

Deny beats ask here because write-vs-read cannot be reliably parsed out of a shell string; the user runs approved commands themselves (e.g. via the `!` prefix). Version bumped to 2.2.0.

## Alternatives rejected

- **`permissionDecision: "ask"` for DB commands** — would allow SELECT debugging with one click, but the user asked for prohibition (禁止), and deny keeps the human fully in the execution loop, matching the dev-philosophy automation boundary.
- **Blocking only dangerous `rm -rf` targets (`/`, `~`, globs)** — target classification of shell strings is fragile; blocking the flag combination is predictable. `rm -r` without `-f` stays available for legitimate cleanup.
- **Blocking `mysqldump` / `wrangler d1 export`** — backups are read-only and reversible; blocking them adds friction without protecting data.
- **Env-var dumps (`printenv`, `env`)** — not blocked; the user's phrase "env関係" refers to `.env` files, and env output is already visible to any script Claude runs.

## Consequences

- `cat .env`, `rm -rf` (in all tested spellings), `mkfs`, `dd of=/dev/…`, and DB client invocations are denied with a reason telling Claude the fallback. Verified with a 35-case pipe-test matrix (allow and deny sides).
- Known over-blocking, accepted: `cp .env.example .env` (bootstrap) and `echo … > .env` (writes) are denied because command text cannot distinguish read from write; `rm -rf node_modules` requires the user. Under-blocking, accepted: this is an accident guard, not an adversarial boundary — a Python script deleting files or opening a DB would pass (`ponytail:` comments in the script name these ceilings).
- Pattern-matched DB clients cover the user's stack (MariaDB/SQLite/D1) plus common others; new clients must be added to the regex.
- Hook registration in `hooks.json` is read at session start — existing sessions need `/reload-plugins` or a restart to pick up the Bash matcher (the script itself is re-read on every invocation once registered).
