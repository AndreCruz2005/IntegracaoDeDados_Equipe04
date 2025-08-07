import pandas as pd

# Verifica as colunas do CSV
df = pd.read_csv('rawData/recife-dados-despesas-2008.csv', sep=';', encoding='latin1', nrows=0)
print("Colunas do CSV:")
for i, col in enumerate(df.columns):
    print(f"{i+1:2d}. {col}")

print(f"\nTotal de colunas: {len(df.columns)}")
