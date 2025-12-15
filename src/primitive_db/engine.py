import shlex

from prettytable import PrettyTable

from src.primitive_db.core import (
    create_table,
    delete,
    drop_table,
    insert,
    select,
    update,
)
from src.primitive_db.parser import parse_clause, parse_values_list
from src.primitive_db.utils import (
    get_input,
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)

DB_FILE = "db_meta.json"


def print_help():
    print("\n***Операции с данными***\n")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> ..")
    print("<command> list_tables")
    print("<command> drop_table <имя_таблицы>")
    print('<command> insert into <таблица> values (<v1>, <v2>, ...) - создать запись.')
    print('<command> select from <таблица> where <col> = <value> - выбрать по условию.')
    print('<command> select from <таблица> - выбрать все записи.')
    print('<command> update <таблица> set <col> = <value> '
          'where <col> = <value> - обновить.')
    print('<command> delete from <таблица> where <col> = <value> - удалить.')
    print("<command> info <таблица> - информация о таблице.")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def _print_rows(table_name, metadata, rows):
    schema = metadata.get(table_name)
    if not schema:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    columns = [c["name"] for c in schema]
    pt = PrettyTable()
    pt.field_names = columns

    for row in rows:
        pt.add_row([row.get(col) for col in columns])

    print(pt)


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

        cmd = args[0].lower()

        if cmd == "help":
            print_help()
            continue

        if cmd == "exit":
            break

        if cmd == "list_tables":
            if not metadata:
                print("Таблиц нет.")
            else:
                for t in metadata:
                    print(f"- {t}")
            continue

        if cmd == "create_table":
            if len(args) < 3:
                print("Некорректное значение: команда. Попробуйте снова.")
                continue
            table_name = args[1]
            columns = args[2:]
            metadata = create_table(metadata, table_name, columns)
            save_metadata(DB_FILE, metadata)
            continue

        if cmd == "drop_table":
            if len(args) != 2:
                print("Некорректное значение: команда. Попробуйте снова.")
                continue
            table_name = args[1]
            metadata = drop_table(metadata, table_name)
            save_metadata(DB_FILE, metadata)
            continue

        if cmd == "info":
            if len(args) != 2:
                print("Некорректное значение: команда. Попробуйте снова.")
                continue
            table_name = args[1]
            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue
            schema = metadata[table_name]
            cols_str = ", ".join(f'{c["name"]}:{c["type"]}' for c in schema)
            data = load_table_data(table_name)
            print(f"Таблица: {table_name}")
            print(f"Столбцы: {cols_str}")
            print(f"Количество записей: {len(data)}")
            continue

        if user_input.lower().startswith("insert into "):
            try:
                tail = user_input[len("insert into "):].strip()
                if " values " not in tail.lower():
                    print("Некорректное значение: команда. Попробуйте снова.")
                    continue

                before_values, values_part = tail.split("values", 1)
                table_name = before_values.strip()

                if table_name not in metadata:
                    print(f'Ошибка: Таблица "{table_name}" не существует.')
                    continue

                values_part = values_part.strip()
                if not (values_part.startswith("(") and values_part.endswith(")")):
                    print("Некорректное значение: values. Попробуйте снова.")
                    continue

                inside = values_part[1:-1].strip()
                values = parse_values_list(inside)

                table_data = load_table_data(table_name)
                table_data, new_id = insert(metadata, table_name, table_data, values)

                if new_id is not None:
                    save_table_data(table_name, table_data)
                    print(f'Запись с ID={new_id} успешно добавлена '
                          f'в таблицу "{table_name}".')

            except ValueError as e:
                print(e)
            continue

        if user_input.lower().startswith("select from "):
            try:
                tail = user_input[len("select from "):].strip()
                if " where " in tail.lower():
                    table_part, where_part = tail.split("where", 1)
                    table_name = table_part.strip()
                    where_clause = parse_clause(where_part.strip())
                else:
                    table_name = tail.strip()
                    where_clause = None

                if table_name not in metadata:
                    print(f'Ошибка: Таблица "{table_name}" не существует.')
                    continue

                table_data = load_table_data(table_name)
                rows = select(metadata, table_name, table_data, where_clause)
                _print_rows(table_name, metadata, rows)

            except ValueError as e:
                print(e)
            continue

        if user_input.lower().startswith("update "):
            try:
                tail = user_input[len("update "):].strip()

                if " set " not in tail.lower() or " where " not in tail.lower():
                    print("Некорректное значение: команда. Попробуйте снова.")
                    continue

                table_part, rest = tail.split("set", 1)
                table_name = table_part.strip()

                set_part, where_part = rest.split("where", 1)
                set_clause = parse_clause(set_part.strip())
                where_clause = parse_clause(where_part.strip())

                if table_name not in metadata:
                    print(f'Ошибка: Таблица "{table_name}" не существует.')
                    continue

                table_data = load_table_data(table_name)
                table_data, ids = update(
                    metadata,
                    table_name,
                    table_data,
                    set_clause,
                    where_clause
                )

                if ids:
                    save_table_data(table_name, table_data)
                    for rid in ids:
                        print(f'Запись с ID={rid} в таблице '
                              f'"{table_name}" успешно обновлена.')
                else:
                    print("Подходящих записей не найдено.")

            except ValueError as e:
                print(e)
            continue

        if user_input.lower().startswith("delete from "):
            try:
                tail = user_input[len("delete from "):].strip()

                if " where " not in tail.lower():
                    print("Некорректное значение: команда. Попробуйте снова.")
                    continue

                table_part, where_part = tail.split("where", 1)
                table_name = table_part.strip()
                where_clause = parse_clause(where_part.strip())

                if table_name not in metadata:
                    print(f'Ошибка: Таблица "{table_name}" не существует.')
                    continue

                table_data = load_table_data(table_name)
                table_data, deleted_count = delete(
                    metadata,
                    table_name,
                    table_data,
                    where_clause)

                if deleted_count > 0:
                    save_table_data(table_name, table_data)
                    if "ID" in where_clause:
                        print(
                            f'Запись с ID={where_clause["ID"]} успешно '
                            f'удалена из таблицы "{table_name}".'
                        )
                    else:
                        print(f"Удалено записей: {deleted_count}")
                else:
                    print("Подходящих записей не найдено.")

            except ValueError as e:
                print(e)
            continue

        print(f"Функции {args[0]} нет. Попробуйте снова.")