from db.models import Task
import time

#returns a list of task names that are ready to run

def get_ready_tasks(dag_id: str) -> list[str]:
    ready_tasks = []
    tasks = Task.get_all()
    for task in tasks:
        if task[1] == dag_id and task[3] == "pending":
            dependencies = Task.get_dependencies(task[0])
            count = 0
            if len(dependencies) == 0:
                ready_tasks.append(task[2])
                continue
            for dependency in dependencies:
                dep_id = dependency[2]
                dep_task = Task.get_by_id(dep_id)
                if dep_task[3] != "success":
                    continue
                count += 1
            if count == len(dependencies):
                ready_tasks.append(task[2])
    return ready_tasks


def run_loop(dag_id: str, worker):
    while True:
        ready_tasks = get_ready_tasks(dag_id)
        if len(ready_tasks) == 0:
            tasks = Task.get_all()
            if any(t[1] == dag_id and t[3] in ("pending", "running") for t in tasks):
                time.sleep(5)
                continue
            break

        for task_name in ready_tasks:
            task_row = next(
                t for t in Task.get_all()
                if t[1] == dag_id and t[2] == task_name
            )
            Task.update_status(task_row[0], "running")
            worker.submit(task_name)

        time.sleep(5)
