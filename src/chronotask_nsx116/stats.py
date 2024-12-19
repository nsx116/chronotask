import plotext as plt
from datetime import datetime
import calendar


def make_minutes_by_date_plot(year, month, data):
    # Prepare all dates in the specified month
    num_days = calendar.monthrange(year, month)[1]
    dates = [
        datetime(year, month, day).strftime("%Y-%m-%d") for day in range(1, num_days + 1)
    ]

    # List of weekday abbreviations
    weekdays = ["mo", "tu", "we", "th", "fr", "sa", "su"]

    x_labels = [
        f"{date.split('-')[-1]}{weekdays[calendar.weekday(year, month, int(date.split('-')[-1]))]}"
        for date in dates
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
                    minutes_by_date[date] += sum(session.get("minutes", 0) for session in sessions)

    # Calculate the average using for given month
    total = sum(minutes_by_date.values())
    today = datetime.now()
    count = 0
    last_non_zero_index = 1
    if (year < today.year) or (year == today.year and month < today.month):
        count = num_days
    else:
        for key, value in minutes_by_date.items():
            count += 1
            if value != 0:
                last_non_zero_index = count  # Track the index of the last non-zero value
        count = last_non_zero_index if count > 0 else 1

    average = round(total / count / 60, 1) if count > 0 else 0

    # If no data for the requested year and month, print a message and exit
    if not data_has_year_month:
        print(f"Requested year {year} and month {month} isn't in the data.")
        return

    # Prepare data for plotting
    y_values = [round(minutes / 60, 1) for minutes in minutes_by_date.values()]  # Total minutes (y-axis)

    # plt.interactive(True)

    # Plotting with plotext
    plt.title(f"Work Hours by Date: {calendar.month_name[month]} {year}")
    plt.bar(x_labels, y_values, width = 2 / 5, color=44)
    plt.theme("pro")
    plt.plotsize(100, 11)
    plt.ylim(0)
    largest = int(max(y_values))
    for y in range(1, largest + 1):
        plt.hline(y, color=13)
    # Draw vertical lines where x_label contains "mo"
    for idx, label in enumerate(x_labels):
        if "mo" in label:
            plt.vline(idx, color=13)  # Use the index as the x-position
    plt.show()
    print(f"Sum: {round(total / 60, 1)} hours Count: {count} days Average: {average} hours/day")
