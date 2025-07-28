import pandas as pd
from Extracao import df_total  


# Definindo os nomes das colunas
df_total.columns = [
    'empenho_ano',
    'ano_movimentacao',
    'mes_movimentacao',
    'orgao_codigo',
    'orgao_nome',
    'unidade_codigo',
    'unidade_nome',
    'categoria_economica_codigo',      # era 'categoria_economica'
    'categoria_economica_nome',        # era 'categoria_nome'
    'grupo_despesa_codigo',            # era 'grupo_despesa'
    'grupo_despesa_nome',              # era 'grupo_nome'
    'modalidade_aplicacao_codigo',     # era 'modalidade_aplicacao'
    'modalidade_aplicacao_nome',       # era 'modalidade_nome'
    'elemento_codigo',                 # era 'elemento_despesa'
    'elemento_nome',
    'subelemento_codigo',              # coluna ausente
    'subelemento_nome',                # coluna ausente
    'funcao_codigo',
    'funcao_nome',
    'subfuncao_codigo',
    'subfuncao_nome',
    'programa_codigo',
    'programa_nome',
    'acao_codigo',
    'acao_nome',
    'fonte_recurso_codigo',            # era 'fonte_recurso'
    'fonte_recurso_nome',              # era 'fonte_nome'
    'empenho_modalidade_nome',         # coluna ausente
    'empenho_modalidade_codigo',       # coluna ausente
    'empenho_numero',                  # coluna ausente
    'subempenho',                      # coluna ausente
    'indicador_subempenho',            # coluna ausente
    'credor_codigo',                   # coluna ausente
    'credor_nome',                     # coluna ausente
    'modalidade_licitacao_codigo',     # coluna ausente
    'modalidade_licitacao_nome',       # coluna ausente
    'valor_empenhado',
    'valor_liquidado',
    'valor_pago'
]


# Especifica os tipos de colunas
colunas_int = ['empenho_ano', 'ano_movimentacao', 'mes_movimentacao']
colunas_float = ['valor_empenhado', 'valor_liquidado', 'valor_pago']

# Converte as colunas para inteiro
for coluna in colunas_int:
    df_total[coluna] = pd.to_numeric(df_total[coluna], errors='coerce').astype('Int64')

# Converte as colunas para float
for coluna in colunas_float:
    df_total[coluna] = pd.to_numeric(df_total[coluna], errors='coerce').astype(float)

# Converte o restante para string
for coluna in df_total.columns:
    if coluna not in colunas_int + colunas_float:
        df_total[coluna] = df_total[coluna].astype(str)

# Agora o dataframe transformado é um arquivo CSV
df_total.to_csv('df_transformado.csv', index=False)
