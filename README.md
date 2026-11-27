# Messy CSV to SQL: Café Sales

Cleaning a deliberately messy café sales dataset with Python (pandas), loading it into SQLite, and answering business questions with SQL.

## The problem

The raw file has 10,000 transactions, but the data can't be trusted as it is:

- `ERROR` and `UNKNOWN` are typed into cells as if they were real values, so a normal empty-cell check misses them.
- Every column loads as text, including quantities, prices, totals, and dates.
- Payment method is 25.8% empty and location is 32.6% empty. Counting the junk values, that rises to 31.8% and 39.6%.

## Dataset

[Cafe Sales - Dirty Data for Cleaning Training](https://www.kaggle.com/datasets/ahmedmohamed2003/cafe-sales-dirty-data-for-cleaning-training) from Kaggle. The data is artificially generated, so the findings below demonstrate the method and say nothing about real café behaviour.

The raw file is not stored in this repo. Download it and save it as `data/raw/dirty_cafe_sales.csv`.

## What the pipeline does

1. **Profile** (`src/01` to `04`): row counts, missing values, duplicates, distinct values, and a check that quantity x price = total.
2. **Clean** (`src/05_clean.py`): turn `ERROR`/`UNKNOWN` into real NULLs, rename columns, fix data types, and recover missing values that other columns determine.
3. **Load** (`src/06_load_to_sqlite.py`): create the table from `sql/01_create_tables.sql` and load it into SQLite, then verify row counts.
4. **Analyze** (`sql/02_analysis.sql`, `sql/03_my_queries.sql`, run with `src/07_run_sql.py`): business questions answered in SQL.

## Key decisions

- **No rows deleted.** 10,000 rows in, 10,000 out.
- **Recover only what is certain.** Each item has exactly one price, and quantity x price = total held on all 8,544 rows where all three were known. Missing prices, totals, quantities, and some items were filled using those rules only.
- **Honest NULLs.** Payment method, location, and date can't be derived from other columns, so they stay NULL instead of being guessed.
- **Safety checks.** The cleaning script stops if the row count changes, IDs repeat, or quantity x price differs from total.
- **Database rules.** The table enforces a primary key and positive-value checks.

## Results of cleaning

| Column | Empty before | Empty after |
|---|---|---|
| item | 969 | 480 |
| quantity | 479 | 23 |
| price_per_unit | 533 | 6 |
| total_spent | 502 | 23 |
| payment_method | 3,178 | 3,178 |
| location | 3,961 | 3,961 |
| transaction_date | 460 | 460 |

## Findings

- Total revenue is 89,096, with an average sale of 8.93.
- Salad earns the most revenue (19,095). Coffee has the most transactions (1,291) but ranks sixth in revenue because it is cheap.
- In-store (3,017) and takeaway (3,022) sales are almost equal.
- Payment methods are split almost evenly (22.6% to 22.9% each), and 31.8% are unknown, so no preferred method can be claimed.
- Monthly revenue is flat (6,644 to 7,353). Friday is the busiest weekday (1,388 sales) and Tuesday the quietest (1,311), but the gap is too small to mean much.
- These flat results are expected, since the data is synthetic.

## Limitations

- 23 rows have no total and are left out of revenue sums.
- 460 rows have no date and are left out of the monthly and weekday queries.
- Weekdays are shown as numbers (0 = Sunday, 6 = Saturday).

## How to run

```
git clone https://github.com/YOUR-USERNAME/project-01-messy-csv-to-sql.git
cd project-01-messy-csv-to-sql
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

On Mac/Linux, activate with `source venv/bin/activate`. Then download the dataset into `data/raw/` and run:

```
python src/05_clean.py
python src/06_load_to_sqlite.py
python src/07_run_sql.py sql/02_analysis.sql
python src/07_run_sql.py sql/03_my_queries.sql
```

## Project structure

```
project-01-messy-csv-to-sql/
├── data/raw/              (not in repo: download the CSV here)
├── sql/
│   ├── 01_create_tables.sql
│   ├── 02_analysis.sql
│   └── 03_my_queries.sql
├── src/
│   ├── 01_explore.py to 04_check_rule.py
│   ├── 05_clean.py
│   ├── 06_load_to_sqlite.py
│   └── 07_run_sql.py
├── requirements.txt
└── README.md
```