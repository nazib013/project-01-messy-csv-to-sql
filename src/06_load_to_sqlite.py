import sqlite3
import pandas as pd

DB_PATH = "data/cafe.db"

# 1. Read the cleaned data (quantity must stay a whole number)
df = pd.read_csv("data/processed/cafe_sales_clean.csv", dtype={"quantity": "Int64"})

# 2. Connect to the database (the file is created if it doesn't exist)
conn = sqlite3.connect(DB_PATH)

# 3. Create the table from the SQL file
with open("sql/01_create_tables.sql", encoding="utf-8") as f:
    conn.executescript(f.read())

# 4. Insert the rows (empty values become NULL automatically)
df.to_sql("cafe_sales", conn, if_exists="append", index=False)
conn.commit()

# 5. Verify the load
rows_in_db = conn.execute("SELECT COUNT(*) FROM cafe_sales").fetchone()[0]
print("Rows in CSV:", len(df))
print("Rows in database:", rows_in_db)
assert rows_in_db == len(df), "Row counts do not match!"

print("\nFirst 5 rows from the database:")
for row in conn.execute("SELECT * FROM cafe_sales LIMIT 5"):
    print(row)

# COUNT(*) counts all rows, COUNT(column) counts only non-NULL values,
# so the difference is the number of NULLs
nulls = pd.read_sql(
    """
    SELECT COUNT(*) - COUNT(item)             AS item,
           COUNT(*) - COUNT(quantity)         AS quantity,
           COUNT(*) - COUNT(price_per_unit)   AS price_per_unit,
           COUNT(*) - COUNT(total_spent)      AS total_spent,
           COUNT(*) - COUNT(payment_method)   AS payment_method,
           COUNT(*) - COUNT(location)         AS location,
           COUNT(*) - COUNT(transaction_date) AS transaction_date
    FROM cafe_sales
    """,
    conn,
)
print("\nNULLs per column in the database:")
print(nulls.T)

conn.close()