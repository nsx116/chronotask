from appdirs import user_data_dir
import os

class Settings:
    def __init__(self, work_duration=25 * 60, short_rest_duration=5 * 60, long_rest_duration=15 * 60, 
                 pomodoros_before_long_rest=4, inactivity_limit=90):
        self.work_duration = work_duration        
        self.short_rest_duration = short_rest_duration        
        self.long_rest_duration = long_rest_duration        
        self.pomodoros_before_long_rest = pomodoros_before_long_rest        
        self.inactivity_limit = inactivity_limit  

    @classmethod
    def from_dict(cls, data):
        return cls(
            work_duration = data.get("work_duration", 25 * 60),     
            short_rest_duration = data.get("short_rest_duration", 5 * 60), 
            long_rest_duration = data.get("long_rest_duration", 15 * 60), 
            pomodoros_before_long_rest = data.get("pomodoros_before_long_rest", 4),  
            inactivity_limit = data.get("inactivity_limit", 90),  
            )

    def to_dict(self):
        return {
                "work_duration": self.work_duration,      
                "short_rest_duration": self.short_rest_duration, 
                "long_rest_duration": self.long_rest_duration, 
                "pomodoros_before_long_rest": self.pomodoros_before_long_rest,
                "inactivity_limit": self.inactivity_limit, 
                }


class Files:
    def __init__(self):
        self.app_name = "chronotask_nsx116"
        self.data_file_short = "data.json"
        self.pomodoro_summary_short = "pomodoro_summary.txt"

        self.data_dir = user_data_dir(self.app_name)
        self.data_file = os.path.join(self.data_dir, self.data_file_short)
        self.pomodoro_summary_file = os.path.join(self.data_dir, self.pomodoro_summary_short)
