import pandas as pd

## EXTRACT — Read raw data ##

# sep=";" — this file uses semicolons as delimiters instead of commas.
# Without this, pandas would treat each entire row as one column.
# df.info() shows you the data types and how many non-null values each column has.
df = pd.read_csv("data.csv", sep=";")
print(df)
print(df.info())

## TRANSFORM — Clean data ##

# 1. Clean "name"
df["name"] = df["name"].astype("string")  # convert column to string type
df["name"] = df["name"].str.strip()  # remove spaces before/after
df["name"] = df["name"].str.title()  # capitalize each word

# 2. Clean "id"
df["id"] = df["id"].astype("string").str.strip()

# 3. Clean "currency"
df["currency"] = df["currency"].astype("string").str.strip().str.upper()

# 4. Normalize dates (replace / with -)
df["created_at"] = df["created_at"].astype("string").str.strip()
df["created_at"] = df["created_at"].str.replace("/", "-", regex=False)

# 5. Convert "price" to number
# We have values like "free" and "not_available" that would crash with astype(float)
# pd.to_numeric with errors="coerce" turns invalid values -> NaN instead of crashing
df["price"] = pd.to_numeric(df["price"], errors="coerce")

print(df.head(10))
print(df.dtypes)

## FLAG — Mark possible problems (suspicious but could be valid)  ##

df["id_missing"] = df["id"].isna()
df["name_missing"] = df["name"].isna()
df["price_missing"] = df["price"].isna()
df["currency_missing"] = df["currency"].isna()
df["negative_price"] = df["price"] < 0  # -> REJECT
df["high_price"] = df["price"] > 10000  # -> FLAG
df["zero_price"] = df["price"] == 0  # -> FLAG

print("=== FLAGGED PROBLEMS ===")
print(f"Missing ID:        {df['id_missing'].sum()}")
print(f"Missing name:      {df['name_missing'].sum()}")
print(f"Missing price:     {df['price_missing'].sum()}")
print(f"Missing currency:  {df['currency_missing'].sum()}")
print(f"Negative price:    {df['negative_price'].sum()}")
print(f"High price:        {df['high_price'].sum()}")
print(f"Price = 0:         {df['zero_price'].sum()}")

## REJECT (Reject impossible values) ##
df["reject_reason"] = ""

# No identity — can't connect to database (Primary Key)
df.loc[df["id_missing"], "reject_reason"] += "missing_id; "

# No name — data is unusable
df.loc[df["name_missing"], "reject_reason"] += "missing_name; "

# Negative price should be rejected,
df.loc[df["negative_price"], "reject_reason"] += "negative_price; "

# Impossible price — clearly wrong data (not just high, but beyond any real product)
df["impossible_price"] = df["price"] > 100000
df.loc[df["impossible_price"], "reject_reason"] += "impossible_price; "

# Mark which rows are rejected
df["is_rejected"] = df["reject_reason"] != ""

# Separate into clean and rejected DataFrames
df_clean = df[~df["is_rejected"]].copy()
df_rejected = df[df["is_rejected"]].copy()

print(f"\nClean products: {len(df_clean)}")
print(f"Rejected:       {len(df_rejected)}")
print(df_rejected[["id", "name", "price", "reject_reason"]])

## LOAD — Generate output CSV files ##
