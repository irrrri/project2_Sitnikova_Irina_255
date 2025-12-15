# project2_Sitnikova_Irina_255

# Primitive DB

Небольшое консольное приложение на Python, демонстрирующее работу с пользовательским вводом,
игровым циклом и обработкой команд.

## Установка

Убедитесь, что у вас установлен Poetry.

```bash
poetry install
```

## Запуск
```bash
poetry run project
```

## Управление таблицами

Доступные команды:

- `create_table <имя> <столбец:тип> ...` — создать таблицу
- `list_tables` — показать список таблиц
- `drop_table <имя>` — удалить таблицу
- `help` — справка
- `exit` — выход

### Пример

```text
create_table users name:str age:int is_active:bool
list_tables
drop_table users
```

## Демонстрация работы

Ниже приведена демонстрация установки пакета, запуска базы данных,
создания таблицы, просмотра списка таблиц и удаления таблицы.

[![asciinema](https://asciinema.org/a/V6NrjudzY5NVuz4zhjESEY5ka.svg)](https://asciinema.org/a/V6NrjudzY5NVuz4zhjESEY5ka)

## CRUD-операции

- `insert into <table> values (<v1>, <v2>, ...)`
- `select from <table>`
- `select from <table> where <col> = <value>`
- `update <table> set <col> = <value> where <col> = <value>`
- `delete from <table> where <col> = <value>`
- `info <table>`

## Демонстрация CRUD-операций

[![asciinema](https://asciinema.org/a/v7G3dbVZkiOfP3P2TaImNjxSX.svg)](https://asciinema.org/a/v7G3dbVZkiOfP3P2TaImNjxSX)
