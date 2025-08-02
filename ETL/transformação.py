import pandas as pd

#criação do meu dataframe
df = pd.read_csv(r"C:\Users\joaov\OneDrive\Documentos\cin\repositorio\ProjetoIntegracao\IntegracaoDeDados_Equipe04\despesas_recife.csv")


#teste se esxistia alguma valor faltando em alguma coluna da tabela --- resultado 0 valores faltando nas colunas
# assim não foi preciso tratar valores faltantes
print(df.isnull().sum())


COL_INT = ('empenho_ano', 'ano_movimentacao', 'mes_movimentacao', 'orgao_codigo',
            'grupo_despesa_codigo','modalidade_aplicacao_codigo','elemento_codigo',
            'subelemento_codigo','funcao_codigo','subfuncao_codigo','programa_codigo',
            'acao_codigo','fonte_recurso_codigo','empenho_numero','subempenho', 'credor_codigo',
            'modalidade_licitacao_codigo')

#optei por numeric no lugar de float para evitar problemas com arredondamento e conseguir mais precisão
COL_NUMERIC = ('valor_empenhado', 'valor_liquidado', 'valor_pago')


#padronização das minhas colunas
df.columns = (
    df.columns
    .str.strip()         # Remove espaços 
    .str.lower()         # Deixa tudo minúsculo
    .str.replace(" ", "_")  # Substitui espaços por underline
)

for coluna in COL_INT:
    df[coluna] = df[coluna].astype(int)

for coluna in COL_NUMERIC:
    # aqui passo para numeric e errors='coerce' faz valores inválidos como abcde virarem NAN só para verificar
    df[coluna] = pd.to_numeric(df[coluna],errors='coerce')



#salvando meu tratamento em um novo arquivo csv
df.to_csv("despesas_recife_tratadas.csv",index = False)