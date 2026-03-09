import pandas as pd
from pathlib import Path

# путь к папке с CSV
DATA_PATH = Path(__file__).resolve().parent.parent / "data"


def load_data():
    """Загрузка всех датасетов в DataFrame"""
    orders = pd.read_csv(DATA_PATH / "olist_orders_dataset.csv")
    order_items = pd.read_csv(DATA_PATH / "olist_order_items_dataset.csv")
    customers = pd.read_csv(DATA_PATH / "olist_customers_dataset.csv")
    payments = pd.read_csv(DATA_PATH / "olist_order_payments_dataset.csv")
    products = pd.read_csv(DATA_PATH / "olist_products_dataset.csv")
    sellers = pd.read_csv(DATA_PATH / "olist_sellers_dataset.csv")
    reviews = pd.read_csv(DATA_PATH / "olist_order_reviews_dataset.csv")

    return orders, order_items, customers, payments, products, sellers, reviews


def initial_data_check(df, name="DataFrame"):
    """Простая первичная проверка датасета"""
    print(f"\n{'=' * 60}")
    print(f"Первичная проверка: {name}")
    print(f"{'=' * 60}")

    print("\n Размерность:")
    print(f"Строк: {df.shape[0]}, Колонок: {df.shape[1]}")

    print("\n Типы данных:")
    print(df.dtypes)

    missing = df.isna().sum()
    missing = missing[missing > 0]
    print("\n Пропуски:")
    if len(missing) == 0:
        print("Пропусков нет ")
    else:
        print(missing.sort_values(ascending=False))

    print("\n Дубликаты:")
    print(f"Количество дубликатов: {df.duplicated().sum()}")

    print("\n Первые 5 строк:")
    print(df.head())


def calculate_metrics(orders, order_items, payments, customers):
    """Расчёт базовых метрик: общая выручка, средний чек, уникальные клиенты"""
    df = (
        orders
        .merge(order_items, on="order_id")
        .merge(payments, on="order_id")
    )

    total_revenue = df["payment_value"].sum()
    unique_customers = customers["customer_unique_id"].nunique()
    avg_order_value = df.groupby("order_id")["payment_value"].sum().mean()

    print("\n Метрики:")
    print(f"Общая выручка: {round(total_revenue, 2)}")
    print(f"Уникальные клиенты: {unique_customers}")
    print(f"Средний чек: {round(avg_order_value, 2)}")


def main():
    orders, order_items, customers, payments, products, sellers, reviews = load_data()

    # первичная проверка
    initial_data_check(orders, "Orders")
    initial_data_check(order_items, "Order Items")
    initial_data_check(customers, "Customers")
    initial_data_check(payments, "Payments")
    initial_data_check(products, "Products")
    initial_data_check(sellers, "Sellers")
    initial_data_check(reviews, "Reviews")

    # расчёт метрик
    calculate_metrics(orders, order_items, payments, customers)


if __name__ == "__main__":
    main()