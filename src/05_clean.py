import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

# Each item has exactly one price (found in 03_check_numbers.py)
PRICE_BY_ITEM = {
    "Cake": 3.0, "Coffee": 2.0, "Cookie": 1.0, "Juice": 3.0,
    "Salad": 5.0, "Sandwich": 4.0, "Smoothie": 4.0, "Tea": 1.5,
}

# Only prices owned by ONE item can be turned back into an item.
# 3.0 (Cake/Juice) and 4.0 (Sandwich/Smoothie) are shared, so they are left out.
ITEM_BY_PRICE = {1.0: "Cookie", 1.5: "Tea", 2.0: "Coffee", 5.0: "Salad"}

# 1. LOAD: treat ERROR and UNKNOWN as empty values from the start
df = pd.read_csv("data/raw/dirty_cafe_sales.csv", na_values=["ERROR", "UNKNOWN"])
rows_in = len(df)

# 2. RENAME columns to snake_case (no spaces, easier in SQL)
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
empty_before = df.isna().sum()

# 3. RECOVER missing values that the other columns determine (order matters)
df["price_per_unit"] = df["price_per_unit"].fillna(df["item"].map(PRICE_BY_ITEM))
df["price_per_unit"] = df["price_per_unit"].fillna(df["total_spent"] / df["quantity"])
df["total_spent"] = df["total_spent"].fillna(df["quantity"] * df["price_per_unit"])
df["quantity"] = df["quantity"].fillna((df["total_spent"] / df["price_per_unit"]).round())
df["item"] = df["item"].fillna(df["price_per_unit"].map(ITEM_BY_PRICE))

# 4. FIX TYPES
df["quantity"] = df["quantity"].astype("Int64")  # whole number that allows empty
df["price_per_unit"] = df["price_per_unit"].round(2)
df["total_spent"] = df["total_spent"].round(2)
df["transaction_date"] = pd.to_datetime(
    df["transaction_date"], format="%Y-%m-%d", errors="coerce"
).dt.strftime("%Y-%m-%d")  # back to plain text, because SQLite has no date type

# 5. CHECKS: the script stops with an error if any of these fail
assert len(df) == rows_in, "Row count changed!"
assert df["transaction_id"].is_unique, "Duplicate transaction IDs!"
complete = df.dropna(subset=["quantity", "price_per_unit", "total_spent"])
assert ((complete["quantity"] * complete["price_per_unit"] - complete["total_spent"]).abs() < 0.01).all(), "Quantity x Price != Total!"

# 6. REPORT
report = pd.DataFrame({"empty_before": empty_before, "empty_after": df.isna().sum()})
print(f"Rows in: {rows_in} | Rows out: {len(df)}")
print(report)
print("\nDATA TYPES:")
print(df.dtypes)

# 7. SAVE
df.to_csv("data/processed/cafe_sales_clean.csv", index=False)
print("\nSaved to data/processed/cafe_sales_clean.csv")