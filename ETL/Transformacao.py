import pandas as pd
from Extracao import df_total

# Função que padroniza as colunas; 
# Retira espaços em branco no início e no final da string;
# Coloca tudo minúsculo e troca o que está em branco no meio da string por "_".
def padronizarColunas(df_total):
    df_total.columns = [col.strip().lower().replace(' ', '_') for col in df_total.columns]
    return df_total

# Funções para retirar duplicatas
def transformar_orgao(df):
    return df[['orgao_codigo', 'orgao_nome']].drop_duplicates()

def transformar_unidade(df):
    return df[['unidade_codigo', 'unidade_nome', 'orgao_codigo']].drop_duplicates()

def transformar_categoria_economica(df):
    return df[['categoria_economica', 'categoria_nome']].drop_duplicates().rename(columns={
        'categoria_economica': 'categoria_economica_codigo',
        'categoria_nome': 'categoria_economica_nome'
    })

def transformar_grupo_despesa(df):
    return df[['grupo_despesa', 'grupo_nome']].drop_duplicates().rename(columns={
        'grupo_despesa': 'grupo_despesa_codigo',
        'grupo_nome': 'grupo_despesa_nome'
    })

def transformar_modalidade_aplicacao(df):
    return df[['modalidade_aplicacao_codigo', 'modalidade_aplicacao_nome']].drop_duplicates()









