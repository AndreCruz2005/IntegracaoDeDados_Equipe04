import pandas as pd
import os

# Criando Diretório com as tabelas CSV
diretorio = r'C:\Users\Adriano\Documents\GitHub\IntegracaoDeDados_Equipe04\Dados'

# Colocando em arquivos_csv os arquivos que terminam com .csv usando List Comprehension
arquivos_csv = [f for f in os.listdir(diretorio) if f.endswith('.csv')]

# Lista para armazenar dataframes
dfs = []

for arquivo in arquivos_csv:
    caminho_arquivo = os.path.join(diretorio, arquivo)
    # Lendo o CSV e armazenando em df
    df = pd.read_csv(caminho_arquivo, sep = ';', header = None, encoding = 'utf-8')
    dfs.append(df)

# Concatenando todos os Dataframes em um só
df_total = pd.concat(dfs, ignore_index = True)


