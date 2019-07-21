# reads the table into pandas  dataframe for easier processing

import pandas as pd


tableList = pd.read_html("./table.html")

df = tableList[0]

print(df)

print(df.dtypes)

columns = list(df)[2:]

print(columns)
print()

illegalArgs = ["NOT", "REMOVED IN Linux"]

for col in columns:
    df[col] = df[col].astype(str)
    for ill in illegalArgs:
    	df = df[df[col].str.contains(ill) == False]

print(df.loc[df["Number"] == 174])
print()
print(df.dtypes)

df.to_pickle("./table.pkl")
