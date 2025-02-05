#!/usr/bin/env python

import json
from datetime import datetime, timedelta
from main import Automation
from config import SCHEDULE_FILE, PROD

def read_schedule(file_path):
    """Read the schedule file and return a list of scheduled tasks."""
    with open(file_path, 'r') as file:
        tasks = json.load(file)
        for task in tasks:
            task['last_run'] = datetime.strptime(task['last_run'], "%Y-%m-%d %H:%M")
        return tasks

def write_schedule(file_path, tasks):
    """Write the updated schedule to the file."""
    with open(file_path, 'w') as file:
        for task in tasks:
            task['last_run'] = task['last_run'].strftime("%Y-%m-%d %H:%M")
        json.dump(tasks, file, indent=4)

def main():
    # Read the schedule file
    tasks = read_schedule(SCHEDULE_FILE)
    current_time = datetime.now()
    all_sites = []
    # Check if there are any tasks scheduled for the current time
    for task in tasks:
        interval = timedelta(weeks=task['interval_weeks'])
        next_run = task['last_run'] + interval
        if current_time >= next_run:
            all_sites.extend(task['sites'])
            task['last_run'] = current_time

    # Write the updated schedule back to the schedule file, otherwise it will run every minute... 

    if PROD:
        write_schedule(SCHEDULE_FILE, tasks)
    if all_sites:
        network_automation = Automation(all_sites)  # Pass sites array to the class
        network_automation.upgrade()  # Trigger upgrade process

if __name__ == "__main__":
    main()