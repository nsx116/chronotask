from chronotask_nsx116.settings import Settings, Files
from datetime import datetime
import json
from pathlib import Path
from collections import defaultdict


def write_total_activity_to_task(data_file, global_id, settings):
    #settings = Settings()
    # files = Files()
    data = load_data(data_file)
    tasks = data.get("tasks")  
    sorted_ids = data.get("sorted_ids")
    task_id = str(global_id)
    if tasks:
        for item in tasks:
            if task_id == item.get("global_id"):
                task = item
                break
        if task:
            task["total_work"] += round(settings.work_duration / 60, 1)
        else:
            print(f"Task with ID {task_id} not found.")
    save_data(data_file, data)


def get_global_id_by_current_id(task_id, sorted_ids):
    task_id = str(task_id)
    found = False                                   # added line
    for current_id, global_id in sorted_ids.items():
        if task_id == current_id:
            return global_id 
    if not found:
            print(f"No task with {task_id} found")
    return None                                       # added line
        #else:
        #    print(f"No task with {task_id} found")

def write_past_minutes_when_quit(global_id, activity_duration, 
                                 work_started_at, total_work_minutes):
    files = Files()
    data = load_data(files.data_file)
    tasks = data.get("tasks", [])
    sorted_ids = data.get("sorted_ids", {})
    
    # Get the task's global ID
    task_id = global_id
    
    if not tasks:
        print("No tasks available.")
        return
    
    # Locate the task by its global ID
    task = next((item for item in tasks if item.get("global_id") == task_id), None)
    
    if not task:
        print(f"Task with ID {task_id} not found.")
        return
    
    # Get today's date as a string
    today = datetime.now().strftime("%Y-%m-%d")
    task["total_work"] += round(activity_duration / 60, 1)
    
    # Initialize history for today if it doesn't exist
    if "history" not in task:
        task["history"] = {}
    if today not in task["history"]:
        task["history"][today] = []
    
    # Add the new work session to the task's history
    task["history"][today].append({
        "work_started_at": work_started_at, 
        "work_stopped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
        "minutes": total_work_minutes,
    })
    
    # Save the updated data back to the file
    save_data(files.data_file, data)
    print(f"Updated task {task_id} with work session on {today}.")


def save_data(data_file, data):
    with open(data_file, 'w') as file:
        json.dump(data, file, indent=4)
    # print(f"Tasks saved to {data_file}")
    

def load_data(data_file):
    path = Path(data_file)
    if path.exists():
        contents = path.read_text()
        data = json.loads(contents)
        return data
    else:
        return defaultdict(dict, {"settings": {},
                                  "sorted_ids": {},
                                  "tasks": []})
        # return defaultdict(dict, {"tasks": []})

"""
def write_past_minutes_when_quit(current_id, activity_duration):
    files = Files()
    data = load_data(files.data_file)
    tasks = data.get("tasks")  
    sorted_ids = data.get("sorted_ids")
    task_id = get_global_id_by_current_id(current_id, sorted_ids)
    if tasks:
        for item in tasks:
            if task_id == item.get("global_id"):
                task = item
                break
        if task:
            task["total_work"] += activity_duration / 60
        else:
            print(f"Task with ID {task_id} not found.")
    save_data(files.data_file, data)
"""
