# Carga.py
import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv('df_transformado.csv')

usuario = 'postgres'
senha = 'Dovahkiin35$'
host = 'localhost'
porta = '5432'
banco = 'integracao_dados'
tabela = 'despesas'

engine = create_engine(f'postgresql://{usuario}:{senha}@{host}:{porta}/{banco}')

try:
    with engine.connect() as conn:
        print("Conexão estabelecida")
        df.to_sql(tabela, conn, if_exists='replace', index=False, chunksize=1000)
        print(f'Dados carregados com sucesso na tabela "{tabela}" do banco "{banco}".')
except Exception as e:
    print("Erro durante a carga:", e)
