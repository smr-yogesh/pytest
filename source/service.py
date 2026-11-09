import requests

database = {1: "Alice", 2: "Bob", 3: "Charlie"}


def get_user(user_id):
    return database.get(user_id)


def get_user_api():
    resonse = requests.get("https://jsonplaceholder.typicode.com/users")
    if resonse.status_code == 200:
        return resonse.json()

    raise requests.HTTPError
