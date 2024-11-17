# import pickle
from chronotask_nsx116.settings import Settings, Files
import json
from pathlib import Path
from collections import defaultdict


def write_total_activity_to_task(data_file, current_id):
    settings = Settings()
    files = Files()
    data = load_data(data_file)
    tasks = data.get("tasks")  
    sorted_ids = data.get("sorted_ids")
    task_id = get_global_id_by_current_id(current_id, sorted_ids)
    if tasks:
        for item in tasks:
            if task_id == item.get("global_id"):
                task = item
                break
        if task:
            task["total_work"] += settings.work_duration / 60
        else:
            print(f"Task with ID {task_id} not found.")
    save_data(data_file, data)


def get_global_id_by_current_id(task_id, sorted_ids):
    task_id = str(task_id)
    for current_id, global_id in sorted_ids.items():
        if task_id == current_id:
            return global_id 
        else:
            print(f"No task with {task_id} found")

def write_past_minutes_when_quit(current_id, activity_duration):
    settings = Settings()
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


def save_data(data_file, data):
    with open(data_file, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Tasks saved to {data_file}")
    

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
def save_objects_dictionary(objects_dictionary, objects_file):
    with open(objects_file, 'wb') as f:
        pickle.dump(objects_dictionary, f)
    print(f"Dictionary saved to {objects_file}")


def load_objects_dictionary(objects_file):
    try:
        with open(objects_file, 'rb') as f:
            objects_dictionary = pickle.load(f)
        print(f"Dictionary loaded from {objects_file}")
        return objects_dictionary
    except FileNotFoundError:
        print("No existing task file found. Starting with an empty task list.")
"""
