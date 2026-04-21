import sqlite3
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# STEP 1: Connect database
conn = sqlite3.connect("sales.db")

# 👉 ADD YOUR CODE HERE 👇 (THIS PART)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    OrderID INT,
    Product TEXT,
    Category TEXT,
    Price REAL,
    Quantity INT,
    City TEXT,
    Date TEXT
)
""")

cursor.execute("DELETE FROM sales")

data = [
(1,'Laptop','Electronics',50000,2,'Mumbai','2024-01-10'),
(2,'Phone','Electronics',20000,3,'Delhi','2024-01-15'),
(3,'Shoes','Fashion',2000,5,'Kolkata','2024-02-05'),
(4,'Tshirt','Fashion',800,4,'Delhi','2024-02-20'),
(5,'Tablet','Electronics',30000,1,'Mumbai','2024-03-12'),
(6,'Laptop','Electronics',55000,1,'Bangalore','2024-03-25'),
(7,'Phone','Electronics',21000,2,'Mumbai','2024-04-10'),
(8,'Shoes','Fashion',1800,3,'Kolkata','2024-04-18'),
(9,'Tablet','Electronics',28000,2,'Delhi','2024-05-08'),
(10,'Tshirt','Fashion',750,6,'Bangalore','2024-05-20')
]

cursor.executemany("INSERT INTO sales VALUES (?,?,?,?,?,?,?)", data)
conn.commit()
# 👉 END OF YOUR ADDED CODE

# STEP 2: Load data
df = pd.read_sql_query("SELECT * FROM sales", conn)

# STEP 3: Analysis
df["Revenue"] = df["Price"] * df["Quantity"]

print("\nTotal Revenue:", df["Revenue"].sum())

top_products = df.groupby("Product")["Revenue"].sum().sort_values(ascending=False)
print("\nTop Products:\n", top_products)

city_sales = df.groupby("City")["Revenue"].sum()
print("\nCity-wise Sales:\n", city_sales)

# Monthly trend
df["Month"] = pd.to_datetime(df["Date"]).dt.month
monthly_sales = df.groupby("Month")["Revenue"].sum()

# STEP 4: Graphs
top_products.plot(kind="bar", title="Top Products")
plt.show(block=True)

city_sales.plot(kind="bar", title="City-wise Sales")
plt.show(block=True)

monthly_sales.plot(kind="line", marker='o', title="Monthly Sales Trend")
plt.show(block=True)

conn.close()