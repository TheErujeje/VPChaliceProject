import json


def load_db():
    with open("data.json") as f:
        return json.load(f)


def save_db(newdata):
    with open("data.json", 'w') as f:
        return json.dump(newdata, f, indent=4)


db = load_db()
