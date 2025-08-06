import pandas as pd
from pathlib import Path

pasta = Path(r"data")

# Usa glob() do objeto Path de pathlib para conseguir o path para todos os arquivos CSV entre 2003 e 2020
arquivos_csv = sorted(
    [arq for arq in pasta.glob("recife-dados-despesas-*.csv") 
     if "2003" <= arq.stem.split('-')[-1] <= "2020"]
) 

lista_dfs = []

# Tabelas são carregads como dataframes e armazenadas na lista
for arq in arquivos_csv:
    data_frame = pd.read_csv(arq, sep=';', encoding='utf-8') 
    lista_dfs.append(data_frame)

# Concatenação das tabelas na lista
df_final = pd.concat(lista_dfs) 

# Salva dataframe unificado para transformação
df_final.to_csv("despesas_recife.csv",index=False)
