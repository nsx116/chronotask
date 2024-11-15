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
        self.data = self.load_data()
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

    def load_data(self):
        path = Path(self.data_file)
        if path.exists():
            contents = path.read_text()
            data = json.loads(contents)
            return data
        else:
            return defaultdict(dict, {"tasks": []})

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
        self.save_data()

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
            self.save_data()  # Save changes to file
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
            self.save_data()  # Save changes to file
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
            self.save_data()  # Save changes to file
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
                self.save_data()  # Save changes to file
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
            self.save_data()

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
            self.save_data()

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
            self.save_data()

    # Save tasks to a file (JSON format)
    def save_data(self):
        with open(self.data_file, 'w') as file:
            json.dump(self.data, file, indent=4)
        print(f"Tasks saved to {self.data_file}")
    
    # In your class initialization or where you set `self.data`
    
    """    
    def load_data(self, data_file):
        try:
            path = Path(data_file)
            contents = path.read_text()
            data = json.loads(contents)
            return data
        except FileNotFoundError:
            print("No existing task file found. Starting with an empty task list.")

    # Load tasks from a file
    def load_tasks(self):
        try:
            with open(self.data_file, 'r') as f:
                self.data = json.load(f)
            print(f"Tasks loaded from {self.tasks_file}")
        except FileNotFoundError:
            print("No existing task file found. Starting with an empty task list.")

    # Load global ID to file
    def load_global_id(self):
            try:
                with open(self.global_id_file, 'r') as f:
                    return int(f.read())
            except FileNotFoundError:
                return 1  # Start at ID 1 if no file is found

    # Save global ID to file
    def save_global_id(self):
        with open(self.global_id_file, 'w') as f:
            f.write(str(self.global_id))

    # Save tasks to a file (JSON format)
    def save_sorted_ids(self):
        with open(self.sorted_ids_file, 'wb') as file:
            pickle.dump(self.sorted_ids, file)
        print(f"Tasks saved to {self.sorted_ids_file}")
    
    # Load tasks from a file
    def load_sorted_ids(self):
        try:
            with open(self.sorted_ids_file, 'rb') as f:
                self.sorted_ids = pickle.load(f)
            print(f"Tasks loaded from {self.sorted_ids_file}")
        except FileNotFoundError:
            print(f"No existing {self.sorted_ids_file} file found.")
    """
