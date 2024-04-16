#!/usr/bin/python3
""" Console Module """
"""
Pythin script that uses this  rest api for given
employee ID to return info about his/her todo list progress
"""
if __name__ == '__main__':
    import csv
    import json
    from requests import get
    from sys import argv
    """this module is fucking documented"""

    employee_ID = argv[1]
    all_todos = get(f'https://jsonplaceholder.typicode.com/todos')
    users = get(f'https://jsonplaceholder.typicode.com/users')

    employee_list = json.loads(all_todos.text)
    users = json.loads(users.text)
    for user in users:
        if user.get('id') == int(employee_ID):
            employee_name = user.get('username')

    task_count = 0
    task_list = []
    task_success = []
    for employee in employee_list:
        if employee.get('userId') == int(employee_ID):
            task_count += 1
            task_list.append(employee['title'])
            task_success.append(employee['completed'])

    json_list = []
    employee_id = str(employee_ID)
    THE_dict = {}
    for i in range(len(task_list)):
        true_or_false = bool(task_success[i])
        task = f'{task_list[i]}'
        name = employee_name
        every_dict = ({'task': task,
                       'completed': true_or_false,
                       'username': name})
        json_list.append(every_dict)
    THE_dict[employee_id] = json_list

    with open(f'{employee_ID}.json', 'w') as f:
        json.dump(THE_dict, f)
