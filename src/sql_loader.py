import sqlalchemy as sa
from data_loader import load_data

# Параметры подключения к PostgreSQL
DB_URL = "postgresql+psycopg2://postgres:******@localhost:5432/olist_db?client_encoding=utf8"


def create_engine():
    """Создаёт подключение к базе данных PostgreSQL."""
    return sa.create_engine(DB_URL)


def create_schema(engine: sa.engine.Engine):
    """Создаёт схему ecommerce, если её нет."""
    with engine.begin() as conn:
        conn.execute(sa.text("CREATE SCHEMA IF NOT EXISTS ecommerce"))
    print("Таблица 'ecommerce' готова")


def load_tables(engine: sa.engine.Engine):
    """Загружает CSV из data_loader в PostgreSQL."""
    # Получаем все датасеты
    orders, order_items, customers, payments, products, sellers, reviews = load_data()

    tables = {
        "orders": orders,
        "order_items": order_items,
        "customers": customers,
        "payments": payments,
        "products": products,
        "sellers": sellers,
        "reviews": reviews
    }

    # Загружаем таблицы
    for table_name, df in tables.items():
        print(f"Загружена таблица '{table_name}'...")
        df.to_sql(
            table_name,
            engine,
            schema="ecommerce",
            if_exists="replace",
            index=False
        )
    print("Все таблицы загружены")


def create_constraints(engine: sa.engine.Engine):
    """Добавляет ключи (PRIMARY и FOREIGN) к таблицам."""

    queries = [
        """
        ALTER TABLE IF EXISTS ecommerce.orders
        ADD PRIMARY KEY (order_id)
        """,
        """
        ALTER TABLE IF EXISTS ecommerce.customers
        ADD PRIMARY KEY (customer_id)
        """,
        """
        ALTER TABLE IF EXISTS ecommerce.order_items
        ADD FOREIGN KEY (order_id)
        REFERENCES ecommerce.orders(order_id)
        """
    ]

    with engine.begin() as conn:
        for q in queries:
            conn.execute(sa.text(q))
    print("Ограничения созданы")


def main():
    """Главная функция ETL: Таблица → Загрузка таблиц → Создания отношений."""
    engine = create_engine()

    print("Создается таблица...")
    create_schema(engine)

    print("Загружается таблица...")
    load_tables(engine)

    print("Создаются ограничения...")
    create_constraints(engine)

    print("ETL завершено")


if __name__ == "__main__":
    main()
