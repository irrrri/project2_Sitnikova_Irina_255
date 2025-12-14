import shlex

from prompt import string

from src.primitive_db.core import create_table, drop_table
from src.primitive_db.utils import get_input, load_metadata, save_metadata

DB_FILE = "db_meta.json"
HELP_TEXT = (
    "<command> exit - выйти из программы\n"
    "<command> help - справочная информация"
)


def print_help():
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> ..")
    print("<command> list_tables")
    print("<command> drop_table <имя_таблицы>")
    print("\nОбщие команды:")
    print("<command> exit")
    print("<command> help\n")


def run():
    print_help()

    while True:
        metadata = load_metadata(DB_FILE)

        user_input = get_input("Введите команду: ")

        if not user_input:
            continue

        try:
            args = shlex.split(user_input)
        except ValueError:
            print("Ошибка разбора команды.")
            continue

        command = args[0]

        if command == "help":
            print_help()

        elif command == "exit":
            break

        elif command == "list_tables":
            if not metadata:
                print("Таблиц нет.")
            else:
                for table in metadata:
                    print(f"- {table}")

        elif command == "create_table":
            if len(args) < 3:
                print("Некорректная команда. Попробуйте снова.")
                continue

            table_name = args[1]
            columns = args[2:]

            metadata = create_table(metadata, table_name, columns)
            save_metadata(DB_FILE, metadata)

        elif command == "drop_table":
            if len(args) != 2:
                print("Некорректная команда. Попробуйте снова.")
                continue

            table_name = args[1]
            metadata = drop_table(metadata, table_name)
            save_metadata(DB_FILE, metadata)

        else:
            print(f"Функции {command} нет. Попробуйте снова.")