import psycopg2

DB_NAME = "olist_db"
DB_USER = "postgres"
DB_PASS = "0000"   
DB_HOST = "localhost"
DB_PORT = "5432"

def run_query(cursor, query, description):
    print(f"\n--- {description} ---")
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows[:10]:  
        print(row)

def main():
    try:
        # подключение к БД
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()
        print("✅ Connected to database!")

        
        queries = [
            (
                "Количество заказов по статусам",
                "SELECT order_status, COUNT(*) FROM olist_orders_dataset GROUP BY order_status;"
            ),
            (
                "ТОП-10 продавцов по сумме продаж",
                """
                SELECT s.seller_id, SUM(oi.price) AS total_sales
                FROM olist_order_items_dataset oi
                JOIN olist_sellers_dataset s ON oi.seller_id = s.seller_id
                GROUP BY s.seller_id
                ORDER BY total_sales DESC
                LIMIT 10;
                """
            ),
            (
                "Средний рейтинг по категориям продуктов",
                """
                SELECT p.product_category_name, AVG(r.review_score) AS avg_score
                FROM olist_order_items_dataset oi
                JOIN olist_products_dataset p ON oi.product_id = p.product_id
                JOIN olist_order_reviews_dataset r ON oi.order_id = r.order_id
                GROUP BY p.product_category_name
                ORDER BY avg_score DESC
                LIMIT 10;
                """
            )
        ]

        
        for description, query in queries:
            run_query(cursor, query, description)

        cursor.close()
        conn.close()
        print("\n✅ Done!")

    except Exception as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    main()
