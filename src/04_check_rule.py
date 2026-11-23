import pandas as pd

df = pd.read_csv("data/raw/dirty_cafe_sales.csv")

# errors="coerce" turns ERROR/UNKNOWN into empty values
qty = pd.to_numeric(df["Quantity"], errors="coerce")
price = pd.to_numeric(df["Price Per Unit"], errors="coerce")
total = pd.to_numeric(df["Total Spent"], errors="coerce")

# Rows where all three numbers are known
known = qty.notna() & price.notna() & total.notna()
print("Rows with all three known:", known.sum())

# Of those, how many break the rule? (tiny tolerance for decimal rounding)
broken = known & ((qty * price - total).abs() > 0.01)
print("Rows where Quantity x Price != Total:", broken.sum())