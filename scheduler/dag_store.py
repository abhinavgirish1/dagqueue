from db.database import get_connection

#stores the dag in the database by inserting the tasks and dependencies into the database

def store_dag(dag_id: str, tasks: list[str], edges: list[list[str]]):
    con = get_connection()
    cur = con.cursor()

    for task in tasks:
        cur.execute(
            "INSERT INTO tasks (dag_id, name, status, start_time, end_time) VALUES (?, ?, ?, ?, ?)",
            (dag_id, task, "pending", None, None)
        )

    for from_task, to_task in edges:
        cur.execute("""
            INSERT INTO dependencies (task_id, depends_on_task_id)
            SELECT t1.id, t2.id
            FROM tasks t1, tasks t2
            WHERE t1.name = ? AND t2.name = ? AND t1.dag_id = ? AND t2.dag_id = ?
        """, (to_task, from_task, dag_id, dag_id))

    con.commit()
    con.close()