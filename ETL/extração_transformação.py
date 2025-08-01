import pandas as pd
import re
from pathlib import Path
from Engine import engine
from sqlalchemy import types as satypes
from sqlalchemy.dialects.postgresql import NUMERIC  #tive que colocar para numeric para conseguir manipular os 3 valores

# Caminho dos arquivos
pasta = Path(r"C:\Users\joaov\OneDrive\Documentos\cin\repositorio\ProjetoIntegracao\IntegracaoDeDados_Equipe04\data")

COL_INT = ('empenho_ano', 'ano_movimentacao', 'mes_movimentacao', 'orgao_codigo', 'grupo_despesas_codigo','modalidade_aplicacao_codigo','elemento_codigo','subelemento_codigo','funcao_codigo','subfuncao_codigo','programa_codigo','acao_codigo','fonte_recurso_codigo','empenho_numero','subempenho', 'credor_codigo','modalidade_licitacao_codigo')
COL_NUMERIC = ('valor_empenhado', 'valor_liquidado', 'valor_pago')



def padronizar_colunas(df: pd.DataFrame) -> pd.DataFrame:

    # INT (nullable)
    for col in COL_INT:
        df[col] = df[col].astype(int)

    # NUMERIC (trata como float no pandas, mas envia como NUMERIC)
    for col in COL_NUMERIC:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace('.', '', regex=False)   # remove separador 
            .str.replace(',', '.', regex=False)  # vírgula vira ponto
            .str.replace(r'[^\d\.-]', '', regex=True)  # tira símbolos
        )
        df[col] = pd.to_numeric(df[col], errors='raise').astype(float).round(2)  # arredonda em 2 casas, errors = raise o pandas me avisa se tiver erro

    outras = [c for c in df.columns if c not in COL_INT + COL_NUMERIC]
    df[outras] = df[outras].astype(str)

    return df

def ler_e_concatenar(pasta: Path) -> pd.DataFrame:
    arquivos = sorted(pasta.glob("recife-dados-despesas-*.csv"))

    dfs = []
    for arq in arquivos:
        
        nome = arq.stem  # Ex: 'recife-dados-despesas-2023'
        ano = int(nome[-4:])  # Últimos 4 caracteres => o ano
        
        df = pd.read_csv(arq, sep=';', encoding='latin1', dtype=str)
        df = padronizar_colunas(df)
        df['ano_arquivo'] = ano  # adiciona a coluna com o ano

        dfs.append(df)
        print(f"Lido e padronizado: {arq.name} (linhas: {len(df)})")
    
    return pd.concat(dfs, ignore_index = True)

df_final = ler_e_concatenar(pasta)

# Tipos explícitos no Postgres
sql_types = {
    **{c: satypes.Integer() for c in COL_INT},
    **{c: NUMERIC(18, 2)    for c in COL_NUMERIC},  # << aqui vira Numeric Máximo 16 dígitos antes da vírgula, e 2 após a vírgula
}
if 'ano_arquivo' in df_final.columns:
    sql_types['ano_arquivo'] = satypes.Integer()

df_final.to_sql(
    'despesas',
    con=engine,
    if_exists='replace',
    index=False,
    dtype=sql_types
)

print(f"Pronto! {len(df_final)} linhas inseridas na tabela 'despesas'.")
