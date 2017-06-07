import pandas as pd

x = 0
for column in df:
    if pd.isnull(column).any():
        logicalMissing = pd.isnull(column)
        x = x + 1
        df.insert(x, [column.name + '_MissingLogical'], logicalMissing)
    x = x + 1

