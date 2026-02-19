import pandas as pd

## ========================================
## EXTRACT — Read raw data
## ========================================
# From Lecture #7: dataframe = pd.read_csv("data.csv")
# Our file uses semicolon (;) as separator

df = pd.read_csv("data.csv", sep=";")

print("Columns:", list(df.columns))
print("Total rows:", len(df))


## ========================================
## TRANSFORM — Clean the data
## ========================================
# From Lecture #7 (String Structurizing):
#   dirty_df["name"] = dirty_df["name"].astype("string")
#   dirty_df["name"] = dirty_df["name"].str.strip()
#   dirty_df["name"] = dirty_df["name"].str.title()
# From Lecture #6: "Trim name, convert price to numbers, uppercase currency."

# 1. Clean "name"
df["name"] = df["name"].astype("string").str.strip().str.title()

# 2. Clean "id"
df["id"] = df["id"].astype("string").str.strip()

# 3. Clean "currency"
df["currency"] = df["currency"].astype("string").str.strip().str.upper()

# 4. Normalize dates (replace / with -)
df["created_at"] = df["created_at"].astype("string").str.strip()
df["created_at"] = df["created_at"].str.replace("/", "-", regex=False)

# 5. Convert "price" to number
df["price"] = pd.to_numeric(df["price"], errors="coerce")

print("\n=== AFTER TRANSFORM ===")
print(df.head(10))


## ========================================
## FLAG — Mark possible problems
## ========================================
# From Lecture #7 (Flagging with Columns):
#   missing_df["price_missing"] = missing_df["price"].isna()

df["id_missing"] = df["id"].isna()
df["name_missing"] = df["name"].isna()
df["price_missing"] = df["price"].isna()
df["currency_missing"] = df["currency"].isna()
df["negative_price"] = df["price"] < 0  # -> REJECT (impossible to fix)
df["high_price"] = df["price"] > 10000  # -> FLAG (suspicious, could be luxury)
df["zero_price"] = df["price"] == 0  # -> FLAG (free? or error?)

print("\n=== FLAGGED PROBLEMS ===")
print(f"Missing ID:        {df['id_missing'].sum()}")
print(f"Missing name:      {df['name_missing'].sum()}")
print(f"Missing price:     {df['price_missing'].sum()}")
print(f"Missing currency:  {df['currency_missing'].sum()}")
print(f"Negative price:    {df['negative_price'].sum()}")
print(f"High price:        {df['high_price'].sum()}")
print(f"Price = 0:         {df['zero_price'].sum()}")


## ========================================
## REJECT — Reject impossible values
## ========================================
# From Lecture #6 (Transform - Flag - Reject):
#   - No identity (missing id) -> can't connect to Primary_Key
#   - Unusable data (missing name)
#   - Impossible values (negative price, price > 100k)
# If something is impossible to process, without changing the value -> reject it"

# Define all reject conditions in one place
reject_condition = (
    df["id"].isna() | df["name"].isna() | (df["price"] < 0) | (df["price"] > 100000)
)

# Separate into valid and rejected
df_rejected = df[reject_condition].copy()
df_clean = df[~reject_condition].copy()

# Add rejection reasons
df_rejected["reject_reason"] = ""
df_rejected.loc[df_rejected["id"].isna(), "reject_reason"] += "missing_id; "
df_rejected.loc[df_rejected["name"].isna(), "reject_reason"] += "missing_name; "
df_rejected.loc[df_rejected["price"] < 0, "reject_reason"] += "negative_price; "
df_rejected.loc[df_rejected["price"] > 100000, "reject_reason"] += "impossible_price; "

print(f"\nClean products: {len(df_clean)}")
print(f"Rejected:       {len(df_rejected)}")
print(df_rejected[["id", "name", "price", "reject_reason"]])

## ========================================
## LOAD — Generate output CSV files
## ========================================
# From Lecture #7: summary.to_csv("output.csv", index=False)
# Utility Methods: .mean(), .median(), .max(), .min()

df_with_price = df_clean[df_clean["price"].notna()]

# --- analytics_summary.csv ---
summary = pd.DataFrame(
    [
        {
            "average_price": round(df_with_price["price"].mean(), 2),
            "median_price": round(df_with_price["price"].median(), 2),
            "total_products": len(df_clean),
            "products_missing_price": int(df_clean["price_missing"].sum()),
        }
    ]
)

summary.to_csv("analytics_summary.csv", index=False)
print("\nanalytics_summary.csv saved!")
print(summary)

# --- price_analysis.csv (BONUS) ---
# Deviant products come from what was FLAGGED

# Top 10 most expensive products
top_10_expensive = df_with_price.nlargest(10, "price")[
    ["id", "name", "price", "currency"]
]

# Deviant products — products that were flagged as suspicious
deviant_products = df_with_price[
    df_with_price["high_price"] | df_with_price["zero_price"]
][["id", "name", "price", "currency", "high_price", "zero_price"]]

# Combine both into one file
top_10_expensive["category"] = "most_expensive"
deviant_products["category"] = "most_deviant"

price_analysis = pd.concat([top_10_expensive, deviant_products], ignore_index=True)
price_analysis.to_csv("price_analysis.csv", index=False)

print("\nprice_analysis.csv saved!")
print(price_analysis)

# --- rejected_products.csv (BONUS) ---
df_rejected[["id", "name", "price", "currency", "reject_reason"]].to_csv(
    "rejected_products.csv", index=False
)
print("\nrejected_products.csv saved!")
