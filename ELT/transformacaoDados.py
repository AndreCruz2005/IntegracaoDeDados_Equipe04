import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

# Configuração da conexão com banco PostgreSQL
# Abordagem ELT: agora vamos transformar os dados que já estão no banco
engine = create_engine(f"postgresql+psycopg2://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}/{os.getenv('DATABASE_URL')}")

print("=== INICIANDO TRANSFORMAÇÃO ELT ===")
print("Transformando dados da tabela raw_despesas")

# Extract: busca os dados brutos que foram carregados anteriormente
print("Extraindo dados brutos da tabela raw_despesas...")
df = pd.read_sql("SELECT * FROM raw_despesas", con=engine)
print(f"  ✓ {len(df)} registros extraídos")

# Transform: aplicação das transformações nos dados
print("\nAplicando transformações...")

# Colunas que devem ser convertidas para inteiro
COL_INT = ('empenho_ano', 'ano_movimentacao', 'mes_movimentacao', 'orgao_codigo',
           'grupo_despesa_codigo', 'modalidade_aplicacao_codigo', 'elemento_codigo',
           'subelemento_codigo', 'funcao_codigo', 'subfuncao_codigo', 'programa_codigo',
           'acao_codigo', 'fonte_recurso_codigo', 'empenho_numero', 'subempenho', 
           'credor_codigo', 'modalidade_licitacao_codigo', 'ano')

# Colunas que devem ser convertidas para decimal/numeric 
COL_NUMERIC = ('valor_empenhado', 'valor_liquidado', 'valor_pago')

# Padronização dos nomes das colunas seguindo padrão snake_case
print("  → Padronizando nomes das colunas...")
df.columns = (
    df.columns
    .str.strip()         # Remove espaços em branco
    .str.lower()         # Converte para minúsculas 
    .str.replace(" ", "_")  # Substitui espaços por underline
)

# Conversão de tipos de dados para inteiros
print("  → Convertendo colunas numéricas inteiras...")
for coluna in COL_INT:
    if coluna in df.columns:
        df[coluna] = pd.to_numeric(df[coluna], errors='coerce').astype('Int64')

# Tratamento especial para valores monetários
# erro na transformação, a partir de 2016 os valores vêm com vírgula em vez de ponto
print("  → Tratando valores monetários (vírgula/ponto)...")
for coluna in COL_NUMERIC:
    if coluna in df.columns:
        # Para anos >= 2016, substitui vírgula por ponto antes da conversão
        mask_2016 = df['ano_movimentacao'] >= 2016
        df.loc[mask_2016, coluna] = (
            df.loc[mask_2016, coluna]
            .astype(str)
            .str.replace('.', '', regex=False)   # Remove separador de milhar, se existir
            .str.replace(',', '.', regex=False)  # Substitui vírgula por ponto
        )
        
        # aqui passo para numeric e errors='coerce' faz valores inválidos virarem NAN
        df[coluna] = pd.to_numeric(df[coluna], errors='coerce')

# Conversão das colunas restantes para string
print("  → Convertendo colunas restantes para string...")
todas_colunas = set(df.columns)
colunas_string = todas_colunas - set(COL_INT) - set(COL_NUMERIC)
for coluna in colunas_string:
    df[coluna] = df[coluna].astype(str)

# Verificação de dados faltantes
print("  → Verificando dados faltantes...")
missing_data = df.isnull().sum()
if missing_data.sum() > 0:
    print(f"    ⚠ Encontrados {missing_data.sum()} valores faltantes")
    print("    Valores faltantes por coluna:")
    for col, count in missing_data[missing_data > 0].items():
        print(f"      {col}: {count}")
else:
    print("    ✓ Nenhum valor faltante encontrado")

# Load: salva os dados transformados em nova tabela
print("\nCarregando dados transformados...")
with engine.connect() as connection:
    # Remove tabela transformada se existir
    connection.execute(text("DROP TABLE IF EXISTS despesas_transformadas"))
    connection.commit()

# Carrega dados transformados na nova tabela
df.to_sql("despesas_transformadas", con=engine, if_exists="replace", index=False)

print(f"  ✓ {len(df)} registros transformados carregados na tabela 'despesas_transformadas'")

# Estatísticas finais
print("\n=== ESTATÍSTICAS DA TRANSFORMAÇÃO ===")
print(f"Total de registros processados: {len(df):,}")
print(f"Anos processados: {sorted(df['ano_movimentacao'].unique())}")
print(f"Período: {df['ano_movimentacao'].min()} a {df['ano_movimentacao'].max()}")
print(f"Total de órgãos: {df['orgao_codigo'].nunique()}")
print(f"Valor total empenhado: R$ {df['valor_empenhado'].sum():,.2f}")

print("\n=== TRANSFORMAÇÃO ELT CONCLUÍDA ===")
print("Dados transformados disponíveis na tabela 'despesas_transformadas'")
