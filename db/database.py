import sqlite3

# Establishing and returning a connection to the SQLite database.
def get_connection(db_name="db/tutorial.db"):
    return sqlite3.connect(db_name)

def init():
    # Initializing the database by creating the required tables if they do not already exist.
    con = get_connection()
    cur = con.cursor()

    # Creating the tasks table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY, 
            dag_id TEXT, 
            name TEXT, 
            status TEXT, 
            start_time TEXT, 
            end_time TEXT
        )
    """)

    # Creating the dependencies table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS dependencies (
            id INTEGER PRIMARY KEY, 
            task_id INTEGER, 
            depends_on_task_id INTEGER, 
            FOREIGN KEY(task_id) REFERENCES tasks(id), 
            FOREIGN KEY(depends_on_task_id) REFERENCES tasks(id)
        )
    """)

    con.commit()
    con.close()