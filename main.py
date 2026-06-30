from db.database import init
from scheduler.dag_store import store_dag
from scheduler.scheduler import run_loop
from worker.worker_pool import WorkerPool


def main():
    init()

    dag_id = "example_dag"
    store_dag(
        dag_id,
        tasks=["fetch", "process", "save"],
        edges=[["fetch", "process"], ["process", "save"]],
    )

    pool = WorkerPool(max_workers=4)
    try:
        run_loop(dag_id, pool)
    finally:
        pool.shutdown()


if __name__ == "__main__":
    main()
