---
name: my-changes
description: Summarises uncommitted changes and flags risky edits. Use when the
  user asks what changed or wants a commit message.
allowed-tools: Bash(git diff *)
---
## Current changes
!`git diff HEAD`

## Instructions
Summarise the changes in 2-3 bullets, then list risks: floats for money,
local times instead of UTC, descriptions or amounts in logs, a DELETE route,
missing tests. If the diff is empty, say so.
