import pandas as pd

# Confere se todas as tabelas têm as mesmas colunas
tables = [pd.read_csv(f'data/recife-dados-despesas-{y}.csv', sep=';') for y in range(2003, 2024)]
columns = [t.columns for t in tables]
print('Tudo igual:', all(list(x) == list(columns[0]) for x in columns))