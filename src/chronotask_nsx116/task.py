from datetime import datetime, date
from terminaltables import AsciiTable
import textwrap

class Task:
    def __init__(self, text="text", due_date=None, project=None,
                 tag=None, value=None, global_id=None):
        self.text = text
        self.due_date = due_date if due_date else date.today()  # Default is today if not provided
        self.project = project
        self.tag = tag
        self.value = value
        self.global_id = global_id

        # Task lifecycle attributes
        self.date_added = datetime.now()
        self.date_done = None
        self.date_dismissed = None
        self.status = "active"  # Can be "active", "done", or "dismissed"
        self.total_work = 0

    def mark_done(self):
        if self.status in ["active", "dismissed"]:
            self.status = "done"
            self.date_done = datetime.now()
            print(f"Task {self.global_id} marked as done.")
        else:
            print(f"Cannot mark task {self.global_id} as done. Current status: {self.status}")

    def mark_active(self):
        if self.status in ["done", "dismissed"]:
            self.status = "active"
            print(f"Task {self.global_id} marked as active.")
        else:
            print(f"Cannot mark task {self.global_id} as active. Current status: {self.status}")

    def dismiss(self):
        if self.status in ["active", "done"]:
            self.status = "dismissed"
            self.date_dismissed = datetime.now()
            print(f"Task {self.global_id} dismissed.")
        else:
            print(f"Cannot dismiss task {self.global_id}. Current status: {self.status}")

    def modify(self, text=None, due_date=None, project=None, tag=None, value=None):
        if text:
            self.text = text
        if due_date:
            self.due_date = due_date
        if project:
            self.project = project
        if tag:
            self.tag = tag
        if value:
            self.value = value
        print(f"Task {self.global_id} modified.")

    def __repr__(self):
     # Determine the checkbox symbol based on the status
        if self.status == "active":
            checkbox = "- [ ]"
        elif self.status == "done":
            checkbox = "- [x]"
        elif self.status == "dismissed":
            checkbox = "- [-]"
        else:
            checkbox = "- [?]"  # For any unknown status
        wrapped_lines = textwrap.wrap(self.text, width=49)
        padded_lines = [line.ljust(49) for line in wrapped_lines]
        wrapped_text = "\n".join(padded_lines)
        details_line = (f"Due={self.due_date}, Project={self.project},"
                        f"Tag={self.tag}, Value={self.value}")
        return f"{wrapped_text}\n{details_line}"

