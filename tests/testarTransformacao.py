import pandas as pd
from sqlalchemy import text

import os
import sys
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_folder)
from postgres.engine import engine

print("=== TESTE DA TRANSFORMAÇÃO ELT ===")
print("Verificando se os dados foram transformados corretamente\n")

# Teste 1: Verificar se as tabelas existem
print("1. Verificando existência das tabelas...")
with engine.connect() as connection:
    # Verifica tabela raw_despesas_pre_2016
    result_raw_pre = connection.execute(text("""
        SELECT COUNT(*) as total FROM information_schema.tables 
        WHERE table_name = 'raw_despesas_pre_2016'
    """))
    raw_exists_pre = result_raw_pre.fetchone()[0] > 0

    # Verifica tabela raw_despesas_pos_2016
    result_raw_pos = connection.execute(text("""
        SELECT COUNT(*) as total FROM information_schema.tables 
        WHERE table_name = 'raw_despesas_pos_2016'
    """))
    raw_exists_pos = result_raw_pos.fetchone()[0] > 0
    
    # Verifica tabela despesas_recife
    result_trans = connection.execute(text("""
        SELECT COUNT(*) as total FROM information_schema.tables 
        WHERE table_name = 'despesas_recife'
    """))
    trans_exists = result_trans.fetchone()[0] > 0
    
    print(f"  ✓ Tabela raw_despesas_pre_2016: {'EXISTE' if raw_exists_pre else 'NÃO EXISTE'}")
    print(f"  ✓ Tabela raw_despesas_pos_2016: {'EXISTE' if raw_exists_pos else 'NÃO EXISTE'}")
    print(f"  ✓ Tabela despesas_recife: {'EXISTE' if trans_exists else 'NÃO EXISTE'}")

if not (raw_exists_pre and raw_exists_pos and trans_exists):
    print("\n❌ ERRO: Execute primeiro os pipelines em ELT e ETL")
    exit()

# Teste 2: Comparar contagem de registros
print("\n2. Comparando contagem de registros...")
with engine.connect() as connection:
    raw_count = (
        connection.execute(text("SELECT COUNT(*) FROM raw_despesas_pre_2016")).fetchone()[0]
        + connection.execute(text("SELECT COUNT(*) FROM raw_despesas_pos_2016")).fetchone()[0]
        + pd.read_csv('despesas_recife_tratadas.csv').shape[0])
    trans_count = connection.execute(text("SELECT COUNT(*) FROM despesas_recife")).fetchone()[0]
    
    print(f"  Registros pré transformação: {raw_count:,}")
    print(f"  Registros em despesas_recife: {trans_count:,}")
    print(f"  Status: {'✓ IGUAL' if raw_count == trans_count else '⚠ DIFERENTE'}")

# Teste 3: Verificar tipos de dados
print("\n3. Verificando tipos de dados das colunas transformadas...")
df_sample = pd.read_sql("SELECT * FROM despesas_recife LIMIT 5", con=engine)

# Colunas que devem ser inteiras
colunas_int = ['ano_movimentacao', 'mes_movimentacao', 'orgao_codigo', 'valor_empenhado']
for col in colunas_int:
    if col in df_sample.columns:
        tipo = str(df_sample[col].dtype)
        print(f"  {col}: {tipo} {'✓' if tipo.lower() in 'float64int64' else '⚠'}")

# Teste 4: Verificar tratamento de vírgula/ponto (anos >= 2016)
print("\n4. Testando tratamento de valores monetários...")
with engine.connect() as connection:
    # Busca dados de 2016 para verificar se vírgulas foram tratadas
    result = connection.execute(text("""
        SELECT ano_movimentacao, valor_empenhado, valor_liquidado, valor_pago 
        FROM despesas_recife 
        WHERE ano_movimentacao >= 2016 
        LIMIT 3
    """))
    
    print("  Amostra de valores >= 2016 (devem ser numéricos):")
    for row in result:
        print(f"    Ano: {row[0]}      Empenhado: {row[1]}, Liquidado: {row[2]}, Pago: {row[3]}")

# Teste 5: Verificar padronização de nomes de colunas
print("\n5. Verificando padronização de nomes das colunas...")
colunas = pd.read_sql("SELECT * FROM despesas_recife LIMIT 100", con=engine).columns.tolist()

problemas_nomes = []
for col in colunas:
    if col != col.lower():
        problemas_nomes.append(f"Não é minúscula: {col}")
    if ' ' in col:
        problemas_nomes.append(f"Contém espaço: {col}")

if problemas_nomes:
    print("  ⚠ PROBLEMAS encontrados:")
    for problema in problemas_nomes:
        print(f"    {problema}")
else:
    print("  ✓ Todos os nomes das colunas estão padronizados (minúsculas, sem espaços)")

# Teste 6: Verificar dados faltantes
print("\n6. Verificando dados faltantes...")
df_check = pd.read_sql("SELECT * FROM despesas_recife LIMIT 10000", con=engine)
missing_data = df_check.isnull().sum()
total_missing = missing_data.sum()

if total_missing > 0:
    print(f"  ⚠ Encontrados {total_missing} valores faltantes:")
    for col, count in missing_data[missing_data > 0].items():
        print(f"    {col}: {count}")
else:
    print("  ✓ Nenhum valor faltante encontrado na amostra")

# Teste 7: Estatísticas básicas
print("\n7. Estatísticas básicas dos dados transformados...")
with engine.connect() as connection:
    stats = connection.execute(text("""
        SELECT 
            MIN(ano_movimentacao) as ano_min,
            MAX(ano_movimentacao) as ano_max,
            COUNT(DISTINCT orgao_codigo) as total_orgaos,
            SUM(valor_empenhado) as total_empenhado,
            COUNT(*) as total_registros
        FROM despesas_recife
    """)).fetchone()
    
    print(f"  Período: {stats[0]} a {stats[1]}")
    print(f"  Total de órgãos: {stats[2]}")
    print(f"  Total empenhado: R$ {stats[3]:,.2f}")
    print(f"  Total de registros: {stats[4]:,}")

print("\n=== TESTE CONCLUÍDO ===")
print("Se todos os itens estão com ✓, a transformação foi bem-sucedida!")
