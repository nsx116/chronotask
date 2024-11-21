import plotext as plt
from datetime import datetime, timedelta
import calendar


def make_minutes_by_date_plot(year, month, data):
    """
    Creates a plot of minutes by date for a given year and month.

    Args:
        data (dict): A dictionary containing tasks with history of work minutes by date.
        year (int): The year for the plot.
        month (int): The month for the plot.
    """
    # Prepare all dates in the specified month
    num_days = calendar.monthrange(year, month)[1]
    dates = [
        datetime(year, month, day).strftime("%Y-%m-%d") for day in range(1, num_days + 1)
    ]

    # Initialize a dictionary to store total minutes per date
    minutes_by_date = {date: 0 for date in dates}

    # Flag to check if the requested year and month exist in data
    data_has_year_month = False

    # Accumulate minutes from task histories
    for task in data.get("tasks", []):
        for date, sessions in task.get("history", {}).items():
            task_year, task_month, _ = map(int, date.split("-"))
            if task_year == year and task_month == month:
                data_has_year_month = True  # Mark that data exists for the requested month
                if date in minutes_by_date:
                    # Sum up all minutes for the date
                    minutes_by_date[date] += sum(session["minutes"] for session in sessions)

    # If no data for the requested year and month, print a message and exit
    if not data_has_year_month:
        print(f"Requested year {year} and month {month} isn't in the data.")
        return

    # Prepare data for plotting
    dates = list(minutes_by_date.keys())  # Dates (x-axis)
    x_labels = [date.split('-')[-1] for date in dates]
    # y_values = list(minutes_by_date.values())  # Total minutes (y-axis)
    y_values = [round(minutes / 60, 1) for minutes in minutes_by_date.values()]  # Total minutes (y-axis)
    print(x_labels)

    # Plotting with plotext
    # plt.clear_plot()
    plt.title(f"Work Hours by Date: {calendar.month_name[month]} {year}")
    plt.bar(x_labels, y_values, label="Hours", width = 1 / 5)
    plt.xlabel("Date")
    plt.ylabel("Hours")
    plt.theme("pro")
    plt.plotsize(100, 20)
    # plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.show()
"""

# Example usage
data = {
    "tasks": [
        {
            "text": "Write work minutes by dates and tasks to json",
            "date": "2024-11-19",
            "project": None,
            "tag": None,
            "value": None,
            "global_id": "de7fcee3-aec6-42e5-8317-171a00ecc49c",
            "date_added": "2024-11-19 17:13:49",
            "date_done": None,
            "date_dismissed": None,
            "status": "done",
            "total_work": 192.1,
            "history": {
                "2024-11-19": [
                    {"work_started_at": "2024-11-19 18-01-26", "work_stopped_at": "2024-11-19 18:02:36", "minutes": 0.0},
                    {"work_started_at": "2024-11-19 18-50-02", "work_stopped_at": "2024-11-19 19:05:20", "minutes": 0.2},
                    {"work_started_at": "2024-11-19 19-05-24", "work_stopped_at": "2024-11-19 20:56:33", "minutes": 1.2},
                ],
                "2024-11-20": [
                    {"work_started_at": "2024-11-20 13-06-18", "work_stopped_at": "2024-11-20 13:06-24", "minutes": 0.0},
                    {"work_started_at": "2024-11-20 13-07-18", "work_stopped_at": "2024-11-20 13:31:50", "minutes": 0.3},
                    {"work_started_at": "2024-11-20 13-32-16", "work_stopped_at": "2024-11-20 13:33:24", "minutes": 1},
                    {"work_started_at": "2024-11-20 13-54-27", "work_stopped_at": "2024-11-20 15:22:36", "minutes": 50},
                ],
            },
        }
    ]
}

make_minutes_by_date_plot(data, 2024, 11)
"""
