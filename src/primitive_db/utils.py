import json
import os
import sys

DATA_DIR = "data"


def get_input(prompt="> ") -> str:
    sys.stdout.write(prompt)
    sys.stdout.flush()
    try:
        return input().strip()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из программы.")
        return "exit"


def load_metadata(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_metadata(filepath, data):
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def _ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def load_table_data(table_name):
    _ensure_data_dir()
    path = os.path.join(DATA_DIR, f"{table_name}.json")
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_table_data(table_name, data):
    _ensure_data_dir()
    path = os.path.join(DATA_DIR, f"{table_name}.json")
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)