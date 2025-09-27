# 📊 Olist E-Store Data Analytics

## 🔹 1. Project Description
This project focuses on **data analytics of the Brazilian online store Olist**.  
The goal is to explore and analyze e-commerce data, load it into a PostgreSQL database, perform analytical queries, and connect the database to Python for automated analysis.  

Dataset used: **Olist Public Dataset (Kaggle)**  
Tables include: customers, orders, payments, reviews, sellers, products, geolocation, and order items.  

---

## 🔹 2. ER Diagram
The ER diagram describes the relationships between the tables in the Olist dataset.  

📌 
<img width="1166" height="591" alt="Снимок экрана 2025-09-27 в 21 21 52" src="https://github.com/user-attachments/assets/0db158da-f202-4a1d-a5b4-a41e7f337de9" />

---

## 🔹 3. Database Setup & Data Loading
- Created PostgreSQL database: `olist_db`
- Created 9 tables with appropriate columns matching the CSV files
- Loaded datasets using `\COPY` command in terminal:

```sql
\COPY olist_customers_dataset(customer_id, customer_unique_id, customer_zip_code_prefix, customer_city, customer_state)
FROM '/Users/macbook/Downloads/archive/olist_customers_dataset.csv'
DELIMITER ',' CSV HEADER;
