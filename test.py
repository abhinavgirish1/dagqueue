"""smoke tests for database and dag modules. Run with: python test.py"""

from db.database import init
from db.models import Task
from scheduler.dag_store import store_dag
from scheduler.dag_validator import has_cycle


def test_database_roundtrip():
    init()
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
    init()
    store_dag("test_dag", ["a", "b"], [["a", "b"]])
    tasks = Task.get_all()
    dag_tasks = [t for t in tasks if t[1] == "test_dag"]
    assert len(dag_tasks) == 2


if __name__ == "__main__":
    test_database_roundtrip()
    test_cycle_detection()
    test_store_dag()
    print("All smoke tests passed.")
