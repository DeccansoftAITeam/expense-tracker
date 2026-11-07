# Lab M12: Build an MCP server

**Time:** 60 minutes · **Branch:** `m12-mcp-build` (from `m11-mcp-connect`)

## What you build

`mcp-server/`, a Python MCP server named **expenses** (MCP Python SDK v2, `MCPServer`), that wraps the Expense Tracker API:

| Kind | Name | Does |
|---|---|---|
| Tool | `add_expense` | Adds an expense (amount in integer paise) |
| Tool | `list_expenses` | Lists expenses, optionally one category or with archived |
| Tool | `monthly_summary` | Totals per category for `YYYY-MM` |
| Tool | `budget_status` | Each budget with spent and over |
| Tool | `archive_expense` | Archives (never deletes, E6) |
| Resource template | `expenses://summary/{month}` | The month as readable text |
| Resource | `expenses://rules` | The data rules |
| Prompt | `review_month` | "Review my spending for this month against the budgets" |

You test it with the **Inspector** (CLI and UI), use it from **Claude Code** and **Claude Desktop**, and call it from your own **Python client**.

The server calls the backend over HTTP, so the rules E1–E8 stay in one place: the backend.

## Before you start

```text
git switch m11-mcp-connect
git switch -c m12-mcp-build
python --version        (macOS: python3 --version)   3.10 or newer
uv --version
node --version          22.19 or newer, for the Inspector
```

Keep the backend running in its own terminal for the whole lab:

```text
cd backend
uv run uvicorn app.main:app --reload
```

## The stdio rule (read this first)

A stdio server talks JSON-RPC over **stdout**. Anything else printed there corrupts the protocol, and the server "dies silently".

```text
print("hi")                      # wrong: breaks a stdio server
print("hi", file=sys.stderr)     # right
logging.info("hi")               # right, when logging goes to stderr
```

## Task 1: Scaffold the project (5 min)

From the project root:

```text
mkdir mcp-server
cd mcp-server
uv init --bare --name expense-mcp-server
uv add "mcp[cli]>=2.0.0" httpx
uv add --dev pytest
```

Claude prompt that does the same:

```text
Create a uv project in mcp-server/ named expense-mcp-server, Python 3.12+, with dependencies
"mcp[cli]>=2.0.0" and httpx, and pytest as a dev dependency. Add pytest settings: testpaths tests,
pythonpath ".". Do not write any code yet.
```

## Task 2: Write the server, one part at a time (15 min)

Ask Claude for each part, and read the code before you accept it.

**Part 1: the server and an HTTP helper.**

```text
Create mcp-server/server.py with the MCP Python SDK v2: from mcp.server import MCPServer,
mcp = MCPServer("expenses", instructions=...). Log to stderr only with logging.basicConfig(stream=sys.stderr),
and set the httpx logger to WARNING. Read the API address from EXPENSE_API_URL, default http://localhost:8000.
Add http_client() that returns httpx.Client(base_url=API_URL, timeout=10), so tests can replace it, and
_call(method, path, **kwargs) that returns the JSON or, for a status of 400 or more, raises
ToolError (from mcp.server.mcpserver.exceptions) with the status and the API's error messages,
without echoing the input values back (E8). End the file with mcp.run(transport="stdio") under __main__.
```

**Part 2: tools.** Type hints become the input schema; the docstring becomes the description every client sees.

```text
In server.py add five tools with @mcp.tool(): add_expense(description: str, amount_paise: int,
category: Literal[...6 categories...] = "other", spent_on: str | None = None,
payment_method: Literal["cash","card","upi","netbanking"] = "upi") -> dict;
list_expenses(category=None, include_archived=False) -> list[dict]; monthly_summary(month: str) -> dict;
budget_status(month: str) -> list[dict]; archive_expense(expense_id: int) -> dict (PATCH archived true).
Each calls the backend through _call. Docstrings say that amounts are integer paise (₹250.50 is 25050)
and months are YYYY-MM. Log only ids (E8).
```

**Part 3: resources and a prompt.**

```text
Add a resource template @mcp.resource("expenses://summary/{month}") that returns the summary as text,
amounts as rupees with 2 decimals using integer maths only, leaving out categories with nothing spent.
Add a fixed resource expenses://rules with the data rules as JSON. Add @mcp.prompt() review_month(month)
that asks to call monthly_summary and budget_status, show a table, list the three largest expenses,
and change nothing.
```

Run it:

```text
uv run server.py
```

**Expected:** it "hangs": it is waiting for JSON-RPC on stdin. That is correct. Stop it with **Ctrl+C**.

## Task 3: The Inspector — CLI, then UI (10 min)

List the tools:

```text
npx @modelcontextprotocol/inspector --cli uv run server.py --method tools/list
```

Call one:

```text
npx @modelcontextprotocol/inspector --cli uv run server.py --method tools/call --tool-name monthly_summary --tool-arg month=2026-11
```

Break a rule on purpose (above ₹1,00,000):

```text
npx @modelcontextprotocol/inspector --cli uv run server.py --method tools/call --tool-name add_expense --tool-arg description=Laptop --tool-arg amount_paise=10000001
```

**Expected:** `"isError": true` with the backend's message. The server keeps running. (With a plain `ValueError` you also get `isError`, but the SDK hides the message; `ToolError` shows it.)

Now the UI:

```text
uv run mcp dev server.py
```

Open the URL it prints. Set **Protocol Era = Auto** in Server Settings and click **Connect**. Then:

1. **Tools**: run `list_expenses` with `category` = `food`.
2. **Resources → Templates**: read `expenses://summary/2026-11`.
3. **Prompts**: get `review_month` with `month` = `2026-11`.
4. **Protocol** tab: every request carries a `_meta` block.

Stop it with **Ctrl+C**.

## Task 4: Use it from Claude Code (8 min)

Go back to the project root and register it for the team (project scope):

```text
cd ..
claude mcp add --scope project --transport stdio expenses --env EXPENSE_API_URL=http://localhost:8000 -- uv run --directory mcp-server server.py
```

Open `.mcp.json`: the `expenses` entry is next to `filesystem` and `playwright`. Add read-only tools to the allow list in `.claude/settings.json`:

```text
Allow mcp__expenses__list_expenses, mcp__expenses__monthly_summary and mcp__expenses__budget_status
in .claude/settings.json. Leave add_expense and archive_expense to ask.
```

Start `claude`, approve the server, check `/mcp`, then:

```text
I spent 180 rupees on an auto today and 2,450.50 on groceries. Add both.
```

**Expected:** two `add_expense` calls with **18000** and **245050** paise, each asking for approval. Then:

```text
/mcp__expenses__review_month 2026-11
```

(Use this month.) **Expected:** a table from `monthly_summary` and `budget_status`, with no prompts. Check the new expenses at http://localhost:5173.

## Task 5: Use it from Claude Desktop (5 min)

```text
cd mcp-server
uv run mcp install server.py --name expenses --with httpx -v EXPENSE_API_URL=http://localhost:8000
```

`--with httpx` matters: Claude Desktop starts the server with only `mcp[cli]` plus what you list.

Or add it by hand to `claude_desktop_config.json` (Settings → Developer → Edit Config). Use the **absolute** paths to `uv` (`where uv` on Windows, `which uv` on macOS) and to your `mcp-server` folder:

```json
{
  "mcpServers": {
    "expenses": {
      "command": "C:\\Users\\you\\.local\\bin\\uv.exe",
      "args": ["run", "--directory", "C:\\work\\expense-tracker\\mcp-server", "server.py"],
      "env": { "EXPENSE_API_URL": "http://localhost:8000" }
    }
  }
}
```

Fully quit and restart Claude Desktop. Ask: `What did I spend on food this month?`

## Task 6: Your own client, and tests (12 min)

```text
Create mcp-server/stdio_client.py: launch server.py over stdio with
StdioServerParameters(command=sys.executable, args=["server.py"]) and mcp.Client. Print the tool names,
call add_expense with 4999 paise in food, read expenses://summary/<that month> (take spent_on from the
JSON text of the result), then call add_expense with 10000001 paise and print is_error and the message.
Use anyio.run(main).
```

```text
uv run stdio_client.py
```

Note: tools return `.content`, resources return `.contents` (plural). Result fields are snake_case (`is_error`).

Now tests that need no backend at all:

```text
Create mcp-server/tests/test_server.py. Use an in-memory client: async with Client(server.mcp).
Replace server.http_client with an httpx.Client using httpx.MockTransport and a fake backend.
Test: the five tool names; amount_paise is "integer" in the input schema; add_expense posts the amount;
an API 422 gives is_error and the next call still works; archiving id 9 (404) is an error;
the summary resource shows ₹250.50; the review_month prompt names the month.
```

```text
uv run pytest -q
```

## Optional: run it over HTTP

In `server.py`, swap the last line for `mcp.run(transport="streamable-http", port=8001)` (port 8000 is the backend). Run `uv run server.py`, then open the Inspector with `npx @modelcontextprotocol/inspector`, choose **Streamable HTTP** and URL `http://localhost:8001/mcp`. Put a breakpoint in a tool and call it from the Inspector. Switch back to stdio afterwards.

## Finish

```text
git add -A
git commit -m "M12: expenses MCP server with tools, resources, prompt and tests"
git switch main
git merge --no-ff m12-mcp-build -m "Merge M12"
git switch m12-mcp-build
```

`main` now holds the complete course app.

## Done when

- [ ] `npx @modelcontextprotocol/inspector --cli uv run server.py --method tools/list` shows the five tools.
- [ ] A too-large amount returns `isError: true` with the backend's message, and the server keeps running.
- [ ] In the Inspector UI you read the summary template and got the `review_month` prompt.
- [ ] Claude Code added expenses through `add_expense` with integer paise, and `review_month` ran without prompts.
- [ ] `uv run stdio_client.py` and `uv run pytest -q` in `mcp-server/` both work.
- [ ] Nothing in `server.py` prints to stdout.

## If you get stuck

- The server connects and then dies at once: look for a `print()` without `file=sys.stderr`.
- Every tool fails with "Connection refused": the backend is not running on port 8000.
- `mcp dev` cannot find the server object: the variable must be named `mcp` (or pass `server.py:mcp`).
- Compare with the reference branch `m12-mcp-build`.
