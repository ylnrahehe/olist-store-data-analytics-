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
```

<img width="584" height="377" alt="Снимок экрана 2025-09-27 в 20 18 07" src="https://github.com/user-attachments/assets/d2517229-bb17-45a7-a434-a2f4f3ab4316" />


---

## 4. SQL Queries & Analytics
Queries were executed in pgAdmin (Query Tool) (queries.sql)


Two types of queries were written:
- Basic checks:
SELECT * FROM table LIMIT 10;
Filtering with WHERE and sorting with ORDER BY
Aggregations with COUNT, AVG, MIN, MAX
Example JOIN between tables
- 10 analytical queries 
Topics include:
Orders by status
Average monthly order value
Top sellers by sales
Unique customers by state
Average review scores by product category
Late deliveries percentage
Average delivery time
Products by category
Average freight value by seller state
Top customers by total spending


👉 All queries are stored in **queries.sql** with short comments.

---

## 🔹 5. Python Integration

- A script **main.py** was written in Python to connect to the **olist_db** database.  
- Library used: **psycopg2-binary**.  
- The script executes several SQL queries from **queries.sql** and displays the results in the terminal.  

### 📌 How to run the script
1. Install dependencies:
   ```bash
   pip install psycopg2-binary


