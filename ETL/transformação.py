import pandas as pd

# Carrega dataframe unificado
df = pd.read_csv("despesas_recife.csv", encoding='utf-8')


# Teste se existia alguma valor faltando em alguma coluna da tabela --- resultado 0 valores faltando nas colunas
# assim não foi preciso tratar valores faltantes
# print(df.isnull().sum())


COL_INT = ('empenho_ano', 'ano_movimentacao', 'mes_movimentacao', 'orgao_codigo',
            'grupo_despesa_codigo','modalidade_aplicacao_codigo','elemento_codigo',
            'subelemento_codigo','funcao_codigo','subfuncao_codigo','programa_codigo',
            'acao_codigo','fonte_recurso_codigo','empenho_numero','subempenho', 'credor_codigo',
            'modalidade_licitacao_codigo')

# Opta-se por numeric ao invés de float para evitar problemas com arredondamento e conseguir mais precisão
COL_NUMERIC = ('valor_empenhado', 'valor_liquidado', 'valor_pago')

# Padronização das colunas
df.columns = (
    df.columns
    .str.strip()         # Remove espaços vazios no começo e fim 
    .str.lower()         # Deixa tudo minúsculo
    .str.replace(" ", "_")  # Substitui espaços por underline
)

for coluna in COL_INT:
    df[coluna] = df[coluna].astype(int)

# Erro na transformação, a partir de 2016 'valor_empenhado', 'valor_liquidado', 'valor_pago' começaram a vir 
# com , e não com . como nos anos anteriores
for coluna in COL_NUMERIC:
    # Para os anos a partir de 2016, troca vírgula por ponto antes de converter
    mask_2016 = df['ano_movimentacao'] >= 2016
    df.loc[mask_2016, coluna] = (
        df.loc[mask_2016, coluna]
        .astype(str)
        .str.replace('.', '', regex=False)   # Remove separador de milhar, se existir
        .str.replace(',', '.', regex=False)
    )

    # Aqui converte para numeric e errors='coerce' faz valores inválidos virarem NAN por precaução
    df[coluna] = pd.to_numeric(df[coluna],errors='coerce')


# Pega o conjunto de todas as colunas
todas_colunas = set(df.columns)

# Subtrai as colunas numéricas e inteiras
colunas_string = todas_colunas - set(COL_INT) - set(COL_NUMERIC)

# Converte as colunas restantes para string
for coluna in colunas_string:
    df[coluna] = df[coluna].astype(str)


# Salvando tratamento em um novo arquivo csv
df.to_csv("despesas_recife_tratadas.csv", index=False, encoding='utf-8')

