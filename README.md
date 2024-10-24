# ChronoTask

ChronoTask is a task management application designed to help you manage and
track your tasks effectively using a Pomodoro timer with activity detection.

## Features
- **Add a Task**: Add a new task to your task list.
  ```bash
  chronotask add "Task"

- **List Active Tasks**:
    ```bash
    chronotask list

- **Options**:
        * --status all: List all tasks.
        * --status active: List active tasks.
        * --status done: List done tasks.
    Each task is displayed in a table format showing the time spent on each 
    task.

- **Task Management**:
    - done: Mark a task as done.
    - active: Mark a task as active.
    - dismiss: Mark a task as dismissed.
    - delete: Delete a task.
    - start: Start the Pomodoro timer for a given task, with activity 
    detection to stop the timer if inactivity exceeds a set interval.

## Examples
- **Add a new task**:
    ```bash
    chronotask add "Write READMI for the project."

- **List active tasks**:
    ```bash
    chronotask list --status active

- **Mark task with ID 2 as done:
    ```bash
    chronotask id 2 done

- **Start the Pomodore timer for the task with ID 1:
    ```bash
    chronotask id 1 start 

## Requirements
  - Python > 3.8
  - pipx

    To install the necessary packages, run the following commands:

    ```bash
    sudo apt update && sudo apt upgrade 
    sudo apt install --upgrade python3
    sudo apt install --upgrade pipx

## Installation
Download the ChronoTask package and install it using pipx:

    ```bash
    curl -LO https://github.com/nsx116/chronotask/raw/main/dist/chronotask_nsx116-0.0.1-py3-none-any.whl && \
    pipx install chronotask_nsx116-0.0.1-py3-none-any.whl

## Dependencies
ChronoTask requires the following Python packages, which will be installed
with pipx during installation:

- pynput
- pygame
- appdirs
- terminaltables













