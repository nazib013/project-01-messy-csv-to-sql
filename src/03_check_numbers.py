import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

df = pd.read_csv("data/raw/dirty_cafe_sales.csv")

# 1. Every distinct value in the number columns
for col in ["Quantity", "Price Per Unit", "Total Spent"]:
    print(f"\nVALUE COUNTS: {col}")
    print(df[col].value_counts(dropna=False))

# 2. Does each item always have the same price?
print("\nPRICES PER ITEM:")
print(df.groupby("Item")["Price Per Unit"].unique())

# 3. Dates: sample values, and which ones fail to convert
print("\nSAMPLE DATES:")
print(df["Transaction Date"].sample(10, random_state=1))

dates = pd.to_datetime(df["Transaction Date"], errors="coerce")
print("\nDATES THAT FAIL TO CONVERT:")
print(df.loc[dates.isna(), "Transaction Date"].value_counts(dropna=False))
print("\nDATE RANGE:", dates.min(), "to", dates.max())