import psycopg2
import random
import time
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

# --- Параметры подключения (измени под свои данные) ---
conn = psycopg2.connect(
    host="localhost",
    database="olist_db",
    user="postgres",
    password="0000"
)
conn.autocommit = True
cur = conn.cursor()

# --- Получаем customer_id из таблицы клиентов, чтобы не нарушать FK ---
cur.execute("SELECT customer_id FROM olist_customers_dataset")
customer_ids = [row[0] for row in cur.fetchall()]

print(f"Loaded {len(customer_ids)} customers.")

# --- Функция для добавления нового заказа ---
def insert_new_order():
    order_id = fake.uuid4()
    customer_id = random.choice(customer_ids)
    order_status = random.choice(["delivered", "shipped", "processing", "approved", "created"])
    order_purchase_timestamp = datetime.now()
    order_approved_at = order_purchase_timestamp + timedelta(minutes=random.randint(1, 30))
    order_delivered_carrier_date = order_approved_at + timedelta(days=random.randint(1, 3))
    order_delivered_customer_date = order_delivered_carrier_date + timedelta(days=random.randint(3, 7))
    order_estimated_delivery_date = order_purchase_timestamp + timedelta(days=random.randint(5, 10))

    query = """
        INSERT INTO olist_orders_dataset (
            order_id,
            customer_id,
            order_status,
            order_purchase_timestamp,
            order_approved_at,
            order_delivered_carrier_date,
            order_delivered_customer_date,
            order_estimated_delivery_date
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """
    cur.execute(query, (
        order_id,
        customer_id,
        order_status,
        order_purchase_timestamp,
        order_approved_at,
        order_delivered_carrier_date,
        order_delivered_customer_date,
        order_estimated_delivery_date
    ))

    print(f"✅ Inserted order {order_id} (status={order_status}) at {order_purchase_timestamp}")

# --- Основной цикл ---
INTERVAL_SECONDS = 10  # можно поменять на 5–20 сек

print("🚀 Auto data insert started! Press Ctrl+C to stop.\n")

try:
    while True:
        insert_new_order()
        time.sleep(INTERVAL_SECONDS)
except KeyboardInterrupt:
    print("\n🛑 Script stopped by user.")
finally:
    cur.close()
    conn.close()
