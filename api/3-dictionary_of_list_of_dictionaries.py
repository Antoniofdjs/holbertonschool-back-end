#!/usr/bin/python3
'''
    Api REST
'''


import requests
from sys import argv
import json
import csv


def get_employee(id=None):
    '''
        using this REST API, for a given employee ID,
        returns information about his/her TODO list progress.
        Export a csv of specific user and export to JSON all user info
    '''
    # check if argv[1] is a number int, it means we are using argv
    if len(argv) > 1:
        try:
            id = int(argv[1])
        except ValueError:
            pass
            return

    if isinstance(id, int):
        user = requests.get(f"https://jsonplaceholder.typicode.com/users/{id}")
        to_dos = requests.get(
            f"https://jsonplaceholder.typicode.com/todos/?userId={id}"
            )

        if to_dos.status_code == 200 and user.status_code == 200:
            # This entire if section will handle the single user and CSV
            user = json.loads(user.text)
            to_dos = json.loads(to_dos.text)

            total_tasks = len(to_dos)
            tasks_completed = 0
            titles_completed = []
            csv_rows = []
            user_id = id

            for to_do in to_dos:
                # Prepare rows for csv file
                csv_rows.append(
                    [user_id,
                     user['username'],
                     to_do['completed'],
                     to_do['title']
                     ]
                    )
                # Count and append titles of completed tasks
                if to_do['completed'] is True:
                    tasks_completed += 1
                    titles_completed.append(to_do['title'])

            tasks_completed = len(titles_completed)

            # 1.0 Data of User Prints with tasks
            print(f"Employee {user['name']} is done \
                  with tasks({tasks_completed}/{total_tasks})")
            for title in titles_completed:
                print(f"\t {title}")

            # 2.0 CSV section
            with open(f"{user_id}.csv", 'w', newline='') as csv_file:
                writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
                writer.writerows(csv_rows)

        # 3.0 All users JSON Section
        users = requests.get("https://jsonplaceholder.typicode.com/users/")

        if users.status_code == 200:
            users = json.loads(users.text)

            # {USER_ID:[ {"username": "USERNAME"},{"username: ..."}], USER2_ID:[{}]
            dict_for_json = {}
            for user in users:
                user_list = []
                user_id = user['id']
                api_url = 'https://jsonplaceholder.typicode.com'
                tasks = requests.get(
                    f"{api_url}/todos/?userId={user_id}"
                    )

                if tasks.status_code == 200:
                    tasks = json.loads(tasks.text)
                    for task in tasks:
                        user_dict = {}
                        username = user['username']
                        task_title = task['title']
                        completed = task['completed']

                        # Make user dictionary for list
                        user_dict.update(
                            {'username': username,
                            'task': task_title,
                            'completed': completed
                            }
                            )
                        user_list.append(user_dict)

                    # Finally put the list inside the json dict
                    dict_for_json[user_id] = user_list

            with open("todo_all_employees.json", 'w') as file:
                json.dump(dict_for_json, file)


if __name__ == '__main__':
    get_employee()
