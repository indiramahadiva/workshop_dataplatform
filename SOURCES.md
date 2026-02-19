# Lab 1 — Documentation Sources

## Tools

**Pandas** — Official docs: https://pandas.pydata.org/docs/
Getting started tutorials: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

**Git** — Official docs: https://git-scm.com/doc
GitHub docs: https://docs.github.com/en

---

## Pandas Methods Used

### Reading Data

`pd.read_csv()` — Reads a CSV file into a DataFrame
https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html

### String Methods

`df["col"].astype("string")` — Converts column to string type
https://pandas.pydata.org/docs/reference/api/pandas.Series.astype.html

`df["col"].str.strip()` — Removes whitespace from start and end
https://pandas.pydata.org/docs/reference/api/pandas.Series.str.strip.html

`df["col"].str.title()` — Capitalizes first letter of each word
https://pandas.pydata.org/docs/reference/api/pandas.Series.str.title.html

`df["col"].str.upper()` — Converts text to uppercase
https://pandas.pydata.org/docs/reference/api/pandas.Series.str.upper.html

`df["col"].str.replace()` — Replaces text in strings
https://pandas.pydata.org/docs/reference/api/pandas.Series.str.replace.html

### Type Conversion

`pd.to_numeric()` — Converts to numeric type. With `errors="coerce"`, invalid values become NaN
https://pandas.pydata.org/docs/reference/api/pandas.to_numeric.html

### Checking Missing Values

`df["col"].isna()` — Returns True where values are missing (NaN)
https://pandas.pydata.org/docs/reference/api/pandas.Series.isna.html

`df["col"].notna()` — Returns True where values exist (not NaN)
https://pandas.pydata.org/docs/reference/api/pandas.Series.notna.html

### Filtering and Selecting

`df.loc[]` — Access rows and columns by label or boolean mask
https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.loc.html

`df[condition]` — Boolean filtering, selects rows where condition is True
https://pandas.pydata.org/docs/user_guide/indexing.html#boolean-indexing

`df.copy()` — Creates an independent copy of a DataFrame
https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.copy.html

`df.nlargest()` — Returns the n rows with the largest values
https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.nlargest.html

`pd.concat()` — Combines multiple DataFrames into one
https://pandas.pydata.org/docs/reference/api/pandas.concat.html

### Aggregation / Utility Methods

`df["col"].mean()` — Calculates the average
https://pandas.pydata.org/docs/reference/api/pandas.Series.mean.html

`df["col"].median()` — Calculates the median (middle value)
https://pandas.pydata.org/docs/reference/api/pandas.Series.median.html

`df["col"].sum()` — Sums all values. For booleans it counts the number of True
https://pandas.pydata.org/docs/reference/api/pandas.Series.sum.html

`df["col"].max()` — Returns the highest value
https://pandas.pydata.org/docs/reference/api/pandas.Series.max.html

`df["col"].min()` — Returns the lowest value
https://pandas.pydata.org/docs/reference/api/pandas.Series.min.html

### Exporting Data

`df.to_csv()` — Saves a DataFrame to a CSV file
https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html

### DataFrame Creation

`pd.DataFrame()` — Creates a new DataFrame
https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html

---

## Python Built-in Functions Used

`round()` — Rounds to n decimal places
https://docs.python.org/3/library/functions.html#round

`int()` — Converts to integer
https://docs.python.org/3/library/functions.html#int

`len()` — Counts number of items (rows in a DataFrame)
https://docs.python.org/3/library/functions.html#len

`str()` — Converts to string
https://docs.python.org/3/library/functions.html#func-str

`print()` — Prints output to terminal
https://docs.python.org/3/library/functions.html#print

`f"..."` — F-strings for string formatting
https://docs.python.org/3/tutorial/inputoutput.html#fstring

---

## Related Technologies (from the course)

**Psycopg3** — Python library for connecting to PostgreSQL databases
Official docs: https://www.psycopg.org/psycopg3/docs/
Install guide: https://www.psycopg.org/psycopg3/docs/basic/install.html

**FastAPI** — Python web framework for building APIs
Official docs: https://fastapi.tiangolo.com/
