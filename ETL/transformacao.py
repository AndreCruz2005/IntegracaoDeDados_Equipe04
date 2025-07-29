import pandas as pd
import re
from pathlib import Path
from Engine import engine
from sqlalchemy import types as satypes
from sqlalchemy.dialects.postgresql import NUMERIC  #tive que colocar para numeric para conseguir manipular os 3 valores

# Caminho dos arquivos
pasta = Path(r"C:\Users\joaov\OneDrive\Documentos\cin\repositorio\ProjetoIntegracao\IntegracaoDeDados_Equipe04\data")

COL_INT = ('empenho_ano', 'ano_movimentacao', 'mes_movimentacao')
COL_NUMERIC = ('valor_empenhado', 'valor_liquidado', 'valor_pago')  # agora serão NUMERIC

def padronizar_colunas(df: pd.DataFrame) -> pd.DataFrame:
    for col in COL_INT + COL_NUMERIC:
        if col not in df.columns:
            df[col] = pd.NA

    # INT (nullable)
    for col in COL_INT:
        df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')

    # NUMERIC (trata como float no pandas, mas envia como NUMERIC)
    for col in COL_NUMERIC:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace('.', '', regex=False)   # remove separador 
            .str.replace(',', '.', regex=False)  # vírgula vira ponto
            .str.replace(r'[^\d\.-]', '', regex=True)  # tira símbolos
        )
        df[col] = pd.to_numeric(df[col], errors='coerce').astype(float).round(2)  # arredonda em 2 casas

    outras = [c for c in df.columns if c not in COL_INT + COL_NUMERIC]
    df[outras] = df[outras].astype(str)

    return df

def ler_e_concatenar(pasta: Path) -> pd.DataFrame:
    arquivos = sorted(pasta.glob("recife-dados-despesas-*.csv"))
    if not arquivos:
        raise FileNotFoundError("Nenhum arquivo encontrado com o padrão 'recife-dados-despesas-*.csv'.")

    dfs = []
    for arq in arquivos:
        m = re.search(r"(\d{4})", arq.stem)
        ano = m.group(1) if m else None

        df = pd.read_csv(arq, sep=';', encoding='latin1', dtype=str)
        df = padronizar_colunas(df)

        if ano is not None:
            df['ano_arquivo'] = int(ano)

        dfs.append(df)
        print(f"Lido e padronizado: {arq.name} (linhas: {len(df)})")

    return pd.concat(dfs, ignore_index=True)

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
