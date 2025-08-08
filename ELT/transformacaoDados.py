import os
import sys
from sqlalchemy import text
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_folder)
from postgres.engine import engine

print("=== INICIANDO TRANSFORMAÇÃO ELT ===")
print("Transformando dados das tabelas 'raw_despesas_pre_2016' e 'raw_despesas_pos_2016'")

def clean_text(conn, table):
    # Encontra todas as colunas que são texto
        result = conn.execute(text(f"""
        SELECT column_name 
        FROM information_schema.columns
        WHERE table_name = '{table}'
        AND data_type = 'text';
        """))
        
        columns = [row.column_name for row in result]
        
        # Trim espaços brancos, deixa tudo minúsculo, substitui ' ' por '_'
        for column in columns:
            print(f"Transformação iniciada para {table}.{column}")
            conn.execute(text(f"""
                UPDATE {table}
                SET {column} = REPLACE(LOWER(TRIM({column})), ' ', '_')
                WHERE {column} IS NOT NULL;
            """))
            print(f"Transformação de {table}.{column} finalizada")
            
def valores_monetarios_para_numeric(conn):
    COL_NUMERIC = ('valor_empenhado', 'valor_liquidado', 'valor_pago')
    
    for column in COL_NUMERIC:
        print(f"Transformação iniciada para 'raw_despesas_pos_2016'.{column}")
        
        # Primeiro, limpa os dados removendo caracteres não numéricos (exceto ponto e vírgula)
        # e padroniza o separador decimal para ponto
        conn.execute(text(f"""
            UPDATE raw_despesas_pos_2016
            SET {column} = CASE
                WHEN {column} IS NULL OR TRIM(CAST({column} AS TEXT)) = '' THEN NULL
                ELSE CAST(
                    REPLACE(
                        REPLACE(
                            REGEXP_REPLACE(CAST({column} AS TEXT), '[^0-9,.\\-]', '', 'g'),
                            ',', '.'
                        ),
                        '..', '.'
                    ) AS NUMERIC(18,2)
                )
            END;
        """))
                    
        # Depois altera o tipo da coluna para NUMERIC(18,2)
        for table in ('raw_despesas_pre_2016', 'raw_despesas_pos_2016'):
            conn.execute(text(f"""
                ALTER TABLE {table}
                ALTER COLUMN {column} TYPE NUMERIC(18,2)
                USING {column}::NUMERIC(18,2);
            """))
        
            print(f"Transformação de {table}.{column} finalizada")
        
def unificar_tabelas_despesas(conn):
    # Cria a tabela unificada com base na estrutura de uma das tabelas
    print("Criando tabela unificada 'despesas_recife'...")
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS despesas_recife AS
        SELECT * FROM raw_despesas_pre_2016 WHERE 1=0;
    """))
    
    # Insere dados da primeira tabela
    print("Inserindo dados de 'raw_despesas_pre_2016'...")
    conn.execute(text("""
        INSERT INTO despesas_recife
        SELECT * FROM raw_despesas_pre_2016;
    """))
    
    # Insere dados da segunda tabela
    print("Inserindo dados de 'raw_despesas_pos_2016'...")
    conn.execute(text("""
        INSERT INTO despesas_recife
        SELECT * FROM raw_despesas_pos_2016;
    """))

def tratar_unidade_codigo(conn, table):
    conn.execute(text(f"""
            ALTER TABLE {table}
            ALTER COLUMN unidade_codigo TYPE text
            USING unidade_codigo::text;
    """))

with engine.begin() as conn:

    for table in ('raw_despesas_pre_2016', 'raw_despesas_pos_2016'):
        clean_text(conn, table)
        tratar_unidade_codigo(conn, table)
        pass
    
    valores_monetarios_para_numeric(conn)
    unificar_tabelas_despesas(conn)
    
        
print("\n=== TRANSFORMAÇÃO ELT CONCLUÍDA ===")
print("Dados transformados disponíveis na tabela 'despesas_recife'")
