#!/usr/bin/python3
'''
    Api REST
'''

if __name__ == '__main__':
    import requests
    from sys import argv

    '''
        Using this REST API, for a given employee ID,
        returns information about his/her TODO list progress.

        Args:
            id (int): The employee ID.

        Returns:
            None
    '''
    if len(argv) > 1:
        try:
            id = int(argv[1])
        except ValueError:
            pass

    if isinstance(id, int):
        user = requests.get(f"https://jsonplaceholder.typicode.com/users/{id}")
        to_dos = requests.get(
            f"https://jsonplaceholder.typicode.com/todos/?userId={id}"
            )

        if to_dos.status_code == 200 and user.status_code == 200:
            user = user.json()
            to_dos = to_dos.json()

            total_tasks = len(to_dos)
            tasks_completed = 0
            titles_completed = []

            for to_do in to_dos:
                if to_do.get('completed'):
                    tasks_completed += 1
                    titles_completed.append(to_do.get('title'))

            tasks_completed = len(titles_completed)

            print(f"Employee {user.get('name')} is done with tasks\
                  ({tasks_completed}/{total_tasks})")
            for title in titles_completed:
                print(f"\t {title}")
