# dagqueue

A DAG-based task queue built in Python from scratch.

## Status

Work in progress (week 2). Core execution pipeline is running end-to-end. FastAPI layer and priority queue are next.

## Architecture

- **FastAPI** — REST API for submitting DAGs and querying status *(planned)*
- **SQLite** — persistence for tasks, dependencies, status, and results
- **Kahn's algorithm** — cycle detection and topological scheduling
- **ThreadPoolExecutor** — concurrent task execution
- **BFS failure propagation** — skip downstream tasks when upstream fails *(planned)*
- **Retry with exponential backoff** *(planned)*
- **Priority scheduling** (high / medium / low) *(planned)*

## Project layout

```
api/          FastAPI routes (planned)
db/           SQLite schema and models
queue/        Task queue (planned)
scheduler/    DAG validation, storage, and scheduling
worker/       Thread pool for task execution
```

## What's implemented

- SQLite schema (`tasks`, `dependencies`)
- `has_cycle()` — Kahn's algorithm for cycle detection
- `store_dag()` — persist a DAG and its edges to the database
- `get_ready_tasks()` — returns tasks whose dependencies are all complete
- `run_loop()` — polls the DB and dispatches ready tasks to the worker pool
- `WorkerPool` — wraps `ThreadPoolExecutor`; accepts an injectable executor callable and updates task status to `success`/`failed` after each run
