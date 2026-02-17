import pandas as pd

## EXTRACT — Read raw data ##

# sep=";" — this file uses semicolons as delimiters instead of commas.
# Without this, pandas would treat each entire row as one column.
# df.info() shows you the data types and how many non-null values each column has.
df = pd.read_csv("data.csv", sep=";")
print(df)
print(df.info())
