#!/usr/bin/python3
'''
    Api REST
'''


import requests
from sys import argv
import json


def get_employee(id=None):
    '''
        using this REST API, for a given employee ID,
        returns information about his/her TODO list progress.
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
        to_dos = requests.get("https://jsonplaceholder.typicode.com/todos/")

        if to_dos.status_code == 200 and user.status_code == 200:
            user = json.loads(user.text)
            to_dos = json.loads(to_dos.text)

            total_tasks = 0
            tasks_completed = 0
            titles = []

            for to_do in to_dos:
                if to_do['userId'] == user['id']:
                    total_tasks += 1
                    if to_do['completed'] is True:
                        tasks_completed += 1
                        titles.append(to_do['title'])

            print(f"Employee {user['name']} is done with tasks\
                  ({tasks_completed}/{total_tasks})")
            for title in titles:
                print(f"\t {title}")


if __name__ == '__main__':
    get_employee()
