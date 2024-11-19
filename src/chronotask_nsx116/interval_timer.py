import os
# Hides Pygame's greeting message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time
import subprocess
from chronotask_nsx116.writing_to_task import write_total_activity_to_task
from chronotask_nsx116.settings import Settings, Files
import chronotask_nsx116.data
import importlib.resources

class IntervalTimer:
    def __init__(self, pomodoro_timer):  
        pygame.mixer.init()
        self.timer = pomodoro_timer
        self.files = Files()
        self.activity_duration = 0 # Activity since start  
        self.rest_duration = 0     # Rest pause duration
        self.pomodoro_count = 0
        self.pomodoro_finish = False
        self.total_work_minutes = 0
        self.total_rest_minutes = 0
        self.short_rest = False
        self.short_rest_start = False
        self.short_rest_finish = False
        self.resting_for_minute = False
        self.long_rest = False
        self.long_rest_start = False
        self.long_rest_finish = False
        self.active_for_minute = False
        self.settings = pomodoro_timer.settings
        with importlib.resources.as_file(importlib.resources.files(chronotask_nsx116.data) / 'notification.wav') as path:
            self.notification_sound = str(path)  # Convert to string if needed by your code
            print(f"Notification sound located at: {self.notification_sound}")
        self.pomodoro_summary = self.files.pomodoro_summary_file

    def run(self, current_id):
        self.update_activity_timer()
        self.registrator(current_id)
        time.sleep(1)

    def update_activity_timer(self):
        """Continuously updates the activity timer and logs every minute."""
        if self.timer.working:
            if not self.timer.activity_timer_pause:
                self.activity_duration += 1
                if self.activity_duration >= self.settings.work_duration:
                    self.pomodoro_count += 1
                    self.pomodoro_finish = True
                    # Handle break logic
                    if self.pomodoro_count % self.settings.pomodoros_before_long_rest == 0:
                        self.long_rest = True
                        self.long_rest_start = True
                        self.change_to_rest()
                    else:
                        self.short_rest = True
                        self.short_rest_start = True
                        self.change_to_rest()
                if self.activity_duration % 60 == 0:  # Log every 1 minute
                    self.total_work_minutes += 1
                    if 0 < self.activity_duration < self.settings.work_duration:
                        self.active_for_minute = True
        else:
            self.rest_duration += 1
            if self.short_rest:
                if self.rest_duration >= self.settings.short_rest_duration:
                    self.short_rest_finish = True
                    self.change_to_work()
            elif self.long_rest:
                if self.rest_duration >= self.settings.long_rest_duration:
                    self.long_rest_finish = True
                    self.change_to_work()
            if self.rest_duration % 60 == 0:
                self.total_rest_minutes += 1
                if 0 < self.rest_duration < self.settings.long_rest_duration:
                    self.resting_for_minute = True

    def registrator(self, current_id):
        if self.pomodoro_finish: 
            message = f"Pomodoro #{self.pomodoro_count} complete! Time for a break."
            self.send_notification(message)
            write_total_activity_to_task(self.files.data_file, current_id, self.settings)
            self.pomodoro_finish = False
        if self.long_rest_start:
            message = f"Long rest for {self.settings.long_rest_duration // 60} minutes."
            print(message)
            self.long_rest_start = False
        if self.long_rest_finish:
            message = "Short rest finished! Time for a work."
            self.send_notification(message)
            self.long_rest_finish = False
        if self.short_rest_start:
            message = f"Short rest for {self.settings.short_rest_duration // 60} minutes."
            print(message)
            self.short_rest_start = False
        if self.short_rest_finish:
            message = "Short rest finished! Time for a work."
            self.send_notification(message)
            self.short_rest_finish = False
        if self.active_for_minute:
            print(f"Active for {self.total_work_minutes} minute(s).")
            self.active_for_minute = False
        if self.resting_for_minute:
            print(f"Resting for {self.rest_duration // 60} minute(s).")
            self.resting_for_minute = False


    def send_notification(self, message):
        print(message)
        subprocess.run(['notify-send', "Pomodoro timer", message])
        try:
            pygame.mixer.music.load(self.notification_sound)
            pygame.mixer.music.play()
            print("Notification sound played.")
        except pygame.error as e:
            print(f"Failed to play sound: {e}")

    def change_to_rest(self):
        """Resets the timer for the next Pomodoro session."""
        self.timer.working = False
        self.activity_timer_pause = True
        self.activity_duration = 0
        self.rest_duration = 0

    def change_to_work(self):
        """Resets the timer for the next Pomodoro session."""
        self.timer.working = True
        self.short_rest = False
        self.long_rest = False
        self.timer.activity_timer_pause = False
        self.activity_duration = 0
        self.rest_duration = 0
        self.timer.last_activity_time = time.time()
        
