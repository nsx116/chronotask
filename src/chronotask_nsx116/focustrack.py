from datetime import datetime
from pynput import mouse, keyboard
import time
import threading
from chronotask_nsx116.interval_timer import IntervalTimer
from chronotask_nsx116.settings import Settings


class FocusTrack:
    def __init__(self):
        self.settings = Settings()
        self.last_activity_time = time.time()
        self.stop_timer = False
        self.working = True
        self.activity_timer_pause = False
        self.pomodoro_summary = self.settings.pomodoro_summary_file
        self.interval_timer = IntervalTimer(self)

    def reset_activity_timer(self):
        """Resets the last activity time when there is user activity."""
        self.last_activity_time = time.time()

    def check_inactivity(self):
        """Checks for inactivity and pauses the timer if no activity is detected for inactivity_limit seconds."""
        while not self.stop_timer:
            if self.working:
                if time.time() - self.last_activity_time > self.settings.inactivity_limit:  # Inactivity period
                    if not self.activity_timer_pause:
                        print(f"No activity for {self.settings.inactivity_limit} seconds, pausing timer {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                        self.activity_timer_pause = True  # Pause the activity timer
            time.sleep(1)  # Check every second

    def update_activity_timer(self, current_id):
        """Continuously updates the activity timer and logs every minute."""
        while not self.stop_timer:
            self.interval_timer.run(current_id)

    def on_mouse_move(self, x, y):
        """Handler for mouse movement activity."""
        self.reset_activity_timer()
        if self.activity_timer_pause and self.working:  # If timer is paused, resume it
            print(f"Resuming timer due to mouse activity.{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            self.activity_timer_pause = False

    def on_keyboard_event(self, key):
        """Handler for keyboard activity."""
        self.reset_activity_timer()
        if self.activity_timer_pause and self.working:  # If timer is paused, resume it
            print(f"Resuming timer due to keyboard activity {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            self.activity_timer_pause = False

    def start(self, current_id):
        """Starts the timer, inactivity checker, and sets up activity listeners."""

        def write_starting_time_to_file():
            with open(self.pomodoro_summary, 'a') as f:
                f.write(f"Work started at:  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        write_starting_time_to_file()
        self.activity_timer_pause = False  # Start the timer immediately

        # Set up mouse and keyboard listeners
        mouse_listener = mouse.Listener(on_move=self.on_mouse_move)
        keyboard_listener = keyboard.Listener(on_press=self.on_keyboard_event)

        mouse_listener.start()
        keyboard_listener.start()

        # Start the inactivity checker thread
        inactivity_thread = threading.Thread(target=self.check_inactivity)
        inactivity_thread.start()

        # Start the activity timer thread (no recursion, just a loop)
        activity_timer_thread = threading.Thread(target=self.update_activity_timer, args=(current_id,))
        activity_timer_thread.start()

        # Start the thread that waits for user input to quit
        quit_thread = threading.Thread(target=self.wait_for_quit_input)
        quit_thread.start()

        # Join threads to allow for clean shutdown
        inactivity_thread.join()
        activity_timer_thread.join()
        quit_thread.join()

        # Stop the listeners when the program exits
        mouse_listener.stop()
        keyboard_listener.stop()

    def wait_for_quit_input(self):
        """Waits for user input 'quit' and stops the timer."""
        user_input = input("Type 'q' to stop the timer: \n")
        if user_input.strip().lower() == 'q':
            self.stop_timer = True
            self.write_summary_to_file()

    def write_summary_to_file(self):
        """Writes Pomodoros, work minutes, and rest minutes to a file."""
        with open(self.pomodoro_summary, 'a') as f:
            f.write(f"Work stopped at:  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Pomodoros completed: {self.interval_timer.pomodoro_count}\n")
            f.write(f"Total work minutes: {self.interval_timer.total_work_minutes}\n")
            f.write(f"Total rest minutes: {self.interval_timer.total_rest_minutes}\n")
            f.write("------------------------------------\n")
        print(f"Pomodoro summary written to {self.pomodoro_summary}. Exiting...")


