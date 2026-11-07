---
name: new-component
description: Creates a React component with a matching Vitest test
arguments: [name, folder]
argument-hint: [Name] [folder]
disable-model-invocation: true
---
Create frontend/src/$folder/$name.jsx and a matching test
frontend/src/$folder/$name.test.jsx.

- Function component with hooks, JavaScript (.jsx), never TypeScript.
- Follow the style of frontend/src/components/ExpenseList.jsx.
- Format money only with formatRupees from frontend/src/money.js (E1).
- The test uses Vitest and @testing-library/react, and calls cleanup after each test.

Run `cd frontend && npm test` and `npm run build` before you finish.
