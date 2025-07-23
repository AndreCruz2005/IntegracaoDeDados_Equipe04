import pandas as pd
import matplotlib.pyplot as plt
from postgres.postgres import engine
from sqlalchemy import text
import requests
from io import StringIO


def padronizar_colunas(table: pd.DataFrame):
    colunas_int = ('empenho_ano', 'ano_movimentacao', 'mes_movimentacao')
    colunas_float = ('valor_empenhado', 'valor_liquidado', 'valor_pago')
    
    for coluna in table:
        
        if coluna in colunas_int:
            table[coluna] =  table[coluna].astype(int)
        
        elif coluna in colunas_float:
            try:
                table[coluna] =  table[coluna].astype(float)
            except Exception as e:
                table[coluna] =  table[coluna].str.replace(',', '.').astype(float)
        else:
            table[coluna] =  table[coluna].astype(str)

def insert_unique(table: pd.DataFrame, engine, table_name: str, columns: list):
    unique = table[columns].drop_duplicates()
    unique.to_sql(table_name, engine, if_exists='append', index=False, method='multi')

def insert_empenho(table: pd.DataFrame, engine):
    empenho_cols = [
        "empenho_ano", "empenho_numero", "subempenho", "indicador_subempenho",
        "valor_empenhado", "valor_liquidado", "valor_pago",
        "ano_movimentacao", "mes_movimentacao",
        "empenho_modalidade_codigo", "unidade_codigo", "categoria_economica_codigo",
        "grupo_despesa_codigo", "modalidade_aplicacao_codigo", "subelemento_codigo",
        "subfuncao_codigo", "acao_codigo", "fonte_recurso_codigo", "credor_codigo", "modalidade_licitacao_codigo"
    ]
    table[empenho_cols].to_sql(
        "Empenho", engine, if_exists='append', index=False, method='multi', chunksize=1000
    )

def store_1_table(table: pd.DataFrame):
    from postgres.postgres import engine  # assumes your engine is defined here

    padronizar_colunas(table)

    insert_unique(table, engine, "Orgao", ["orgao_codigo", "orgao_nome"])
    insert_unique(table, engine, "Unidade", ["unidade_codigo", "unidade_nome", "orgao_codigo"])
    insert_unique(table, engine, "CategoriaEconomica", ["categoria_economica_codigo", "categoria_economica_nome"])
    insert_unique(table, engine, "GrupoDespesa", ["grupo_despesa_codigo", "grupo_despesa_nome"])
    insert_unique(table, engine, "ModalidadeAplicacao", ["modalidade_aplicacao_codigo", "modalidade_aplicacao_nome"])
    insert_unique(table, engine, "Elemento", ["elemento_codigo", "elemento_nome"])
    insert_unique(table, engine, "Subelemento", ["subelemento_codigo", "subelemento_nome", "elemento_codigo"])
    insert_unique(table, engine, "Funcao", ["funcao_codigo", "funcao_nome"])
    insert_unique(table, engine, "Subfuncao", ["subfuncao_codigo", "subfuncao_nome", "funcao_codigo"])
    insert_unique(table, engine, "Programa", ["programa_codigo", "programa_nome"])
    insert_unique(table, engine, "Acao", ["acao_codigo", "acao_nome", "programa_codigo"])
    insert_unique(table, engine, "FonteRecurso", ["fonte_recurso_codigo", "fonte_recurso_nome"])
    insert_unique(table, engine, "ModalidadeEmpenho", ["empenho_modalidade_codigo", "empenho_modalidade_nome"])
    insert_unique(table, engine, "ModalidadeLicitacao", ["modalidade_licitacao_codigo", "modalidade_licitacao_nome"])
    insert_unique(table, engine, "Credor", ["credor_codigo", "credor_nome"])

    insert_empenho(table, engine)

            
def main():
    res = requests.get('https://media.githubusercontent.com/media/AndreCruz2005/IntegracaoDeDados_Equipe04/refs/heads/andre_dev/data/recife-dados-despesas-2023.csv')
    csv_data = StringIO(res.content.decode('utf-8'))
    test_table = pd.read_csv(csv_data, sep=';')
    store_1_table(test_table)
    
    
if __name__ == "__main__":
    main()
