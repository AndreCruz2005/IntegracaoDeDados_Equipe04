import pandas as pd
import matplotlib.pyplot as plt
from postgres.postgres import engine
from sqlalchemy import text

def padronizar_colunas(table: pd.DataFrame):
    colunas_int = ('empenho_ano', 'ano_movimentacao', 'mes_movimentacao')
    colunas_float = ('valor_empenhado', 'valor_liquidado', 'valor_pago')
    
    for coluna in table:
        
        if coluna in colunas_int:
            table[coluna] =  pd.to_numeric(table[coluna], errors='coerce').fillna(0).astype(int)
        
        elif coluna in colunas_float:
            try:
                table[coluna] =  pd.to_numeric(table[coluna], errors='coerce').fillna(0).astype(float)
            except Exception as e:
                table[coluna] =  table[coluna].str.replace(',', '.')
                table[coluna] =  pd.to_numeric(table[coluna], errors='coerce').fillna(0).astype(float)
        else:
            table[coluna] =  table[coluna].astype(str)

def store_1_table(table: pd.DataFrame):
    padronizar_colunas(table)
    
    for idx, row in table.iterrows():
        ano_movimentacao = row['ano_movimentacao']
        mes_movimentacao = row['mes_movimentacao']
        orgao_codigo = row['orgao_codigo']
        orgao_nome = row['orgao_nome']
        unidade_codigo = row['unidade_codigo']
        unidade_nome = row['unidade_nome']
        categoria_economica_codigo = row['categoria_economica_codigo']
        categoria_economica_nome = row['categoria_economica_nome']
        grupo_despesa_codigo = row['grupo_despesa_codigo']
        grupo_despesa_nome = row['grupo_despesa_nome']
        modalidade_aplicacao_codigo = row['modalidade_aplicacao_codigo']
        modalidade_aplicacao_nome = row['modalidade_aplicacao_nome']
        elemento_codigo = row['elemento_codigo']
        elemento_nome = row['elemento_nome']
        subelemento_codigo = row['subelemento_codigo']
        subelemento_nome = row['subelemento_nome']
        funcao_codigo = row['funcao_codigo']
        funcao_nome = row['funcao_nome']
        subfuncao_codigo = row['subfuncao_codigo']
        subfuncao_nome = row['subfuncao_nome']
        programa_codigo = row['programa_codigo']
        programa_nome = row['programa_nome']
        acao_codigo = row['acao_codigo']
        acao_nome = row['acao_nome']
        fonte_recurso_codigo = row['fonte_recurso_codigo']
        fonte_recurso_nome = row['fonte_recurso_nome']
        empenho_ano = row['empenho_ano']
        empenho_modalidade_nome = row['empenho_modalidade_nome']
        empenho_modalidade_codigo = row['empenho_modalidade_codigo']
        empenho_numero = row['empenho_numero']
        subempenho = row['subempenho']
        indicador_subempenho = row['indicador_subempenho']
        credor_codigo = row['credor_codigo']
        credor_nome = row['credor_nome']
        modalidade_licitacao_codigo = row['modalidade_licitacao_codigo']
        modalidade_licitacao_nome = row['modalidade_licitacao_nome']
        valor_empenhado = row['valor_empenhado']
        valor_liquidado = row['valor_liquidado']
        valor_pago = row['valor_pago']
        
        with engine.connect() as connection:
            connection.execute(text(f"""
                INSERT INTO Orgao (orgao_codigo, orgao_nome) VALUES ('{orgao_codigo}', '{orgao_nome}') ON CONFLICT DO NOTHING;
                INSERT INTO Unidade (unidade_codigo, unidade_nome, orgao_codigo) VALUES ('{unidade_codigo}', '{unidade_nome}', '{orgao_codigo}') ON CONFLICT DO NOTHING;
                INSERT INTO CategoriaEconomica (categoria_economica_codigo, categoria_economica_nome) VALUES ('{categoria_economica_codigo}', '{categoria_economica_nome}') ON CONFLICT DO NOTHING;
                INSERT INTO GrupoDespesa (grupo_despesa_codigo, grupo_despesa_nome) VALUES ('{grupo_despesa_codigo}', '{grupo_despesa_nome}') ON CONFLICT DO NOTHING;
                INSERT INTO ModalidadeAplicacao (modalidade_aplicacao_codigo, modalidade_aplicacao_nome) VALUES ('{modalidade_aplicacao_codigo}', '{modalidade_aplicacao_nome}') ON CONFLICT DO NOTHING;
                INSERT INTO Elemento (elemento_codigo, elemento_nome) VALUES ('{elemento_codigo}', '{elemento_nome}') ON CONFLICT DO NOTHING;
                INSERT INTO Subelemento (subelemento_codigo, subelemento_nome, elemento_codigo) VALUES ('{subelemento_codigo}', '{subelemento_nome}', '{elemento_codigo}') ON CONFLICT DO NOTHING;
                INSERT INTO Funcao (funcao_codigo, funcao_nome) VALUES ('{funcao_codigo}', '{funcao_nome}') ON CONFLICT DO NOTHING;
                INSERT INTO Subfuncao (subfuncao_codigo, subfuncao_nome, funcao_codigo) VALUES ('{subfuncao_codigo}', '{subfuncao_nome}', '{funcao_codigo}') ON CONFLICT DO NOTHING;
                INSERT INTO Programa (programa_codigo, programa_nome) VALUES ('{programa_codigo}', '{programa_nome}') ON CONFLICT DO NOTHING;
                INSERT INTO Acao (acao_codigo, acao_nome, programa_codigo) VALUES ('{acao_codigo}', '{acao_nome}', '{programa_codigo}') ON CONFLICT DO NOTHING;
                INSERT INTO FonteRecurso (fonte_recurso_codigo, fonte_recurso_nome) VALUES ('{fonte_recurso_codigo}', '{fonte_recurso_nome}') ON CONFLICT DO NOTHING;
                INSERT INTO ModalidadeEmpenho (empenho_modalidade_codigo, empenho_modalidade_nome) VALUES ('{empenho_modalidade_codigo}', '{empenho_modalidade_nome}') ON CONFLICT DO NOTHING;
                INSERT INTO ModalidadeLicitacao (modalidade_licitacao_codigo, modalidade_licitacao_nome) VALUES ('{modalidade_licitacao_codigo}', '{modalidade_licitacao_nome}') ON CONFLICT DO NOTHING;
                INSERT INTO Credor (credor_codigo, credor_nome) VALUES ('{credor_codigo}', '{credor_nome}') ON CONFLICT DO NOTHING; 
                INSERT INTO Empenho (
                    empenho_ano, empenho_numero, subempenho, indicador_subempenho,
                    valor_empenhado, valor_liquidado, valor_pago,
                    ano_movimentacao, mes_movimentacao,
                    empenho_modalidade_codigo, unidade_codigo, categoria_economica_codigo,
                    grupo_despesa_codigo, modalidade_aplicacao_codigo, subelemento_codigo,
                    subfuncao_codigo, acao_codigo, fonte_recurso_codigo, credor_codigo, modalidade_licitacao_codigo
                ) VALUES (
                    {empenho_ano}, '{empenho_numero}', '{subempenho}', '{indicador_subempenho}',
                    {valor_empenhado}, {valor_liquidado}, {valor_pago},
                    {ano_movimentacao}, {mes_movimentacao},
                    '{row['empenho_modalidade_codigo']}', '{row['unidade_codigo']}', '{row['categoria_economica_codigo']}',
                    '{row['grupo_despesa_codigo']}', '{row['modalidade_aplicacao_codigo']}', '{row['subelemento_codigo']}',
                    '{row['subfuncao_codigo']}', '{row['acao_codigo']}', '{row['fonte_recurso_codigo']}', '{row['credor_codigo']}', '{row['modalidade_licitacao_codigo']}'
                ) ON CONFLICT DO NOTHING;
            """))
            connection.commit()
            
def main():
    test_table = pd.read_csv('data/recife-dados-despesas-2020.csv', sep=';')
    store_1_table(test_table)
    
    
if __name__ == "__main__":
    main()