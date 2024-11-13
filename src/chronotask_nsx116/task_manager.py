from terminaltables import AsciiTable
from appdirs import user_data_dir
import os
import pickle
import textwrap
from chronotask_nsx116.task import Task
from chronotask_nsx116.focustrack import FocusTrack 
from chronotask_nsx116.settings import Settings

class TaskManager:
    def __init__(self):
        self.settings = Settings()
        self.data_dir = self.settings.data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        self.sorted_ids = {}  # Dictionary to store tasks by their global ID
        self.tasks = {}  # Dictionary to store tasks by their global ID
        self.tasks_file = self.settings.tasks_file
        self.sorted_ids_file = self.settings.sorted_ids_file
        self.global_id_file = self.settings.global_id_file
        self.global_id = self.load_global_id()
        self.load_tasks()  # Load tasks from file on initialization
        self.load_sorted_ids() 
        self.timer = FocusTrack()
        

    # Add a new task
    def add_task(self, text, due_date=None, project=None, tag=None, value=None):
        global_id = self.global_id
        task = Task(text, due_date, project, tag, value, global_id) 
        self.tasks[task.global_id] = task
        self.global_id +=1
        self.save_global_id()
        self.save_tasks()  # Save changes to file
        print(task)
        return task

    def get_global_id_by_current_id(self, task_id):
        print(self.sorted_ids)
        for current_id, global_id in self.sorted_ids.items():
            if current_id == task_id:
                return global_id 
        return None  

    def mark_task_done(self, current_id):
        task_id = self.get_global_id_by_current_id(current_id)
        task = self.tasks.get(task_id)
        if task:
            task.mark_done()
            self.save_tasks()  # Save changes to file
            self.save_sorted_ids()
        else:
            print(f"Task with ID {task_id} not found.")

    # Mark a task as active by task ID
    def mark_task_active(self, current_id):
        task_id = self.get_global_id_by_current_id(current_id)
        task = self.tasks.get(task_id)
        if task:
            task.mark_active()
            self.save_tasks()  # Save changes to file
            self.save_sorted_ids()
        else:
            print(f"Task with ID {task_id} not found.")

    # Dismiss a task by task ID
    def dismiss_task(self, current_id):
        task_id = self.get_global_id_by_current_id(current_id)
        task = self.tasks.get(task_id)
        if task:
            task.dismiss()
            self.save_tasks()  # Save changes to file
            self.save_sorted_ids()
        else:
            print(f"Task with ID {task_id} not found.")
    
    # Delete a task by task ID
    def delete_task(self, current_id):
        task_id = self.get_global_id_by_current_id(current_id)
        task = self.tasks.pop(task_id, None)  # Remove task from dictionary
        if task:
            self.save_tasks()  # Save changes to file
            print(f"Task {task_id} permanently deleted.")
            self.save_sorted_ids()
        else:
            print(f"Task with ID {task_id} not found.")
    
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

    def start_task(self, current_id):
        self.timer.start(current_id)
        # print(current_id)

    # Printing tasks neatly 
    def print_tasks(self):
        table_data = [['ID', '[*]', 'Text', 'Created', 'Due Date', 'Total work,\nhours']]
        for current_id, global_id in self.sorted_ids.items():
            task = self.tasks[global_id]
            if task.status == "active":
                checkbox = "[ ]"
            elif task.status == "done":
                checkbox = "[x]"
            elif task.status == "dismissed":
                checkbox = "[-]"
            else:
                checkbox = "[?]"  # For any unknown status
            wrapped_lines = textwrap.wrap(task.text, width=39)
            padded_lines = [line.ljust(35) for line in wrapped_lines]
            task_text_wrapped = "\n".join(padded_lines)
            date_added = task.date_added.strftime("%Y-%m-%d")
            total_work_hours = round(task.total_work / 60, 1)
            table_data.append([current_id, checkbox, task_text_wrapped, date_added, task.due_date, total_work_hours])
        table = AsciiTable(table_data)
        print(table.table)

    # List all tasks, with optional status filtering
    def list_tasks(self, status):
        # Reverse tasks order so items in table list from recents to olders
        reversed_tasks = dict(reversed(self.tasks.items())) 
        current_id = 1  # Initialize current_id sequence
        self.sorted_ids = {} 
        if not self.tasks:
            print("No tasks available.")
            return

        if status and "all" in status:  # Adjust to check if 'all' is in the status list
            print("All in status")
            for global_id, task in reversed_tasks.items():
                self.sorted_ids[current_id] = global_id
                current_id += 1  # Increment current_id for the next blue task
            if self.sorted_ids:
                self.print_tasks()
            self.save_sorted_ids()

        elif status:
            print("done, dismissed, active in status")
            valid_statuses = {"done", "dismissed", "active"}
            for global_id, task in reversed_tasks.items():
                if task.status in status:  # Check if the color is blue
                    self.sorted_ids[current_id] = task.global_id
                    current_id += 1  # Increment current_id for the next blue task
            if self.sorted_ids:
                self.print_tasks()
            else:
                print(f"No tasks with statuses: {', '.join(status)}")
            self.save_sorted_ids()

        else:
            print("Without status")
            for global_id, task in reversed_tasks.items():
                if task.status == "active":
                    self.sorted_ids[current_id] = task.global_id
                    current_id += 1  # Increment current_id for the next blue task
            if self.sorted_ids:
                self.print_tasks()
            else:
                    print("No tasks with status: active")
            self.save_sorted_ids()

    # Save tasks to a file (JSON format)
    def save_tasks(self):
        with open(self.tasks_file, 'wb') as file:
            pickle.dump(self.tasks, file)
        print(f"Tasks saved to {self.tasks_file}")
    
    # Load tasks from a file
    def load_tasks(self):
        try:
            with open(self.tasks_file, 'rb') as f:
                self.tasks = pickle.load(f)
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

