# Lab 1 — ETL Pipeline (Theory)

## What is a Data Platform?

A data platform is technology that collects, stores, and processes data so that it is correct, accessible, and reliable to use.

## Data Platform Layers

A data platform is built up in layers. Each layer has a specific job:

### Ingestion

How data comes into the platform. It could be from files, APIs, databases, or other systems.

In this lab, ingestion is when we read the CSV file:

```python
df = pd.read_csv("data.csv", sep=";")
```

### Storage

Where data is saved. There are three main types:

- **Data Warehouse** — stores structured data that is ready for analysis and reports (like SQL databases)
- **Data Lake** — stores large amounts of raw data in different formats, both structured and unstructured
- **Data Lakehouse** — a combination of both, flexible storage with better structure and performance

In this lab, storage is the Pandas DataFrame — our data lives in memory as a 2D table (rows and columns), similar to a spreadsheet.

### Transformation

How data is processed. This means turning raw data into something usable: cleaning, sorting, merging, and adapting.

In this lab, transformation is everything I do to clean the data:

```python
df["name"] = df["name"].str.strip().str.title()
df["currency"] = df["currency"].str.strip().str.upper()
df["price"] = pd.to_numeric(df["price"], errors="coerce")
```

### Access (BI & Analytics)

Where insights are derived from the data. This is where the data becomes useful for decisions.

In this lab, access is when we generate `analytics_summary.csv` with average price, median price, and product counts.

## ETL — Extract, Transform, Load

ETL is a pattern for how data moves through a pipeline:

### Extract

Raw data is extracted from different sources — databases, files, APIs, SaaS platforms. You pull the data out of wherever it lives.

In this lab:

```python
df = pd.read_csv("data.csv", sep=";")
```

### Transform

This is where we clean, validate, flag, and reject data before it goes to its final destination.

In this lab, Pandas is our staging area. We do all the cleaning work in a DataFrame before saving.

### Load

The cleaned data is loaded into the warehouse or system after transformation. Only clean, validated data gets through.

In this lab:

```python
summary.to_csv("analytics_summary.csv", index=False)
```

In a real project, this step could use Psycopg3 to load data into a PostgreSQL database instead of saving to CSV.

## ETL vs ELT — What's the Difference?

The key difference: in ETL you clean data before loading it (Python/Pandas does the work). In ELT you load raw data first, then clean it inside the database (tools like dbt handle the transformation).

This lab uses ETL because I transform with Pandas first, then save the clean result into csv files.

## Transform — Flag — Reject

This is the core framework for handling data quality. There are four possible outcomes when looking at a piece of data:

### OK Data

Example: `{"id": "SKU-1009", "name": "socks", "price": 99, "currency": "SEK"}` — everything is correct.

### Clean/Transform (>>)

I can fix the format without changing the meaning.

Example: `" shoes "` -> `"Shoes"` - we trim whitespace and capitalize. The meaning stays the same. Or `"sek"` -> `"SEK"` -> we uppercase the currency. No meaning change.

### Flag (! or ?)

Something looks suspicious, but it could be valid. I mark it and decide later.

Example: `{"name": "Shoes", "price": -799}` — could be a refund, an error, or a discount. Intent is unclear, so I flag it.

Another example: `bananas: 4828kr` — weird price for bananas, but not impossible. I flag it, I don't reject it.

### Reject (X)

Impossible to process without guessing. The data breaks rules and can't be fixed safely.

Examples: missing ID (no identity), negative price (removing minus changes meaning), price of 999999 (clearly wrong).

In this lab, we define all reject conditions in one place:

```python
reject_condition = (
    df["id"].isna() |
    df["name"].isna() |
    (df["price"] < 0) |
    (df["price"] > 100000)
)
df_rejected = df[reject_condition].copy()
df_clean = df[~reject_condition].copy()
```

## Technologies

### Pandas

A Python library for reading, cleaning, and analyzing data. It uses DataFrames — 2D tables (like spreadsheets) that can store different data types in columns. Pandas supports many file formats: CSV, JSON, Excel, Parquet, SQL, HTML, and more.

### Psycopg3

A Python library for connecting to PostgreSQL databases. It supports bulk data storage, transactions, connection pools, and JSONB. In this lab we saved to CSV files, but in a real project I would use Psycopg3 to load the clean data into PostgreSQL.

Why Psycopg3: bulk storage, safer transactions, cleaner code, better JSON support, row factories (get dicts or Pydantic models directly instead of `row[0]`), and async support.

### Pydantic (Bonus)

A Python library for data validation using schemas. You define what data should look like — types, required fields, constraints — and Pydantic checks if the data matches. If it doesn't match, it raises an error.

Example: if you define `price: float`, Pydantic will reject `price: "free"` automatically. It works together with FastAPI for API validation.
