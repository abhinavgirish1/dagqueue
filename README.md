# dagqueue

A DAG-based task queue built in Python from scratch.

## Status

Work in progress (week 1). Schema, cycle detection, and DAG persistence are implemented. Scheduler, worker pool, and FastAPI layer are next.

## Architecture

- **FastAPI** — REST API for submitting DAGs and querying status *(planned)*
- **SQLite** — persistence for tasks, dependencies, status, and results
- **Kahn's algorithm** — cycle detection and topological scheduling
- **ThreadPoolExecutor** — concurrent task execution *(planned)*
- **BFS failure propagation** — skip downstream tasks when upstream fails *(planned)*
- **Retry with exponential backoff** *(planned)*
- **Priority scheduling** (high / medium / low) *(planned)*

## Project layout

```
api/          FastAPI routes (planned)
db/           SQLite schema and models
queue/        Task queue (planned)
scheduler/    DAG validation, storage, and scheduling
worker/       Thread pool for task execution (planned)
```

## Setup

Requires Python 3.10+.

```bash
python test.py          # run smoke tests
```

No third-party dependencies yet. See `requirements.txt`.

## What's implemented

- SQLite schema (`tasks`, `dependencies`)
- `has_cycle()` — Kahn's algorithm for cycle detection
- `store_dag()` — persist a DAG and its edges to the database
