import json
import sys


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