SUPPORTED_TYPES = {"int", "str", "bool"}


def create_table(metadata, table_name, columns):
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    parsed_columns = []

    parsed_columns.append({"name": "ID", "type": "int"})

    for column in columns:
        if ":" not in column:
            print(f"Некорректное значение: {column}. Попробуйте снова.")
            return metadata

        name, col_type = column.split(":", 1)

        if col_type not in SUPPORTED_TYPES:
            print(f"Некорректное значение: {col_type}. Попробуйте снова.")
            return metadata

        parsed_columns.append({"name": name, "type": col_type})

    metadata[table_name] = parsed_columns

    column_descriptions = ", ".join(
        f'{col["name"]}:{col["type"]}' for col in parsed_columns
    )

    print(
        f'Таблица "{table_name}" успешно создана со столбцами: {column_descriptions}'
    )

    return metadata


def drop_table(metadata, table_name):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')

    return metadata