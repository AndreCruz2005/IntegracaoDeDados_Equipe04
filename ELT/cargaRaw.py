import os
import sys
import pandas as pd

parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_folder)
from postgres.engine import engine

# Lista dos anos que serão processados na abordagem ELT
anos = (2003, 2004, 2005, 2018, 2019, 2020)

print("=== INICIANDO CARGA ELT - DADOS BRUTOS ===")
print("Carregando dados sem transformação na tabela raw_despesas")

for ano in anos:
    print(f"Processando ano {ano}...")
    caminho = f"data/recife-dados-despesas-{ano}.csv"
    
    # Extração: lê os dados CSV sem nenhuma transformação
    df = pd.read_csv(caminho, sep=';', encoding='utf-8')    
    
    # Load: insere dados brutos diretamente no banco para posterior transformação
    # if_exists="append" adiciona os dados sem sobrescrever registros existentes
    if ano < 2016:
        df.to_sql("raw_despesas_pre_2016", con=engine, if_exists="append", index=False)
    else:
        # Para anos >= 2016, cria uma tabela separada para evitar problemas com vírgula/ponto
        df.to_sql("raw_despesas_pos_2016", con=engine, if_exists="append", index=False)
    
    print(f"  ✓ {len(df)} registros carregados para {ano}")

print("\n=== CARGA ELT CONCLUÍDA ===")
print("Dados brutos disponíveis nas tabelas 'raw_despesas_pre_2016' e 'raw_despesas_pos_2016' para transformação")
