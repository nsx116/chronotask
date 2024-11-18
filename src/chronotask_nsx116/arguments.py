import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Add, list, id, delete")

    # Create a subparser for the main commands (task, note, recurrent, leak)
    subparsers = parser.add_subparsers(dest="action", help="Add, list, id)")

    # -------------------- TASK COMMAND --------------------
    # task_parser = subparsers.add_parser("task", help="Manage tasks")
    # task_subparsers = task_parser.add_subparsers(dest="action", help="Task actions")

    # 'add' command for tasks
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("text", help="Task description text")
    add_parser.add_argument("--date", help="Due date for the task (format: YYYY-MM-DD)")
    add_parser.add_argument("--project", help="Project name")
    add_parser.add_argument("--tag", help="Tag")
    add_parser.add_argument("--val", help="Value or priority")

    # 'list' command for tasks
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument('--status', nargs='*', choices=['all', 'active', 'done', 'dismissed'], help='List active tasks')

    # Subparser for task-specific actions based on task ID
    id_parser = subparsers.add_parser("id", help="Actions for a specific task")
    id_parser.add_argument("task_id", type=int, help="ID of the task to operate on")
    id_subparsers = id_parser.add_subparsers(dest="task_action", help="Task-specific actions")

    # Task-specific actions: 'done', 'dismiss', 'mod', 'delete'
    id_subparsers.add_parser("done", help="Mark task as done")
    id_subparsers.add_parser("dismiss", help="Dismiss the task")
    id_subparsers.add_parser("active", help="Mark task as active")
    
    mod_parser = id_subparsers.add_parser("mod", help="Modify a task")
    mod_parser.add_argument("--text", help="New task description")
    mod_parser.add_argument("--date", help="New due date")
    mod_parser.add_argument("--project", help="New project")
    mod_parser.add_argument("--tag", help="New tag")
    mod_parser.add_argument("--value", type=int, help="New value or priority")

    id_subparsers.add_parser("delete", help="Delete a task")
    id_subparsers.add_parser("start", help="Start a task")
    
    # Set pomodoro-timer settings
    set_parser = subparsers.add_parser("set", help="Set pomodoro-timer settings")
    set_parser.add_argument("--work", help="Work duration in minutes")
    set_parser.add_argument("--short-rest", help="Short rest duration in minutes")
    set_parser.add_argument("--long-rest", help="Long rest duration in minutes")
    set_parser.add_argument("--pomodoros", help="Pomodoros count before long rest")
    set_parser.add_argument("--inactivity", help="Inactivity duration in seconds to stop activity timer")

    return parser.parse_args()

# Commands
def handle_add(manager, args):
    # Handle the 'add' action to add a new task
    manager.add_task(args.text, args.date, args.project, args.tag, args.val)
    print(f"handle.add task added: {args.text}")

def handle_list(manager, args):
    # Handle task-specific actions based on task ID.
    manager.list_tasks(args.status)       

def handle_id_action(manager, args):
    # Handle task-specific actions based on task ID.
    if args.task_action == "done":
        manager.mark_task_done(args.task_id)
        print(f"Marking task {args.task_id} as done")
    elif args.task_action == "dismiss":
        manager.dismiss_task(args.task_id)
        print(f"Dismissing task {args.task_id}")
    elif args.task_action == "active":
        manager.mark_task_active(args.task_id)
        print(f"Marking task {args.task_id} active")
    elif args.task_action == "mod":
        manager.modify_task(
            args.task_id,
            text=args.text,
            due_date=args.date,
            project=args.project,
            tag=args.tag,
            value=args.value
            )              
        print(f"Modifying task {args.task_id}")
    elif args.task_action == "delete":
        manager.delete_task(args.task_id)
        print(f"Deleting task {args.task_id}")
    elif args.task_action == "start":
        print(f"Starting task {args.task_id}")
        manager.start_task(args.task_id)

def handle_set(manager, args):
    # Convert argument values to integers if they are provided, otherwise leave as None
    manager.set_settings(
        work=int(args.work) if args.work else None,
        short_rest=int(args.short_rest) if args.short_rest else None,
        long_rest=int(args.long_rest) if args.long_rest else None,
        pomodoros=int(args.pomodoros) if args.pomodoros else None,
        inactivity=int(args.inactivity) if args.inactivity else None,
    )
"""
def handle_set(manager, args):
    # Convert argument values to integers if they are provided, otherwise leave as None
    manager.set_settings(
        work=args.work,
        short_rest=args.short_rest,
        long_rest=args.long_rest,
        pomodoros=args.pomodoros,
        inactivity=args.inactivity,
    )
"""
