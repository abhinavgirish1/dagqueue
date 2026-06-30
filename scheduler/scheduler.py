from db.models import Task
import time

#returns a list of task names that are ready to run

def get_ready_tasks(dag_id: str) -> list[str]:
    tasks = Task.get_by_dag(dag_id)
    status_by_id = {task[0]: task[3] for task in tasks}

    ready_tasks = []
    for task in tasks:
        if task[3] != "pending":
            continue
        deps = Task.get_dependencies(task[0])
        if all(status_by_id.get(dep[2]) == "success" for dep in deps):
            ready_tasks.append(task[2])

    return ready_tasks


def run_loop(dag_id: str, worker):
    while True:
        ready_tasks = get_ready_tasks(dag_id)
        if not ready_tasks:
            tasks = Task.get_by_dag(dag_id)
            if any(t[3] in ("pending", "running") for t in tasks):
                time.sleep(5)
                continue
            break

        tasks_by_name = {t[2]: t for t in Task.get_by_dag(dag_id)}
        for task_name in ready_tasks:
            task_id = tasks_by_name[task_name][0]
            Task.update_status(task_id, "running")
            worker.submit(task_id, task_name)

        time.sleep(5)
