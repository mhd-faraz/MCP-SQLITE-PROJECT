import sqlite3
import pandas as pd

# ----------------------------------------
# STEP A: Database file se connection karo
# ----------------------------------------
conn = sqlite3.connect("sales.db")

# ----------------------------------------
# STEP B: Sales data banao — 12 rows
# ----------------------------------------
data = {
    "month": [
        "2024-01", "2024-01", "2024-01",
        "2024-02", "2024-02", "2024-02",
        "2024-03", "2024-03", "2024-03",
        "2024-04", "2024-04", "2024-04"
    ],
    "product": [
        "Laptop", "Phone", "Tablet",
        "Laptop", "Phone", "Tablet",
        "Laptop", "Phone", "Tablet",
        "Laptop", "Phone", "Tablet"
    ],
    "region": [
        "North", "South", "East",
        "North", "South", "East",
        "West",  "North", "South",
        "East",  "West",  "North"
    ],
    "units": [
        10, 25, 15,
        12, 30, 18,
        9,  28, 20,
        14, 22, 17
    ],
    "revenue": [
        500000, 375000, 210000,
        600000, 450000, 252000,
        450000, 420000, 280000,
        700000, 330000, 238000
    ]
}

# ----------------------------------------
# STEP C: Dictionary se DataFrame banao
# ----------------------------------------
df = pd.DataFrame(data)

# ----------------------------------------
# STEP D: DataFrame ko database mein dalo
# ----------------------------------------
df.to_sql("sales", conn, if_exists="replace", index=False)

# ----------------------------------------
# STEP E: Verify karo — wapas padho DB se
# ----------------------------------------
result = pd.read_sql("SELECT * FROM sales", conn)
print("Database ready! Total rows:", len(result))
print("\nSample data:")
print(result.head())

# ----------------------------------------
# STEP F: Connection band karo
# ----------------------------------------
conn.close()
print("\nsales.db file ban gayi!")