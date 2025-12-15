SUPPORTED_TYPES = {"int", "str", "bool"}


def _get_schema(metadata, table_name):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return None
    return metadata[table_name]


def _validate_value(expected_type: str, value):
    if expected_type == "int":
        return isinstance(value, int)
    if expected_type == "str":
        return isinstance(value, str)
    if expected_type == "bool":
        return isinstance(value, bool)
    return False


def _cast_to_type(expected_type: str, value):
    if expected_type == "int":
        if isinstance(value, int):
            return value
        if (isinstance(value, str) and
                (value.isdigit() or (value.startswith("-") and value[1:].isdigit()))):
            return int(value)
        return None

    if expected_type == "bool":
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            low = value.strip().lower()
            if low == "true":
                return True
            if low == "false":
                return False
        return None

    if expected_type == "str":
        if isinstance(value, str):
            return value
        return str(value)

    return None


def _typed_where(metadata, table_name, where_clause):
    schema = _get_schema(metadata, table_name)
    if schema is None:
        return None, None

    schema_map = {c["name"]: c["type"] for c in schema}
    (col, raw_val), = where_clause.items()

    if col not in schema_map:
        print(f"Некорректное значение: {col}. Попробуйте снова.")
        return None, None

    typed_val = _cast_to_type(schema_map[col], raw_val)
    if typed_val is None:
        print(f"Некорректное значение: {raw_val}. Попробуйте снова.")
        return None, None

    return col, typed_val


def create_table(metadata, table_name, columns):
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    parsed_columns = [{"name": "ID", "type": "int"}]

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

    cols_str = ", ".join(f'{c["name"]}:{c["type"]}' for c in parsed_columns)
    print(f'Таблица "{table_name}" успешно создана со столбцами: {cols_str}')
    return metadata


def drop_table(metadata, table_name):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata


def insert(metadata, table_name, table_data, values):
    schema = _get_schema(metadata, table_name)
    if schema is None:
        return table_data, None

    expected_count = len(schema) - 1
    if len(values) != expected_count:
        print(f"Некорректное значение: {values}. Попробуйте снова.")
        return table_data, None

    for col, val in zip(schema[1:], values, strict=False):
        if not _validate_value(col["type"], val):
            print(f"Некорректное значение: {val}. Попробуйте снова.")
            return table_data, None

    if table_data:
        new_id = max(row["ID"] for row in table_data) + 1
    else:
        new_id = 1

    row = {"ID": new_id}
    for col, val in zip(schema[1:], values, strict=False):
        row[col["name"]] = val

    table_data.append(row)
    return table_data, new_id


def select(metadata, table_name, table_data, where_clause=None):
    if not where_clause:
        return table_data

    where_col, where_val = _typed_where(metadata, table_name, where_clause)
    if where_col is None:
        return []

    return [row for row in table_data if row.get(where_col) == where_val]


def update(metadata, table_name, table_data, set_clause, where_clause):
    schema = _get_schema(metadata, table_name)
    if schema is None:
        return table_data, []

    schema_map = {c["name"]: c["type"] for c in schema}

    (set_col, set_raw), = set_clause.items()
    if set_col not in schema_map:
        print(f"Некорректное значение: {set_col}. Попробуйте снова.")
        return table_data, []

    set_val = _cast_to_type(schema_map[set_col], set_raw)
    if set_val is None:
        print(f"Некорректное значение: {set_raw}. Попробуйте снова.")
        return table_data, []

    where_col, where_val = _typed_where(metadata, table_name, where_clause)
    if where_col is None:
        return table_data, []

    matched_ids = []
    for row in table_data:
        if row.get(where_col) == where_val:
            row[set_col] = set_val
            matched_ids.append(row["ID"])

    return table_data, matched_ids


def delete(metadata, table_name, table_data, where_clause):
    where_col, where_val = _typed_where(metadata, table_name, where_clause)
    if where_col is None:
        return table_data, 0

    before = len(table_data)
    table_data = [row for row in table_data if row.get(where_col) != where_val]
    return table_data, before - len(table_data)