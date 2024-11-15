from terminaltables import AsciiTable
from appdirs import user_data_dir
from pathlib import Path
from datetime import date, datetime
from collections import defaultdict
import os
import json
import textwrap
import uuid
from chronotask_nsx116.focustrack import FocusTrack 
from chronotask_nsx116.settings import Settings
from chronotask_nsx116.writing_to_task import load_data, save_data

class TaskManager:
    def __init__(self):
        self.settings = Settings()
        self.data_dir = self.settings.data_dir
        self.data_file = self.settings.data_file
        os.makedirs(self.data_dir, exist_ok=True)
        # self.data = {} # newly added
        # self.sorted_ids = {} # newly added
        # self.data = self.load_data(self.data_file)
        # self.data = self.load_data(getattr(self, 'data_file', None) or 'data.json')
        self.data = load_data(self.data_file)
        self.sorted_ids = self.data.get("sorted_ids", {})
        # self.sorted_ids = self.data["sorted_ids"] if self.data["sorted_ids"] else {}  # Dictionary to store tasks by their global ID
        self.tasks = self.data.get("tasks", [])  # Dictionary to store tasks by their global ID
        # self.tasks_file = self.settings.tasks_file
        # self.sorted_ids_file = self.settings.sorted_ids_file
        # self.global_id_file = self.settings.global_id_file
        # self.global_id = self.load_global_id()
        # self.load_tasks()  # Load tasks from file on initialization
        # self.load_sorted_ids() 
        self.timer = FocusTrack()


    # Add a new task
    def add_task(self, text, due_date=None, project=None, tag=None, value=None):
        task = {}
        task["text"] = text
        task["date"] = due_date if due_date else date.today().strftime("%Y-%m-%d")  # Default is today if not provided
        task["project"] = project
        task["tag"] = tag
        task["value"] = value
        task["global_id"] = str(uuid.uuid4()) 

        # Task lifecycle attributes
        task["date_added"] = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        task["date_done"] = None
        task["date_dismissed"] = None
        task["status"] = "active"  # Can be "active", "done", or "dismissed"
        task["total_work"] = 0
        task["history"] = {}
        self.data["tasks"].append(task)
        print(self.tasks)
        save_data(self.data_file, self.data)

    def get_global_id_by_current_id(self, task_id):
        # print(self.sorted_ids)
        for current_id, global_id in self.sorted_ids.items():
            if current_id == task_id:
                return global_id 
        # - [ ]
        return None  

    def mark_task_done(self, current_id):
        task_id = self.get_global_id_by_current_id(current_id)
        task = None  # Initialize task as None
        # Iterate through the list of tasks to find the one with the matching global_id
        for item in self.tasks:
            if task_id == item.get("global_id"):
                task = item  # Found the task
                break  # Exit loop once the task is found
        if task:
            task["status"] = "done"
            save_data(self.data_file, self.data)  # Save changes to file
            print(f"Task with ID {task_id} has been marked as done.")
        else:
            print(f"Task with ID {task_id} not found.")

    def mark_task_active(self, current_id):
        task_id = self.get_global_id_by_current_id(current_id)
        task = None  # Initialize task as None
        # Iterate through the list of tasks to find the one with the matching global_id
        for item in self.tasks:
            if task_id == item.get("global_id"):
                task = item  # Found the task
                break  # Exit loop once the task is found
        if task:
            task["status"] = "active"
            save_data(self.data_file, self.data)  # Save changes to file
            print(f"Task with ID {task_id} has been marked as active.")
        else:
            print(f"Task with ID {task_id} not found.")

    # Dismiss a task by task ID
    def dismiss_task(self, current_id):
        task_id = self.get_global_id_by_current_id(current_id)
        task = None  # Initialize task as None
        # Iterate through the list of tasks to find the one with the matching global_id
        for item in self.tasks:
            if task_id == item.get("global_id"):
                task = item  # Found the task
                break  # Exit loop once the task is found
        if task:
            task["status"] = "dismissed"
            save_data(self.data_file, self.data)  # Save changes to file
            print(f"Task with ID {task_id} has been dismissed.")
        else:
            print(f"Task with ID {task_id} not found.")

    # Delete a task by task ID
    def delete_task(self, current_id):
        task_id = self.get_global_id_by_current_id(current_id)
        task_found = False  # Track if the task was found and deleted
        # Iterate over self.tasks to find and remove the task with the matching global_id
        for i, item in enumerate(self.tasks):
            if item.get("global_id") == task_id:
                del self.tasks[i]  # Delete the task from the list
                task_found = True
                save_data(self.data_file, self.data)  # Save changes to file
                print(f"Task with ID {task_id} has been deleted.")
                break  # Exit loop after deleting the task
        if not task_found:
            print(f"Task with ID {task_id} not found.")

    """
    # Modify a task by task ID
    def modify_task(self, current_id, **kwargs):
        task_id = self.get_global_id_by_current_id(current_id)
        task = self.tasks.get(task_id)
        if task:
            task.modify(**kwargs)
            print(task)
            self.save_tasks()  # Save changes to file
            self.save_sorted_ids()
        else:
            print(f"Task with ID {task_id} not found.")
    """
    def start_task(self, current_id):
        self.timer.start(current_id)
        print(current_id)

    # Printing tasks neatly 
    def print_tasks(self):
        table_data = [['ID', '[*]', 'Text', 'Created', 'Due Date', 'Total work,\nhours']]
        for current_id, global_id in self.sorted_ids.items():
            for item in self.tasks:
                if global_id == item.get("global_id"):
                    task = item
                    break
            if task["status"] == "active":
                checkbox = "[ ]"
            elif task["status"] == "done":
                checkbox = "[x]"
            elif task["status"] == "dismissed":
                checkbox = "[-]"
            else:
                checkbox = "[?]"  # For any unknown status
            wrapped_lines = textwrap.wrap(task["text"], width=39)
            padded_lines = [line.ljust(35) for line in wrapped_lines]
            task_text_wrapped = "\n".join(padded_lines)
            date_added = task["date_added"]
            total_work_hours = round(task["total_work"] / 60, 1)
            table_data.append([current_id, checkbox, task_text_wrapped, date_added, task["date"], total_work_hours])
        table = AsciiTable(table_data)
        print(table.table)

    # List all tasks, with optional status filtering
    def list_tasks(self, status):
        # Reverse tasks order so items in table list from recents to olders
        reversed_tasks = reversed(self.tasks) 
        current_id = 1  # Initialize current_id sequence
        self.sorted_ids = {} 
        if not self.tasks:
            print("No tasks available.")
            return

        if status and "all" in status:  # Adjust to check if 'all' is in the status list
            print("All in status")
            for item in reversed_tasks:
                self.sorted_ids[current_id] = item["global_id"]
                current_id += 1  # Increment current_id for the next task
            if self.sorted_ids:
                self.print_tasks()
            save_data(self.data_file, self.data)

        elif status:
            print("done, dismissed, active in status")
            valid_statuses = {"done", "dismissed", "active"}
            for item in reversed_tasks:
                if item["status"] in status:  # Check if the color is blue
                    self.sorted_ids[current_id] = item["global_id"]
                    current_id += 1  # Increment current_id for the next blue task
            if self.sorted_ids:
                self.print_tasks()
            else:
                print(f"No tasks with statuses: {', '.join(status)}")
            save_data(self.data_file, self.data)

        else:
            print("Without status")
            for item in reversed_tasks:
                if item["status"] == "active":
                    self.sorted_ids[current_id] = item["global_id"]
                    current_id += 1  # Increment current_id for the next blue task
            if self.sorted_ids:
                self.print_tasks()
            else:
                    print("No tasks with status: active")
            save_data(self.data_file, self.data)

    
