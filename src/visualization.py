import pandas as pd
import sqlalchemy as sa
import matplotlib.pyplot as plt
import seaborn as sns

DB_URL = "postgresql+psycopg2://postgres:*****@localhost:5432/olist_db"

engine = sa.create_engine(DB_URL)


def monthly_active_users():
    query = """
    SELECT
        DATE_TRUNC('month', order_purchase_timestamp::timestamp) AS month,
        COUNT(DISTINCT customer_id) AS mau
    FROM ecommerce.orders
    GROUP BY month
    ORDER BY month
    """

    df = pd.read_sql(query, engine)

    plt.figure(figsize=(10,5))
    sns.lineplot(data=df, x="month", y="mau")

    plt.title("Активные пользователи по месяцам")
    plt.xlabel("Месяц")
    plt.ylabel("Количество пользователей")

    plt.show()


def top_products():
    query = """
    SELECT
        p.product_category_name,
        SUM(oi.price) AS total_sales
    FROM ecommerce.order_items oi
    JOIN ecommerce.products p ON oi.product_id = p.product_id
    GROUP BY p.product_category_name
    ORDER BY total_sales DESC
    LIMIT 10
    """

    df = pd.read_sql(query, engine)

    plt.figure(figsize=(10,6))
    sns.barplot(data=df, x="total_sales", y="product_category_name")

    plt.title("Топ-10 категорий товаров по продажам")
    plt.xlabel("Выручка")
    plt.ylabel("Категория")

    plt.show()


def review_distribution():
    query = """
    SELECT review_score, COUNT(*) as review_count
    FROM ecommerce.reviews
    GROUP BY review_score
    ORDER BY review_score
    """

    df = pd.read_sql(query, engine)

    plt.figure(figsize=(6,4))
    sns.barplot(data=df, x="review_score", y="review_count")

    plt.title("Распределение оценок отзывов")

    plt.show()


def main():
    monthly_active_users()
    top_products()
    review_distribution()


if __name__ == "__main__":
    main()