from postgres.engine import engine  
from sqlalchemy.types import Integer, Numeric, String
import pandas as pd

# Carrega o CSV JÁ TRATADO
df = pd.read_csv("despesas_recife_tratadas.csv", encoding='utf-8')

# Apenas mapeia tipos do Pandas para o PostgreSQL evitando que ele interprete sozinho e converta os valores que eu já havia transformado
tipos_colunas_sqlalchemy = {
    # Colunas inteiras 
    'ano_movimentacao': Integer(),
    'mes_movimentacao': Integer(),
    'orgao_codigo': Integer(),
    'grupo_despesa_codigo': Integer(),
    'modalidade_aplicacao_codigo': Integer(),
    'elemento_codigo': Integer(),
    'subelemento_codigo': Integer(),
    'funcao_codigo': Integer(),
    'subfuncao_codigo': Integer(),
    'programa_codigo': Integer(),
    'acao_codigo': Integer(),
    'fonte_recurso_codigo': Integer(),
    'empenho_ano': Integer(),
    'empenho_numero': Integer(),
    'subempenho': Integer(),
    'credor_codigo': Integer(),
    'modalidade_licitacao_codigo': Integer(),
    
    # Colunas numéricas 
    'valor_empenhado': Numeric(18, 2),
    'valor_liquidado': Numeric(18, 2),
    'valor_pago': Numeric(18, 2),
    
    #  colunas que são strings 
    'orgao_nome': String(255),
    'unidade_codigo': String(50),  # Códigos não numéricos são strings
    'unidade_nome': String(255),
    'categoria_economica_codigo': String(50),
    'categoria_economica_nome': String(255),
    'grupo_despesa_nome': String(255),
    'modalidade_aplicacao_nome': String(255),
    'elemento_nome': String(255),
    'subelemento_nome': String(255),
    'funcao_nome': String(255),
    'subfuncao_nome': String(255),
    'programa_nome': String(255),
    'acao_nome': String(255),
    'fonte_recurso_nome': String(255),
    'empenho_modalidade_nome': String(255),
    'empenho_modalidade_codigo': String(50),
    'indicador_subempenho': String(50),
    'credor_nome': String(255),
    'modalidade_licitacao_nome': String(255)
}

# Envia ao banco (os dados já estão tratados)
print("Carregamento de dados iniciado")
df.to_sql(
    name="despesas_recife",
    con=engine,
    if_exists="replace",
    index=False,
    dtype=tipos_colunas_sqlalchemy
)

print("Carregamento de dados finalizado")