import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

df = pd.read_csv("data/raw/dirty_cafe_sales.csv")

print("COLUMN NAMES:")
print(df.columns.tolist())

# 1. Missing values as a percentage of all rows
print("\nMISSING VALUES (%):")
print((df.isna().mean() * 100).round(1))

# 2. Is Transaction ID really unique?
print("\nTRANSACTION ID CHECK:")
print("Total rows:", len(df))
print("Unique IDs:", df["Transaction ID"].nunique())

# 3. Rows that are exact copies of other rows
print("\nDUPLICATE ROWS:", df.duplicated().sum())

# 4. Every distinct value in the text columns, with counts
for col in ["Item", "Payment Method", "Location"]:
    print(f"\nVALUE COUNTS: {col}")
    print(df[col].value_counts(dropna=False))

# 5. What type pandas thinks each column is
print("\nDATA TYPES:")
print(df.dtypes)