import argparse
from datetime import datetime


def parse_args():
    parser = argparse.ArgumentParser(
        description="A task management and pomodoro timer app.",
        epilog=(
            "Examples:\n"
            "  chronotask add 'Complete project report' --date 2024-11-15 --project Work --tag Important\n"
            "  chronotask list --status active done\n"
            "  chronotask id 3 done\n"
            "  chronotask set --work=25 --short-rest=5 --long-rest=15 --pomodoros=4 --inactivity=90\n"
            "  chronotask stats 2024-11\n"
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )

    # Create a subparser for main commands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    subparsers.required = True  # Ensure a command is provided

    # -------------------- TASK COMMANDS --------------------
    # Add a new task
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("text", help="Task description text")
    add_parser.add_argument("--date", help="Due date for the task (format: YYYY-MM-DD)")
    add_parser.add_argument("--project", help="Project name")
    add_parser.add_argument("--tag", help="Tag")
    add_parser.add_argument("--val", help="Value or priority")

    # List tasks
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument(
        '--status',
        nargs='*',
        choices=['all', 'active', 'done', 'dismissed'],
        help="Task status to filter by (default: active)"
    )

    # Actions for a specific task by ID
    id_parser = subparsers.add_parser("id", help="Actions for a specific task")
    id_parser.add_argument("task_id", type=int, help="ID of the task to operate on")
    id_subparsers = id_parser.add_subparsers(dest="task_action", help="Actions for the task")
    id_subparsers.required = True

    # Task-specific actions
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

    # -------------------- POMODORO TIMER SETTINGS --------------------
    set_parser = subparsers.add_parser("set", help="Set pomodoro-timer settings, without arguments prints current settings")
    set_parser.add_argument("--work", type=int, help="Work duration in minutes")
    set_parser.add_argument("--short-rest", type=int, help="Short rest duration in minutes")
    set_parser.add_argument("--long-rest", type=int, help="Long rest duration in minutes")
    set_parser.add_argument("--pomodoros", type=int, help="Pomodoros count before long rest")
    set_parser.add_argument("--inactivity", type=int, help="Inactivity duration in seconds to stop activity timer")

    # -------------------- STATISTICS --------------------
    stats_parser = subparsers.add_parser("stats", help="Display monthly statistics")
    stats_parser.add_argument(
        "year_month",
        nargs="?",
        default=None,
        help="Year and month for statistics (format: YYYY-MM). Defaults to \
        current month if not provided"
    )

    return parser.parse_args()


# Commands
def handle_add(manager, args):
    # Handle the 'add' action to add a new task
    manager.add_task(args.text, args.date, args.project, args.tag, args.val)
    print("Task has been added.")

def handle_list(manager, args):
    # Handle task-specific actions based on task ID. Commented lines is for
    # show statistics for current month wiht list command
    # now = datetime.now()
    # year, month = now.year, now.month
    # manager.stats(year, month)
    manager.list_tasks(args.status)       

def handle_id_command(manager, args):
    # Handle task-specific actions based on task ID.
    if args.task_action == "done":
        manager.mark_task_done(args.task_id)
        # print(f"Marking task {args.task_id} as done")
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
        # print(f"Deleting task {args.task_id}")
    elif args.task_action == "start":
        print(f"Starting task {args.task_id} at {datetime.now().strftime('%Y-%m-%d %H:%M')}")
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

def handle_stats(manager, args):
    try:
        if args.year_month is None:
            now = datetime.now()
            year, month = now.year, now.month
        else:
            year, month = map(int, args.year_month.split("-"))
        manager.stats(year, month)
    except ValueError:
        print("Invalid format for year and month. Please use YYYY-MM (e.g., 2024-10).")
