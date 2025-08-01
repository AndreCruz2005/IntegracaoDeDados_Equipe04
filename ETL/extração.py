import pandas as pd
from pathlib import Path


pasta = Path(r"C:\Users\joaov\OneDrive\Documentos\cin\repositorio\ProjetoIntegracao\IntegracaoDeDados_Equipe04\data")

#.glob um objeto pathlib e ele vai procurar os arquivos dentro da minha pasta 
arquivos_csv = sorted(pasta.glob("recife-dados-despesas-*.csv"))  # * é um wildcard pega tudo entre o nome e o csv



lista_dfs = []

for arq in arquivos_csv:
    data_frame = pd.read_csv(arq, sep=';', encoding= 'latin1') # latin1 serve para ler os caracteres especiais da língua
    
    lista_dfs.append(data_frame)

#junção das atabelas que estão na minha lista
df_final = pd.concat(lista_dfs) 


#salvando meu data frame na minha pasta para realizar a transformação depois
df_final.to_csv("despesas_recife.csv",index=False)



