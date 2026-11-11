# Return Batch Reconciliation Desk

Start with the [client request](SPEC.md). This application currently lets a coordinator register
expected cases manually, inspect XML files and download an inspection report. The six requested
capabilities are for you to build. Existing application code earns no new implementation credit.
Work one capability at a time: decide how a part should work and say so before you ask your coding
agent to build it, and ask it to stop when that part is done. An agent asked for everything at once
makes every design decision for you.

## Run locally

Use Python 3.12+, Node.js 24, uv and pnpm. Run these commands from the repository root:

```sh
uv sync --directory backend --locked
pnpm --dir frontend install --frozen-lockfile
```

In one terminal:

```sh
uv run --directory backend uvicorn return_desk.app:create_app --factory --host 127.0.0.1 --port 8000
```

In another:

```sh
pnpm --dir frontend dev
```

Open http://127.0.0.1:5173. Register `DEMO-101,2025` and upload `samples/xml/example.xml` to
explore the existing behavior. No API account, key or environment file is needed. The local
SQLite file defaults to `backend/data/desk.sqlite3`; `RETURN_DESK_DB` can select another location.
Keep any data you need before resetting a disposable local database.

## What is supplied

- `frontend/`: a small React/Vite application.
- `backend/`: its FastAPI application and runtime dependencies.
- `samples/expected.csv`: a minimal example of the expected-case list (Feature 1).
- `samples/xml/example.xml`: an example the existing application reads.
- `samples/deliveries/`: one input ZIP per supplier (Feature 2). They are not output handoffs.

Read [customer formats](docs/input-formats.md), [assignment requirements](docs/submission.md)
and the separate [Quiz](docs/quiz.md). The existing application does not yet accept CSV or ZIP.
The format examples are not test cases with prepared expected results. Design and implement your
own tests, test data, quality checks and CI. No completed testing or CI setup is included.
