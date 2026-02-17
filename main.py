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
