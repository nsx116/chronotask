from datetime import datetime
import time
import threading
import sys
import tty
import termios
import select
import os
from chronotask_nsx116.interval_timer import IntervalTimer
from chronotask_nsx116.settings import Settings, Files
from chronotask_nsx116.writing_to_task import write_past_minutes_when_quit
from chronotask_nsx116.writing_to_task import get_global_id_by_current_id
from chronotask_nsx116.writing_to_task import write_at_start


class FocusTrack:
    def __init__(self, task_manager):
        self.settings = task_manager.settings
        self.files = Files()
        self.last_activity_time = time.time()
        self.stop_timer = False
        self.working = True
        self.activity_timer_pause = False
        self.pomodoro_summary = self.files.pomodoro_summary_file
        self.interval_timer = IntervalTimer(self)
        self.activity_duration = self.interval_timer.activity_duration
        self.work_started_at = None
        self.sorted_ids = task_manager.sorted_ids
        self.use_x11 = self._check_x11()

    def _check_x11(self):
        """Check if X11 display is available. Returns True for local GUI, False for SSH."""
        try:
            return 'DISPLAY' in os.environ and os.environ['DISPLAY']
        except Exception:
            return False

    def reset_activity_timer(self):
        """Resets the last activity time when there is user activity."""
        self.last_activity_time = time.time()

    def check_inactivity(self):
        """Checks for inactivity and pauses the timer if no activity is detected."""
        while not self.stop_timer:
            if self.working:
                if time.time() - self.last_activity_time > self.settings.inactivity_limit:
                    if not self.activity_timer_pause:
                        print("\r" + " " * 75, end='', flush=True)
                        print(f"\rNo activity for {self.settings.inactivity_limit} seconds, pausing timer {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", end='', flush=True)
                        self.activity_timer_pause = True
            time.sleep(1)

    def update_activity_timer(self, global_id):
        """Continuously updates the activity timer and logs every minute."""
        while not self.stop_timer:
            self.interval_timer.run(global_id)

    def _x11_activity_loop(self, global_id):
        """Run pynput listeners for X11/graphical environments."""
        from pynput import mouse, keyboard
        
        def on_mouse_move(x, y):
            self.reset_activity_timer()
            if self.activity_timer_pause and self.working:
                print("\r" + " " * 75, end='', flush=True)
                print(f"\rResuming timer due to mouse activity.{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", end='', flush=True)
                self.activity_timer_pause = False

        def on_keyboard_event(key):
            self.reset_activity_timer()
            if self.activity_timer_pause and self.working:
                print("\r" + " " * 75, end='', flush=True)
                print(f"\rResuming timer due to keyboard activity {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", end='', flush=True)
                self.activity_timer_pause = False

        mouse_listener = mouse.Listener(on_move=on_mouse_move)
        keyboard_listener = keyboard.Listener(on_press=on_keyboard_event)

        mouse_listener.start()
        keyboard_listener.start()

        while not self.stop_timer:
            time.sleep(0.1)

        mouse_listener.stop()
        keyboard_listener.stop()

    def _tty_activity_loop(self, global_id):
        """Monitor TTY input for SSH/terminal environments (only for 'q' quit)."""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            while not self.stop_timer:
                if select.select([sys.stdin], [], [], 0.1)[0]:
                    ch = sys.stdin.read(1)
                    if ch == 'q':
                        self.stop_timer = True
                        write_past_minutes_when_quit(
                            global_id,
                            self.interval_timer.activity_duration,
                        )
                        print("Timer stopped.")
                        break
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def start(self, current_id):
        """Starts the timer with appropriate input detection mode."""

        self.work_started_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        global_id = get_global_id_by_current_id(current_id, self.sorted_ids)
        write_at_start(global_id, self.work_started_at)

        self.activity_timer_pause = False

        if self.use_x11:
            activity_thread = threading.Thread(target=self._x11_activity_loop, args=(global_id,))
            print("Using X11 input monitoring (mouse/keyboard)")
            inactivity_thread = threading.Thread(target=self.check_inactivity, daemon=True)
            inactivity_thread.start()
        else:
            activity_thread = threading.Thread(target=self._tty_activity_loop, args=(global_id,))
            print("SSH mode: Timer runs continuously without activity detection")
            print("Press 'q' to stop the timer")

        activity_thread.start()

        activity_timer_thread = threading.Thread(target=self.update_activity_timer, args=(global_id,))
        activity_timer_thread.start()

        quit_thread = threading.Thread(target=self.wait_for_quit_input, args=(global_id,))
        quit_thread.start()

        activity_thread.join()
        activity_timer_thread.join()
        quit_thread.join()

    def wait_for_quit_input(self, global_id):
        """Waits for user input 'q' and stops the timer."""
        if not self.use_x11:
            while not self.stop_timer:
                time.sleep(0.1)
        else:
            while not self.stop_timer:
                try:
                    user_input = input().strip().lower()
                    if user_input == 'q':
                        self.stop_timer = True
                        write_past_minutes_when_quit(
                            global_id,
                            self.interval_timer.activity_duration,
                        )
                        print("Timer stopped.")
                    else:
                        print("Invalid input. Type 'q' to stop the timer.")
                except KeyboardInterrupt:
                    print("\nExiting due to keyboard interrupt.")
                    self.stop_timer = True
                    break
