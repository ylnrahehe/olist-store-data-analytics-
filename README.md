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


<img width="600" height="405" alt="Снимок экрана 2025-09-27 в 20 34 50" src="https://github.com/user-attachments/assets/affd1437-a646-4333-9054-6fe1a1074820" />


👉 All queries are stored in **queries.sql** with short comments.

---

## 🔹 5. Python Integration

- A script **main.py** was written in Python to connect to the **olist_db** database.  
- Library used: **psycopg2-binary**.  
- The script executes several SQL queries from **queries.sql** and displays the results in the terminal.

<img width="456" height="459" alt="Снимок экрана 2025-10-04 в 02 58 17" src="https://github.com/user-attachments/assets/9775a3dc-fb3a-4a3e-a44d-c32647ce18b7" />


---

### 6. Visualizations (Matplotlib)  
Created **6 static charts** for business insights:  
- Orders by status  
- Average order value over time  
- Top sellers by total orders  
- Customers by state  
- Product review scores  
- Average delivery time (days)

<img width="635" height="474" alt="Снимок экрана 2025-10-04 в 02 52 33" src="https://github.com/user-attachments/assets/6950e15e-e375-44d0-ac1a-8068e3cee563" />

<img width="584" height="454" alt="Снимок экрана 2025-10-04 в 02 53 19" src="https://github.com/user-attachments/assets/d17e936f-6c76-47d6-b6d4-6aff75933e0f" />

---

### 7. Interactive Visualization (Plotly)  
- Built an **interactive scatter chart** with a **time slider** (`animation_frame` in Plotly).  
- Shows how customer orders evolve over time across different states.

---

### 8. Export to Excel with Formatting  
- Added function `export_to_excel()` with **openpyxl**.  
- Exports query results into `/exports/olist_report.xlsx`.



### 📌 How to run the script
1. Install dependencies:
   ```bash
   pip install psycopg2-binary

2. My **main.py** file is in folder named "python3", so maybe you will need this to run the file
   - python3 main.py

