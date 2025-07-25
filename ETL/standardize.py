import pandas as pd
import re
from pathlib import Path
from Engine import engine
from sqlalchemy import types as satypes

# Caminho dos arquivos
pasta = Path(r"C:\Users\joaov\OneDrive\Documentos\cin\repositorio\ProjetoIntegracao\IntegracaoDeDados_Equipe04\data")

COL_INT = ('empenho_ano', 'ano_movimentacao', 'mes_movimentacao')
COL_FLOAT = ('valor_empenhado', 'valor_liquidado', 'valor_pago')

def padronizar_colunas(df: pd.DataFrame) -> pd.DataFrame:
    # Garante que todas as colunas existam (caso algum CSV venha faltando algo)
    for col in COL_INT + COL_FLOAT:
        if col not in df.columns:
            df[col] = pd.NA

    # INT (nullable)
    for col in COL_INT:
        df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')

    # FLOAT
    for col in COL_FLOAT:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace('.', '', regex=False)   # remove separador de milhar
            .str.replace(',', '.', regex=False)  # vírgula -> ponto
            .str.replace(r'[^\d\.-]', '', regex=True)  # tira símbolos
        )
        df[col] = pd.to_numeric(df[col], errors='coerce').astype(float)

    # Demais -> string
    outras = [c for c in df.columns if c not in COL_INT + COL_FLOAT]
    df[outras] = df[outras].astype(str)

    return df

def ler_e_concatenar(pasta: Path) -> pd.DataFrame:
    arquivos = sorted(pasta.glob("recife-dados-despesas-*.csv"))
    if not arquivos:
        raise FileNotFoundError("Nenhum arquivo encontrado com o padrão 'recife-dados-despesas-*.csv'.")

    dfs = []
    for arq in arquivos:
        # extrai ano só se quiser guardar (opcional)
        m = re.search(r"(\d{4})", arq.stem)
        ano = m.group(1) if m else None

        df = pd.read_csv(arq, sep=';', encoding='latin1', dtype=str)  # lê tudo como str para depois padronizar
        df = padronizar_colunas(df)

        if ano is not None:
            df['ano_arquivo'] = int(ano)  # pode ser útil em consultas

        dfs.append(df)
        print(f"Lido e padronizado: {arq.name} (linhas: {len(df)})")

    return pd.concat(dfs, ignore_index=True)

# Lê tudo
df_final = ler_e_concatenar(pasta)

# Mapeia tipos explícitos para o PostgreSQL
sql_types = {
    **{c: satypes.Integer() for c in COL_INT},
    **{c: satypes.Float()   for c in COL_FLOAT},
}
if 'ano_arquivo' in df_final.columns:
    sql_types['ano_arquivo'] = satypes.Integer()

# Envia tudo para UMA única tabela
df_final.to_sql(
    'despesas',  # nome único
    con=engine,
    if_exists='replace',  #'append' se quiser rodar incrementalmente depois
    index=False,
    dtype=sql_types
)

print(f"Pronto! {len(df_final)} linhas inseridas na tabela 'despesas'.")
