import pandas as pd
import re
from pathlib  import Path
from Engine import engine


# vou colocar as tabelas do governo no banco para testar
pasta = Path("C:\\Users\\joaov\\OneDrive\\Documentos\\cin\\repositorio\\ProjetoIntegracao\\IntegracaoDeDados_Equipe04\\data")


#  Pega todos os arquivos do padrão desejado. O método .glob() procura arquivos ou pastas dentro de um diretório, com base em um padrão e sorted ordena.
arquivos = sorted(pasta.glob("recife-dados-despesas-*.csv"))

for arq in arquivos:
    #  Extrai o ano do nome do arquivo
    m = re.search(r"(\d{4})", arq.stem)
    if not m:
        print(f"Pulando {arq.name}: não encontrei ano no nome.")
        continue
    ano = m.group(1)

    #usando o pandas para ler um arquivo CSV e carregar os dados dele dentro de um DataFram
    df = pd.read_csv(arq, sep=';', encoding='latin1')

    #  Define o nome da tabela
    tabela = f"despesas_{ano}"

    #Envia para o PostgreSQL (cria/replace a tabela)
    df.to_sql(tabela, con=engine, if_exists='replace', index=False)

    print(f" {arq.name} → tabela '{tabela}' criada/enviada.")

print("Fim!")