# 0007: Rename the plugin from fable-coding to wanyaldee-skills

(日本語: [0007-rename-to-wanyaldee-skills.ja.md](../ja/0007-rename-to-wanyaldee-skills.ja.md))

## Context

The plugin started as one skill reproducing Fable 5's coding discipline
("fable-coding" fit). By v1.7.0 it carried five skills — coding discipline,
dev philosophy, a Fable 5 prompting reference, memory discipline, memory
audit — plus a credential hook. The user observed the name no longer
describes the contents and proposed "Wanyaldee's Skills Package".

## Decision

Full rename to `wanyaldee-skills` at v2.0.0 (kebab-case identifier; the
display name stays "Wanyaldee's Skills Package"): GitHub repo renamed via
`gh repo rename` (old URLs redirect, so existing clones and the old
marketplace path keep working), plugin and marketplace identifiers changed
in `.claude-plugin/*.json`, README retitled with migration steps. The inner
`fable-coding` *skill* keeps its name — it genuinely is the Fable 5 coding
discipline; package name and skill role now separate cleanly. Major version
bump because the install identity changes: existing installs must
uninstall `fable-coding`, remove the old marketplace, and re-add
`Wanyaldee/wanyaldee-skills`.

## Alternatives rejected

- **Rename the repo only** — leaves the plugin identifier lying about its
  contents, which was the actual complaint; saves one reinstall at the cost
  of permanent skew.
- **Also rename the `fable-coding` skill** — its name is accurate for what
  it does; renaming it would break the one name that still fits.
- **Deferring until "later"** — the repo went public hours ago with no
  external users; this is the cheapest the rename will ever be.

## Consequences

- Skill namespace changes from `fable-coding:*` to `wanyaldee-skills:*`;
  each installed environment reinstalls once.
- The local clone directory `~/fable-coding` was intentionally left as-is
  (renaming it mid-session breaks the running session); the user can `mv`
  it at leisure — git remotes already point at the new URL.
- GitHub's redirect from the old repo name persists until a new repo takes
  the old name; the README documents the new path so nothing relies on the
  redirect long-term.
