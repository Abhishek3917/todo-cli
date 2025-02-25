import os
import json
import curses
from datetime import datetime

TODO_FILE = "todo_list.json"

def load_todos():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, 'r') as file:
            todos = json.load(file)

            for todo in todos:
                if 'added_on' not in todo:
                    todo['added_on'] = datetime.now().strftime("%d-%m-%Y")  
                if 'deadline' not in todo:
                    todo['deadline'] = "No deadline"  

            return todos
    return []

def save_todos(todos):
    with open(TODO_FILE, 'w') as file:
        json.dump(todos, file, indent=4)

def add_task(todos, task, deadline):
    current_date = datetime.now().strftime("%d-%m-%Y")
    todos.append({"task": task, "completed": False, "added_on": current_date, "deadline": deadline})
    save_todos(todos)

def toggle_task_status(todos, task_number):
    if task_number < len(todos):
        todos[task_number]["completed"] = not todos[task_number]["completed"]
        save_todos(todos)

def delete_task(todos, task_number):
    if task_number < len(todos):
        del todos[task_number]
        save_todos(todos)

def show_tasks(stdscr, todos, selected_task):
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    if not todos:
        stdscr.addstr(0, 0, "No tasks found.")
    else:
        for index, todo in enumerate(todos):
            
            added_on = todo.get('added_on', 'No date')
            deadline = todo.get('deadline', 'No deadline')

            task = f"{index + 1}. {todo['task']} [{ 'Done' if todo['completed'] else 'Not done' }] | Added: {added_on} | Deadline: {deadline}"

            if index == selected_task:
                stdscr.addstr(index, 0, task, curses.A_REVERSE) 
            else:
                stdscr.addstr(index, 0, task)

    stdscr.refresh()

def main(stdscr):
    todos = load_todos()
    selected_task = 0

    while True:
        show_tasks(stdscr, todos, selected_task)

        key = stdscr.getch()

        if key == curses.KEY_UP or key == ord('k'):
            selected_task = max(0, selected_task - 1)  
        elif key == curses.KEY_DOWN or key == ord('j'):
            selected_task = min(len(todos) - 1, selected_task + 1)
        elif key == ord('\n'): 
            if todos[selected_task]["completed"]:
                continue
            toggle_task_status(todos, selected_task) 
        elif key == ord('q'): 
            break
        elif key == ord('a'): 
            stdscr.clear()
            stdscr.addstr(0, 0, "Enter task description: ")
            stdscr.refresh()
            curses.echo()
            task = stdscr.getstr(1, 0).decode("utf-8")

            stdscr.addstr(2, 0, "Enter deadline (dd-mm-yyyy): ")
            stdscr.refresh()
            deadline = stdscr.getstr(3, 0).decode("utf-8")
            
          
            try:
                datetime.strptime(deadline, "%d-%m-%Y")
            except ValueError:
                stdscr.addstr(5, 0, "Invalid date format! Please use dd-mm-yyyy.")
                stdscr.refresh()
                stdscr.getch() 
                continue

            add_task(todos, task, deadline)
            stdscr.clear()
        elif key == ord('r'):  
            todos = load_todos()
        elif key == ord('d'):  
            if len(todos) > 0:
                delete_task(todos, selected_task)
                selected_task = min(len(todos) - 1, selected_task)
        elif key == ord('c'):  
            toggle_task_status(todos, selected_task) 

        stdscr.refresh()

if __name__ == "__main__":

    KEYBINDINGS = """

                    j/k or Arrow Down/Up  - Navigate through tasks
                    Enter                 - Toggle task completion
                    a                     - Add a new task
                    d                     - Delete selected task
                    c                     - Change task status manually
                    r                     - Reload tasks
                    q                     - Quit
                """
                
    curses.wrapper(main)
    print(KEYBINDINGS)