from concurrent.futures import ThreadPoolExecutor, Future
from typing import Callable
from db.models import Task


class WorkerPool:
    def __init__(self, max_workers: int = 4, executor: Callable[[str], None] = None):
        self._pool = ThreadPoolExecutor(max_workers=max_workers)
        self._executor = executor or WorkerPool._default_executor

    def submit(self, task_id: int, task_name: str) -> Future:
        return self._pool.submit(self._run_task, task_id, task_name)

    def _run_task(self, task_id: int, task_name: str):
        try:
            self._executor(task_name)
            Task.update_status(task_id, "success")
        except Exception:
            Task.update_status(task_id, "failed")
            raise

    @staticmethod
    def _default_executor(task_name: str):
        import time
        print(f"[worker] starting  {task_name}")
        time.sleep(1)
        print(f"[worker] finished  {task_name}")

    def shutdown(self, wait: bool = True):
        self._pool.shutdown(wait=wait)
