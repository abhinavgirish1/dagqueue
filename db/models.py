from db.database import get_connection

class Task:
    @staticmethod
    def create(dag_id, name, status, start_time, end_time):
        con = get_connection()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO tasks (dag_id, name, status, start_time, end_time) VALUES (?, ?, ?, ?, ?)",
            (dag_id, name, status, start_time, end_time),
        )
        con.commit()
        con.close()

    @staticmethod
    def get_all():
        con = get_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM tasks")
        tasks = cur.fetchall()
        con.close()
        return tasks
    
    @staticmethod
    def get_by_id(task_id):
        con = get_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        task = cur.fetchone()
        con.close()
        return task
    
    @staticmethod
    def delete(task_id):
        con = get_connection()
        cur = con.cursor()
        cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        con.commit()
        con.close()