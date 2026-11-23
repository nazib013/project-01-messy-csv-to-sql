DROP TABLE IF EXISTS cafe_sales;

CREATE TABLE cafe_sales (
    transaction_id   TEXT PRIMARY KEY,
    item             TEXT,
    quantity         INTEGER CHECK (quantity > 0),
    price_per_unit   REAL    CHECK (price_per_unit > 0),
    total_spent      REAL    CHECK (total_spent > 0),
    payment_method   TEXT,
    location         TEXT,
    transaction_date TEXT
);