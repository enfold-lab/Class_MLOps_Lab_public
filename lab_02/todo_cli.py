#!/usr/bin/env python3

"""
USAGE EXAMPLES
--------------
## Add tasks
python todo_cli.py add "Clean code practice"
python todo_cli.py add "Prepare ppt slides" --due 2025-09-20

## List tasks (only todo by default)
python todo_cli.py list

## List all (including done)
python todo_cli.py list --all

## Mark done
python todo_cli.py done 1

## Delete a task
python todo_cli.py delete 2



TASK DESCRIPTION
----------------
You are given a WORKING BUT DIRTY implementation of a CLI To-Do application.

Your job is to **make the code clean** without changing the user-visible behavior.
(this process is called refactoring)

After refactoring, write a pytest unit test suite to verify the functionality of your application.

Once you have completed refactoring and testing, you may also try to improve the
user experience (UX) by adding new features or enhancing your code.
But remember: only do this after you are done with the refactoring task.
"""

import argparse
import datetime as dt
import sqlite3
 



DB_DEFAULT_PATH = "todo.db"

CONN = sqlite3.connect(DB_DEFAULT_PATH)
CONN.row_factory = sqlite3.Row

CONN.execute(
    """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        status TEXT CHECK(status IN ('todo','done')) NOT NULL DEFAULT 'todo',
        due_date TEXT,
        created_at TEXT NOT NULL DEFAULT (datetime('now'))
    );
    """
)




def str_to_date(text):
    """Parse string YYYY-MM-DD to date."""
    try:
        return dt.date.fromisoformat(text)
    except ValueError as e:
        raise ValueError("Invalid date format. Use YYYY-MM-DD.") from e

def date_to_str(d):
    return d.isoformat() if d else "-"





def build_parser():
    parser = argparse.ArgumentParser(prog="To-do CLI app.", description="SQLite-backed To-Do CLI application")

    sub = parser.add_subparsers(dest="command", required=True)

    # add
    p_add = sub.add_parser("add", help="Add a new task")
    p_add.add_argument("title", type=str, help="Task title")
    p_add.add_argument("--due", type=str, default=None, help="Due date YYYY-MM-DD (optional)")

    # list
    p_list = sub.add_parser("list", help="List tasks")
    p_list.add_argument("--all", action="store_true", help="Show all tasks (including completed).")

    # done
    p_done = sub.add_parser("done", help="Mark a task as completed")
    p_done.add_argument("id", type=int, help="Task ID")

    # delete
    p_del = sub.add_parser("delete", help="Delete a task")
    p_del.add_argument("id", type=int)

    return parser


def run_cli(args):
    try:
        if args.command == "add":
            due_date = str_to_date(args.due) if args.due else None
            due_str = due_date.isoformat() if due_date else None
            cur = CONN.execute(
                "INSERT INTO tasks (title, due_date) VALUES (?, ?)",
                (args.title, due_str),
            )
            CONN.commit()
            new_task_id = cur.lastrowid

            row = CONN.execute(
                "SELECT id, title, status, due_date, created_at FROM tasks WHERE id = ?",
                (new_task_id,),
            ).fetchone()
            if row is None:
                raise ValueError(f"Task with id {new_task_id} not found.")
            
            due = dt.date.fromisoformat(row["due_date"]) if row["due_date"] else None
            created_date = dt.datetime.fromisoformat(row["created_at"].replace(" ", "T"))
            print(f'Added #{row["id"]}: {row["title"]} (Created at: {created_date}, Due: {date_to_str(due)})')

        elif args.command == "list":
            sql = "SELECT id, title, status, due_date, created_at FROM tasks"

            if not args.all:
                sql += " WHERE status = 'todo'"

            sql += """
                ORDER BY
                    CASE status WHEN 'todo' THEN 0 ELSE 1 END,
                    CASE WHEN due_date IS NULL THEN 1 ELSE 0 END,
                    due_date,
                    created_at
            """
            rows = CONN.execute(sql).fetchall()

            print_data = []
            for row in rows:
                status_icon = "✅ " if row["status"] == "done" else "⬜ "
                due = row["due_date"] if row["due_date"] else "-"
                print_data.append(
                    (row["id"], row["title"], status_icon + row["status"], due, row["created_at"])
                )

            if not print_data:
                print("(no tasks)")

            headers = ("ID", "Title", "Status", "Due", "Created")
            widths = [max(len(str(x)) for x in col) for col in zip(headers, *print_data)]
            line = "  ".join(h.ljust(w) for h, w in zip(headers, widths))
            print(line)
            print("-" * len(line))
            for r in print_data:
                print("  ".join(str(x).ljust(w) for x, w in zip(r, widths)))

        elif args.command == "done":
            cur = CONN.execute(
                "UPDATE tasks SET status = 'done' WHERE id = ?",
                (args.id,),
            )
            if cur.rowcount == 0:
                raise ValueError(f"Task with id {args.id} not found.")
            CONN.commit()
            
            row = CONN.execute(
                "SELECT id, title, status, due_date, created_at FROM tasks WHERE id = ?",
                (args.id,),
            ).fetchone()
            if row is None:
                raise ValueError(f"Task with id {args.id} not found.")
            
            due = dt.date.fromisoformat(row["due_date"]) if row["due_date"] else None
            created_date = dt.datetime.fromisoformat(row["created_at"].replace(" ", "T"))
            print(f'Completed #{row["id"]}: {row["title"]} (Created at: {created_date}, Due: {date_to_str(due)})')

        elif args.command == "delete":
            cur = CONN.execute("DELETE FROM tasks WHERE id = ?", (args.id,))
            if cur.rowcount == 0:
                raise ValueError(f"Task with id {args.id} not found.")
            CONN.commit()

            print(f"Deleted #{args.id}")

        return 0
    
    except ValueError as ve:
        print(f"Error: {ve}")
        return 2
    except sqlite3.Error as se:
        print(f"Database error: {se}")
        return 3



def main():
    parser = build_parser()
    args = parser.parse_args()
    raise SystemExit(run_cli(args))


if __name__ == "__main__":
    main()
