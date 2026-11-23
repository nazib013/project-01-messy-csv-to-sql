import sqlite3
import sys
import pandas as pd

sql_file = sys.argv[1]  # the file name you type after the script name

with open(sql_file, encoding="utf-8") as f:
    text = f.read()

conn = sqlite3.connect("data/cafe.db")

for query in text.split(";"):
    # skip chunks that contain only comments or whitespace
    lines = [l for l in query.splitlines() if l.strip() and not l.strip().startswith("--")]
    if not lines:
        continue
    print("-" * 60)
    print(query.strip())
    print(pd.read_sql(query, conn).to_string(index=False))

conn.close()