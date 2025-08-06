import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

# Configuração da conexão com banco PostgreSQL usando variáveis de ambiente
# Abordagem ELT: Extract, Load, Transform - carrega dados brutos primeiro
engine = create_engine(f"postgresql+psycopg2://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}/{os.getenv('DATABASE_URL')}")

# Lista dos anos que serão processados na abordagem ELT
anos = [2008, 2009, 2010, 2011, 2012]

print("=== INICIANDO CARGA ELT - DADOS BRUTOS ===")
print("Carregando dados sem transformação na tabela raw_despesas")

for ano in anos:
    print(f"Processando ano {ano}...")
    caminho = f"../data/recife-dados-despesas-{ano}.csv"
    
    # Extração: lê os dados CSV sem nenhuma transformação
    # Mantém encoding latin1 para preservar caracteres especiais originais
    df = pd.read_csv(caminho, sep=';', encoding='latin1')
    
    # Adiciona coluna de controle para identificar o ano na tabela unificada
    df["ano"] = ano
    
    # Load: insere dados brutos diretamente no banco para posterior transformação
    # if_exists="append" adiciona os dados sem sobrescrever registros existentes
    df.to_sql("raw_despesas", con=engine, if_exists="append", index=False)
    
    print(f"  ✓ {len(df)} registros carregados para {ano}")

print("\n=== CARGA ELT CONCLUÍDA ===")
print("Dados brutos disponíveis na tabela 'raw_despesas' para transformação")
