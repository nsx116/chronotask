from chronotask_nsx116.task_manager import TaskManager  
from chronotask_nsx116.arguments import parse_args
from chronotask_nsx116.arguments import handle_add
from chronotask_nsx116.arguments import handle_list
from chronotask_nsx116.arguments import handle_id_command
from chronotask_nsx116.arguments import handle_set
from chronotask_nsx116.arguments import handle_stats

def main():
    args = parse_args()
    manager = TaskManager()


    # TASK handling
    if args.command == "add":
        handle_add(manager, args)
    elif args.command == "list":
        handle_list(manager, args)
    elif args.command == "id":
        handle_id_command(manager, args)
    elif args.command == "set":
        handle_set(manager, args)
    elif args.command == "stats":
        handle_stats(manager, args)

if __name__ == "__main__":
    main()
