import sqlite3
import datetime

# Connect to the database
conn = sqlite3.connect("todo.db")
cursor = conn.cursor()

# Creating the table
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Pending',
    date_added TEXT NOT NULL
)
""")
conn.commit()


def remove_task():
    print("Let's check your tasks first...")
    view_tasks()
    try:
        task_id = input("Task ID to delete: ").strip()
        task_id = int(task_id)
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        print(f"Task {task_id} is gone.")
    except ValueError:
        print("Hmm, that doesn't look right.")
    except Exception as e:
        print("something broke. Not sure what happened.", e)

def new_task():
    task = input("What's your task? ").strip()
    if not task:
        print("You gotta type something.")
        return
    date_added = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO tasks (task, status, date_added) VALUES (?, 'Pending', ?)", (task, date_added))
    conn.commit()
    print(f"Alright, added: {task}")

def view_tasks(status_filter=None):
    print("Fetching tasks...")  
    query = "SELECT * FROM tasks"
    params = []
    
    if status_filter:
        query += " WHERE status = ?"
        params.append(status_filter)
    query += " ORDER BY date_added ASC"
    cursor.execute(query, params)
    tasks = cursor.fetchall()
    if not tasks:
        print("Nothing here yet.")
        return

    print("\nID | Task                         | Status   | Date Added")
    print("-" * 55)
    for t in tasks:
        print(f"{t[0]}  | {t[1][:25]:<25} | {t[2]:<8} | {t[3]}")

def set_task_done():
    print("Pending tasks:")
    view_tasks("Pending")
    try:
        task_id = input("Which one is done? ").strip()
        task_id = int(task_id)
        cursor.execute("UPDATE tasks SET status = 'Completed' WHERE id = ?", (task_id,))
        conn.commit()
        print(f"Task {task_id} is now marked done.")
    except ValueError:
        print("that's not a number.")
    except Exception as e:
        print("Weird error.what happened.", e)

def change_task():
    view_tasks()
    try:
        task_id = input("Which task to edit? ").strip()
        task_id = int(task_id)
        new_task = input("New description: ").strip()
        if not new_task:
            print("you need to enter something.")
            return
        cursor.execute("UPDATE tasks SET task = ? WHERE id = ?", (new_task, task_id))
        conn.commit()
        print(f"Alright, updated task {task_id}.")
    except ValueError:
        print("That ID looks weird.")
    except Exception as e:
        print("that didn't work", e)

while True:
    print("\n==== Task Manager ====")
    print("1) Add a Task")
    print("2) Show All Tasks")
    print("3) Show Pending Tasks")
    print("4) Show Completed Tasks")
    print("5) Edit a Task")
    print("6) Mark Task as Done")
    print("7) Delete a Task")
    print("8) Exit")

    choice = input("> Enter choice: ").strip()

    if choice == "1":
        new_task()
    elif choice == "2":
        view_tasks()
    elif choice == "3":
        view_tasks("Pending")
    elif choice == "4":
        view_tasks("Completed")
    elif choice == "5":
        change_task()
    elif choice == "6":
        set_task_done()
    elif choice == "7":
        remove_task()
    elif choice == "8":
        print("Alright, see ya.")
        break
    else:
        print("That's not an option.")

conn.close()
