import sqlite3

path_db = 'todo.db'

def init_db():
    with sqlite3.connect(path_db) as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT, completed INTEGER)")
        conn.commit()

def add_task(task):
    with sqlite3.connect(path_db) as conn:
        cursor = conn.cursor()        
        cursor.execute("INSERT INTO tasks (task, completed) VALUES (?, 0)", (task, ))
        conn.commit()
        return cursor.lastrowid

def update_task(task_id, new_task):
    with sqlite3.connect(path_db) as conn:
        cursor = conn.cursor()        
        cursor.execute("UPDATE tasks SET task = ? WHERE id = ?", (new_task, task_id))
        conn.commit()

def update_task_status(task_id, completed):
    with sqlite3.connect(path_db) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (1 if completed else 0, task_id))
        conn.commit()

def get_tasks(filter_type):
    with sqlite3.connect(path_db) as conn:
        cursor = conn.cursor()        
        if filter_type == 'all':
            cursor.execute("SELECT * FROM tasks")
        elif filter_type == 'completed':
            cursor.execute("SELECT * FROM tasks WHERE completed = 1")
        elif filter_type == 'uncompleted':
            cursor.execute("SELECT * FROM tasks WHERE completed = 0")
        return cursor.fetchall()

def delete_task(task_id):
    with sqlite3.connect(path_db) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()

def delete_completed_tasks():
    with sqlite3.connect(path_db) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE completed = 1")
        conn.commit()