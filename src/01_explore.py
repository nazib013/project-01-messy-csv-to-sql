import pandas as pd

# Make the terminal show all columns instead of hiding some with "..."
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

df = pd.read_csv("data/raw/dirty_cafe_sales.csv")

print("SHAPE (rows, columns):")
print(df.shape)

print("\nFIRST 10 ROWS:")
print(df.head(10))

print("\nCOLUMN INFO:")
df.info()

print("\nMISSING VALUES PER COLUMN:")
print(df.isna().sum())