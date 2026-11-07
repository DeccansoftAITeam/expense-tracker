---
name: review-expense-change
description: Reviews the branch's expense changes in a separate, read-only context.
disable-model-invocation: true
context: fork
agent: Explore
background: false
allowed-tools: Bash(git diff *)
---
Diff to review:
!`git diff main...HEAD`

Check rules E1-E8 from CLAUDE.md, each as OK or problem: integer paise,
YYYY-MM-DD and UTC dates, description 1-120, amount 1 to 10,000,000 paise,
category values, no delete, no clock in rules.py, no descriptions or amounts
in logs. Also: every new endpoint has a test. Quote the line for each problem.
