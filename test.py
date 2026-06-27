"""Smoke tests for database and DAG modules. Run with: python test.py"""

import os

from db.database import init
from db.models import Task
from scheduler.dag_store import store_dag
from scheduler.dag_validator import has_cycle
from scheduler.scheduler import get_ready_tasks, run_loop


def reset_db():
    if os.path.exists("db/tutorial.db"):
        os.remove("db/tutorial.db")
    init()


def test_database_roundtrip():
    reset_db()
    Task.create(
        dag_id="smoke_dag",
        name="smoke_task",
        status="pending",
        start_time=None,
        end_time=None,
    )
    tasks = Task.get_all()
    assert any(t[1] == "smoke_dag" and t[2] == "smoke_task" for t in tasks)


def test_cycle_detection():
    assert not has_cycle(["a", "b", "c"], [["a", "b"], ["b", "c"]])
    assert has_cycle(["a", "b"], [["a", "b"], ["b", "a"]])


def test_store_dag():
    reset_db()
    store_dag("test_dag", ["a", "b"], [["a", "b"]])
    tasks = Task.get_all()
    dag_tasks = [t for t in tasks if t[1] == "test_dag"]
    assert len(dag_tasks) == 2


def test_store_dag_rejects_cycle():
    reset_db()
    try:
        store_dag("bad_dag", ["a", "b"], [["a", "b"], ["b", "a"]])
        assert False, "Expected ValueError for cyclic DAG"
    except ValueError:
        pass
    tasks = [t for t in Task.get_all() if t[1] == "bad_dag"]
    assert len(tasks) == 0


def test_get_ready_tasks():
    reset_db()
    store_dag("ready_dag", ["a", "b", "c"], [["a", "b"], ["a", "c"]])

    ready = get_ready_tasks("ready_dag")
    assert ready == ["a"]

    a_row = next(t for t in Task.get_all() if t[1] == "ready_dag" and t[2] == "a")
    Task.update_status(a_row[0], "success")

    ready = get_ready_tasks("ready_dag")
    assert set(ready) == {"b", "c"}



if __name__ == "__main__":
    test_database_roundtrip()
    test_cycle_detection()
    test_store_dag()
    test_store_dag_rejects_cycle()
    test_get_ready_tasks()
    print("All smoke tests passed.")
