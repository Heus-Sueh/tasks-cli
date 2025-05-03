import json
import sys
from pathlib import Path
from datetime import datetime
from pydantic import Field, BaseModel
from typing import Literal

JSON_FILE = "tasks.json"


class Task(BaseModel):
    id: int
    description: str
    status: Literal["todo", "done", "in-progress"]
    created_at: str = Field(
        default_factory=lambda: datetime.now().strftime("%d %b %Y - %H:%M")
    )
    updated_at: str = Field(
        default_factory=lambda: datetime.now().strftime("%d %b %Y - %H:%M")
    )


def help_command() -> None:
    program_name = sys.argv[0]
    help_text = f"""A task manager
    Usage: {program_name} <COMMAND>
    Commands: 
        add 
        update | upd <ID> <new description>
        remove | delete | del 
        mark-done <ID> 
        mark-in-progress <ID> 
        list (done, todo, in-progress)"
    """
    print(help_text)


def read_json(json_file: Path) -> list[Task]:
    json_file = JSON_FILE
    if Path(json_file).exists():
        try:
            with Path.open(json_file) as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Error find the json file")
    return []


def write_to_json(data, file_path) -> None:
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


def add_command():
    try:
        command = sys.argv[2]
        createdAt = strftime("%d %b %Y - %H:%M")
        task = {
            "id": 1,
            "description": str(command),
            "status": "todo",
            "createdAt": createdAt,
            "updatedAt": createdAt,
        }
        tasks = read_json(JSON_FILE)

        if tasks:
            # calcula o próximo id baseado na ultima task adicionada
            max_id = max(task["id"] for task in tasks)
            task["id"] = max_id + 1

        tasks.append(task)
        write_to_json(tasks, JSON_FILE)

        print(f"{command} - Task added successfully (ID: {task['id']})")

    except IndexError:
        print(f'Usage: {sys.argv[0]} add "study"')


def delete_command():
    try:
        selected_id = int(sys.argv[2])
        tasks = read_json(JSON_FILE)

        updated_tasks = [task for task in tasks if task["id"] != selected_id]
        if len(updated_tasks) == len(tasks):
            print("No task with this ID founded")
        else:
            removed_task = next(task for task in tasks if task["id"] == selected_id)
            print(
                f"{removed_task['description']} - Task removed successfully (ID: {removed_task['id']})",
            )
        write_to_json(updated_tasks, JSON_FILE)

    except IndexError:
        print(f"Usage: {sys.argv[0]} delete <ID>")

    except ValueError:
        print("The <ID> must be a Integer")


def update_command():
    try:
        selected_id = int(sys.argv[2])
        new_description = sys.argv[3]

        tasks = read_json(JSON_FILE)
        found = False
        for task in tasks:
            if task["id"] == selected_id:
                task["description"] = new_description
                task["updatedAt"] = strftime("%d %b %Y - %H:%M")
                print(
                    f"{task['description']} - Task updated successfully (ID: {task['id']})",
                )
                found = True
                break
        if not found:
            print("Task not founded")
        write_to_json(tasks, JSON_FILE)

    except IndexError:
        print(f"Usage: {sys.argv[0]} update <ID> 'cook dinner'")

    except ValueError:
        print("The <ID> must be a Integer")


def modify_task_status(status):
    try:
        selected_id = int(sys.argv[2])

        tasks = read_json(JSON_FILE)

        found = False
        for task in tasks:
            if task["id"] == selected_id:
                if status == "done":
                    task["status"] = "done"
                    print(
                        f"{task['description']} - Task done successfully (ID: {task['id']})",
                    )
                elif status == "in-progress":
                    task["status"] = "in-progress"
                    print(
                        f"{task['description']} - Task marked as in-progress (ID: {task['id']})",
                    )
                else:
                    print("status not valid")

                task["updatedAt"] = strftime("%d %b %Y - %H:%M")
                found = True
                break

        if not found:
            print("Task not founded")

        write_to_json(tasks, JSON_FILE)

    except IndexError:
        print(f"Usage: {sys.argv[0]} update <ID> 'cook dinner'")

    except ValueError:
        print("The <ID> must be a Integer")


def formatted_tasks(tasks):
    for task in tasks:
        print(
            f"description: {task['description']}\nid: {task['id']}\nstatus: {task['status']}\n",
        )


def list_command():
    tasks = read_json(JSON_FILE)

    try:
        argument = sys.argv[2]
        match argument:
            case "done":
                done_tasks = [task for task in tasks if task["status"] == argument]
                print("Tasks done: \n")
                formatted_tasks(done_tasks)
            case "todo":
                todo_tasks = [task for task in tasks if task["status"] == argument]
                print("To-do Tasks: \n")
                formatted_tasks(todo_tasks)
            case "in-progress":
                in_progress_tasks = [
                    task for task in tasks if task["status"] == argument
                ]
                print("Tasks in-progress: \n")
                formatted_tasks(in_progress_tasks)
            case _:
                print(f"Usage: {sys.argv[0]} list (todo, in-progress, done)")
    except IndexError:
        print("All Tasks: \n")
        formatted_tasks(tasks)


def main():
    try:
        command = sys.argv[1]
        match command:
            case "add":
                add_command()
            case "update" | "upd":
                update_command()
            case "delete" | "del" | "remove":
                delete_command()
            case "mark-done":
                modify_task_status("done")
            case "mark-in-progress":
                modify_task_status("in-progress")
            case "list":
                list_command()
            case "help" | "--help" | "-h":
                help_command()
            case _:
                return help_command()

    except IndexError:
        help_command()


if __name__ == "__main__":
    main()
