#!/usr/bin/env python3
"""PreToolUse hook: deny dangerous Bash commands (secret reads, destructive ops, direct DB access)."""
import json
import re
import sys

cmd = json.load(sys.stdin).get("tool_input", {}).get("command") or ""


def deny(reason):
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": f"fable-coding: {reason}",
                }
            }
        )
    )
    sys.exit(0)


# 1. .env references (templates stay readable — same policy as deny-secrets.py / ADR 0008).
# ponytail: matches command text, so writes like `cp .env.example .env` are also
# denied; ask the user to run those themselves.
for m in re.finditer(r'(?:^|[\s"\'=/(])(\.env(?:\.[A-Za-z0-9_.-]+)?)', cmd):
    if not m.group(1).endswith((".example", ".sample", ".template")):
        deny(
            f"'{m.group(1)}' referenced in Bash command; may expose secrets. "
            "Read the .env.example/.sample/.template variant, or ask the user to run this."
        )

# 2. Destructive commands.
# ponytail: only rm with BOTH -r and -f is blocked; plain `rm -r` still works.
for seg in re.split(r"[;|&\n]", cmd):
    if re.match(r"\s*(?:sudo\s+)?rm\s", seg) or re.search(
        r"(?:\bxargs\s+|-exec\s+)(?:sudo\s+)?rm\s", seg
    ):
        flags = "".join(re.findall(r"\s-([A-Za-z]+)", seg))
        long_flags = re.findall(r"\s--(\w[\w-]*)", seg)
        recursive = "r" in flags or "R" in flags or "recursive" in long_flags
        force = "f" in flags or "force" in long_flags
        if recursive and force:
            deny("rm -rf blocked. Ask the user to run destructive deletions themselves.")
if re.search(r"\bmkfs", cmd) or re.search(r"\bdd\b[^;|&\n]*\bof=/dev/", cmd):
    deny("filesystem/device-destroying command blocked.")

# 3. Direct DB access (human-in-the-loop: report the statement, let the user run it).
if re.search(
    r"(?:^|[;&|(\n]\s*|\bsudo\s+)(mysql|mariadb|psql|sqlite3|mongosh|mongo|redis-cli)\b", cmd
) or re.search(r"\bwrangler\s+d1\s+(execute|migrations\s+apply)\b", cmd):
    deny(
        "direct DB access via Bash blocked. Report the exact statement(s) to the user "
        "and let them execute (fable-coding section 4)."
    )
