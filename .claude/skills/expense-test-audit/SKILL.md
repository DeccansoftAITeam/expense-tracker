---
name: expense-test-audit
description: Audits backend test names against the naming rules and reports
  badly named tests. Use when asked to check or audit test names.
allowed-tools: Bash(python ${CLAUDE_SKILL_DIR}/scripts/*)
disallowed-tools: Edit Write
---
Run python ${CLAUDE_SKILL_DIR}/scripts/list_expense_tests.py backend/tests
Then check each name against naming-rules.md.

Report a table: test name, OK or problem, a better name when it is a problem.
Do not edit any file.
