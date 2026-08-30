from . import data_for_base
import sqlalchemy as sa


def reflect_table(connection, table_name):
    """
    Загружает таблицу из базы, используя autoload_from=connection.
    Таблицы не нужно описывать вручную.
    """
    metadata = sa.MetaData()
    table = sa.Table(table_name, metadata, autoload_with=connection)
    return table


def populate_table(connection, table_name):
    """
    Вставляет записи в таблицу через одно соединение.
    """
    table = reflect_table(connection, table_name)
    data = getattr(data_for_base, table_name)
    # вставка одной операцией (быстро)
    connection.execute(table.insert(), data)

    if "id" in table.c:
        sync_sequence(connection, table)



def sync_sequence(connection, table):
    table_name = table.name

    sequence = connection.execute(
        sa.text("""
            SELECT pg_get_serial_sequence(:table_name, 'id')
        """),
        {"table_name": table_name},
    ).scalar_one()

    if sequence is None:
        return

    max_id = connection.execute(
        sa.select(sa.func.max(table.c.id))
    ).scalar()

    if max_id is None:
        return

    connection.execute(
        sa.text("SELECT setval(:sequence, :value)"),
        {
            "sequence": sequence,
            "value": max_id,
        },
    )

def run(connection):
    """
    Основная функция, вызываемая из миграции.
    Работает на одном соединении из Alembic upgrade().
    """
    # словарь "имя таблицы" → список данных
    payload = ["dates", "users", "meters", "measures", "actions"]

    for table_name in payload:
        print(f"Заполнение таблицы: {table_name}")
        populate_table(connection, table_name)
