from appdirs import user_data_dir
import os

class Settings:
    def __init__(self):
        # Timer settings
        self.work_duration = 5     # Default 25 minutes
        self.short_rest_duration = 5   # Default 5 minutes
        self.long_rest_duration = 15  # Default 15 minutes
        self.pomodoros_before_long_rest = 4  # Default 4 Pomodoros before a long rest
        self.inactivity_limit = 90  # Default inactivity time (60 seconds for testing)

        # Files
        self.app_name = "chronotask_nsx116"
        self.data_file_short = "data.json"
        self.sorted_ids_file_short = "sorted_ids.pkl"
        self.global_id_file_short = "global_id.txt"
        self.pomodoro_summary_short = "pomodoro_summary.txt"

        self.data_dir = user_data_dir(self.app_name)
        self.data_file = os.path.join(self.data_dir, self.data_file_short)
        self.sorted_ids_file = os.path.join(self.data_dir, self.sorted_ids_file_short)
        self.global_id_file = os.path.join(self.data_dir, self.global_id_file_short)
        self.pomodoro_summary_file = os.path.join(self.data_dir, self.pomodoro_summary_short)
