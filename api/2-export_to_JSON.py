#!/usr/bin/python3
"""Documentation"""
import json
import requests
import sys

if __name__ == "__main__":
    employee_id = int(sys.argv[1])

    api_url = f'https://jsonplaceholder.typicode.com/users/{employee_id}'
    response = requests.get(api_url)

    employee_name = response.json()["username"]

    api_url2 = (
            f'https://jsonplaceholder.typicode.com/todos?userId={employee_id}'
    )
    response = requests.get(api_url2)

    tasks = response.json()
    total_tasks = len(tasks)

    completed_tasks = []
    for task in tasks:
        if task["completed"]:
            completed_tasks.append(task)

    n_total_tasks = len(completed_tasks)

    print(
        f"Employee {employee_name} is done with "
        f"tasks({n_total_tasks}/{total_tasks}):"
    )

    for task in completed_tasks:
        print(f"\t {task['title']}")

    json_dict = {employee_id: []}
    for task in tasks:
        json_format = {
            "task": task["title"],
            "completed": task["completed"],
            "username": employee_name
        }
        json_dict[employee_id].append(json_format)

    with open(f"{employee_id}.json", 'w') as json_file:
        json.dump(json_dict, json_file)
