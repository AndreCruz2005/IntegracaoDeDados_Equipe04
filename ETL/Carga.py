import pandas as pd
from sqlalchemy import create_engine

# Lê o CSV transformado
df = pd.read_csv('df_transformado.csv')

# Configurações de conexão com o banco PostgreSQL
usuario = 'postgres'
senha = 'Dovahkiin35$'
host = 'localhost'
porta = '5432'
banco = 'integracao_dados'
tabela = 'despesas'

# Cria a string de conexão (usando sqlalchemy)
engine = create_engine(f'postgresql://{usuario}:{senha}@{host}:{porta}/{banco}')

# Faz a carga para a tabela desejada (substitui se já existir)
df.to_sql(tabela, engine, if_exists='replace', index=False)

print(f'Dados carregados com sucesso na tabela "{tabela}" do banco "{banco}".')
