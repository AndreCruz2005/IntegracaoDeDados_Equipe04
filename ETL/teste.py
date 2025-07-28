import pandas as pd

# Carregar o arquivo CSV
df = pd.read_csv('recife-dados-despesas-2003.csv', sep=';', encoding='latin-1')

# Mostrar as primeiras linhas para verificar
print(df.head())

# Verificar informações básicas do dataframe
print(df.info())

# Exemplo de análise: total de despesas por órgão
total_por_orgao = df.groupby('orgao_nome')['valor_pago'].sum()
print(total_por_orgao)