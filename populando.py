import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine


load_dotenv()
senha = os.getenv("SENHA")

#estabeleci a conecção com o host
engine = create_engine(
    f"postgresql+psycopg2://postgres:{senha}@localhost/despesas_orc",
    connect_args={"options": "-c search_path=raw,analytics"}
    )

colunas_total = ['ano_movimentacao', 'mes_movimentacao', 'orgao_codigo', 'orgao_nome', 'unidade_codigo', 'unidade_nome',
           'categoria_economica_codigo', 'categoria_economica_nome', 'grupo_despesa_codigo', 'grupo_despesa_nome',
            'modalidade_aplicacao_codigo', 'modalidade_aplicacao_nome', 'elemento_codigo', 'elemento_nome',
            'subelemento_codigo', 'subelemento_nome', 'funcao_codigo', 'funcao_nome', 'subfuncao_codigo', 'subfuncao_nome',
            'programa_codigo', 'programa_nome', 'acao_codigo', 'acao_nome', 'fonte_recurso_codigo', 'fonte_recurso_nome',
            'empenho_ano', 'empenho_modalidade_nome', 'empenho_modalidade_codigo', 'empenho_numero', 'subempenho',
            'indicador_subempenho', 'credor_codigo', 'credor_nome', 'modalidade_licitacao_codigo', 'modalidade_licitacao_nome',
            'valor_empenhado', 'valor_liquidado', 'valor_pago'
]
colunas_int = ['ano_movimentacao','mes_movimentacao', 'orgao_codigo', 'categoria_economica_codigo','grupo_despesa_codigo','modalidade_aplicacao_codigo',
               'elemento_codigo','subelemento_codigo','funcao_codigo','subfuncao_codigo','programa_codigo','acao_codigo','fonte_recurso_codigo',
               'empenho_ano','empenho_modalidade_codigo','empenho_numero','subempenho','credor_codigo','modalidade_licitacao_codigo'
]
colunas_decimal = [
   'unidade_codigo', 'valor_empenhado', 'valor_liquidado', 'valor_pago'
]

##preparação da tipagem das colunas
with engine.connect() as conexao:
    df = pd.read_sql("SELECT * FROM raw.raw_despesas",conexao)
    print(list(df.columns))
    for coluna in colunas_int: ##o tipo padrão dessas conversões é float64
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce").astype("Int64")
    for coluna in colunas_decimal:
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce").round(2)

##populando o esquema analitico
df_empenho = df[
    ['empenho_ano', 'empenho_modalidade_nome', 'empenho_modalidade_codigo', 'empenho_numero', 'subempenho',
    'indicador_subempenho', 'credor_codigo', 'credor_nome', 'modalidade_licitacao_codigo', 'modalidade_licitacao_nome',
    'valor_empenhado', 'valor_liquidado', 'valor_pago']
].drop_duplicates()
df_empenho.to_sql("empenho", engine, if_exists="append", index=False, schema="analytics")

df_acao = df[['acao_codigo','acao_nome', 'programa_codigo']].drop_duplicates()
df_acao.to_sql("acao", engine,if_exists='append',schema='analytics',index=False)

df_programa = df[['programa_codigo', 'programa_nome']].drop_duplicates()
df_programa.to_sql("programa", engine, if_exists='append', schema='analytics', index=False)

df_categoria_economica = df[['df_categoria_economica_codigo','df_categoria_economica_nome']].drop_duplicates()
df_categoria_economica.to_sql('categoria_economica', engine, if_exists="append", index=False, schema="analytics")

df_credor = df[['credor_codigo', 'credor_nome']].drop_duplicates()
df_credor.to_sql("credor", engine, if_exists="append", index=False, schema="analytics")

df_elemento = df[['elemento_codigo', 'elemento_nome']].drop_duplicates()
df_elemento.to_sql("elemento", engine, if_exists="append", index=False, schema="analytics")

df_subelemento = df[['subelemento_codigo', 'subelemento_nome', 'elemento_codigo']].drop_duplicates()
df_subelemento.to_sql("subelemento", engine, if_exists="append", index=False, schema="analytics")

df_fonte_recurso = df[['fonte_recurso_codigo', 'fonte_recurso_nome']].drop_duplicates()
df_fonte_recurso.to_sql("fonte_recurso", engine, if_exists="append", index=False, schema="analytics")

df_funcao = df[['funcao_codigo', 'funcao_nome']].drop_duplicates()
df_funcao.to_sql("funcao", engine, if_exists="append", index=False, schema="analytics")

df_subfuncao = df[['subfuncao_codigo', 'subfuncao_nome', 'funcao_codigo']].drop_duplicates()
df_subfuncao.to_sql("subfuncao", engine, if_exists="append", index=False, schema="analytics")

df_grupo_despesa = df[['grupo_despesa_codigo', 'grupo_despesa_nome']].drop_duplicates()
df_grupo_despesa.to_sql("grupo_despesa", engine, if_exists="append", index=False, schema="analytics")

df_modalidade_aplicacao = df[['modalidade_aplicacao_codigo', 'modalidade_aplicacao_nome']].drop_duplicates()
df_modalidade_aplicacao.to_sql("modalidade_aplicacao", engine, if_exists="append", index=False, schema="analytics")

df_unidade = df[['unidade_codigo', 'unidade_nome', 'orgao_codigo']].drop_duplicates()
df_unidade.to_sql("unidade", engine, if_exists="append", index=False, schema="analytics")

df_orgao = df[['orgao_codigo', 'orgao_nome']].drop_duplicates()
df_orgao.to_sql("orgao", engine, if_exists="append", index=False, schema="analytics")

df_modalidade_empenho = df[['empenho_modalidade_codigo', 'empenho_modalidade_nome']].drop_duplicates()
df_modalidade_empenho.to_sql("modalidade_empenho", engine, if_exists="append", index=False, schema="analytics")

df_modalidade_licitacao = df[['modalidade_licitacao_codigo', 'modalidade_licitacao_nome']].drop_duplicates()
df_modalidade_licitacao.to_sql("modalidade_licitacao", engine, if_exists="append", index=False, schema="analytics")


#.to_sql('', engine, if_exists="append", index=False, schema="analytics")

#pra ser int
# 1.  ano_movimentacao 2. mes_movimentacao 3. orgao_codigo 4. categoria_economica_codigo 5. grupo_despesa_codigo 6. modalidade_aplicacao_codigo 7. elemento_codigo 8. subelemento_codigo 9. funcao_codigo 10. subfuncao_codigo 11. programa_codigo 12. acao_codigo 13. fonte_recurso_codigo 14. empenho_ano 15. emepnho_modalidade_codigo 16. empenho_numero 17. subempenho 18. credor_codigo 19. modalidade_licitacao_codigo
#para ser decimal de 2 ,
# unidade codigo, valor_empenhado, valor_liquidado, valor_pago
#para continuar como text
# o resto