import pandas as pd;

data = pd.read_excel('./buffANDdebuff.xlsx')

for index, row in data.iterrows():
    print(f"Card Type: {row['cardType']}, Function: {row['cardFunc']}")


print(data.iloc[0])

print(data)