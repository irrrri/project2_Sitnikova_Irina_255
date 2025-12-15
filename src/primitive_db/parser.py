import shlex


def parse_scalar(value: str):
    v = value.strip()

    low = v.lower()
    if low == "true":
        return True
    if low == "false":
        return False

    if v.isdigit() or (v.startswith("-") and v[1:].isdigit()):
        return int(v)

    return v


def parse_clause(text: str):
    try:
        tokens = shlex.split(text)
    except ValueError:
        raise ValueError(f"Некорректное значение: {text}. Попробуйте снова.")

    if len(tokens) != 3 or tokens[1] != "=":
        raise ValueError(f"Некорректное значение: {text}. Попробуйте снова.")

    col = tokens[0]
    val = parse_scalar(tokens[2])
    return {col: val}


def parse_values_list(values_text: str):
    lexer = shlex.shlex(values_text, posix=True)
    lexer.whitespace = ","
    lexer.whitespace_split = True
    lexer.quotes = "\"'"

    raw_items = [item.strip() for item in lexer if item.strip()]
    return [parse_scalar(item) for item in raw_items]