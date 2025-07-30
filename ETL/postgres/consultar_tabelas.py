from sqlalchemy import text
from postgres import engine

def select_all_from(table, connection):
    result = connection.execute(text(f"""
    SELECT * FROM public."{table}";
    """))

    for i, row in enumerate(result):
        print(row)

def select_count_from(table, connection):
    result = connection.execute(text(f"""
    SELECT {table}_codigo, COUNT(*) AS qt FROM public."{table}"
    GROUP BY {table}_codigo
    ORDER BY qt ASC;
    """))

    for i, row in enumerate(result):
        print(row)

def select_count_from_and_group_by_name(table, connection):
    result = connection.execute(text(f"""
    SELECT {table}_nome, COUNT(*) AS qt FROM public."{table}"
    GROUP BY {table}_nome
    ORDER BY qt ASC;
    """))

    for i, row in enumerate(result):
        print(row)


def gastos_por_ano(connection):
    result = connection.execute(text(f"""
    SELECT e.empenho_ano, SUM(e.valor_pago) FROM public."Empenho" e
    GROUP BY e.empenho_ano;
    """))

    print("ANO | DESPESA")
    for i, row in enumerate(result):
        print(f"{row[0]} | R$ {row[1]:,.2f}")

def select_rows_de_credor(credor, connection):
    query = text("""
        SELECT e.* 
        FROM public."Empenho" e
        JOIN public."Credor" c ON e.credor_codigo = c.credor_codigo
        WHERE c.credor_nome = :credor_nome;
    """)
    
    result = connection.execute(query, {"credor_nome": credor})
    
    for i, row in enumerate(result):
        print(row)

def orgaos_que_mais_receberam(connection):
    result = connection.execute(text(f"""
    SELECT o.orgao_nome, SUM(e.valor_pago) AS dinheiro FROM public."Empenho" e
    JOIN public."Unidade" u ON u.unidade_codigo = e.unidade_codigo
    JOIN public."Orgao" o ON o.orgao_codigo = u.orgao_codigo
    GROUP BY o.orgao_codigo, o.orgao_nome
    ORDER BY dinheiro DESC;
    """))
    
    for i, row in enumerate(result):
        print(row[0], f'{row[1]:,.2f}')

def credores_que_mais_receberam(connection):
    result = connection.execute(text(f"""
    SELECT c.credor_nome, SUM(e.valor_pago) AS dinheiro FROM public."Empenho" e
    JOIN public."Credor" c ON c.credor_codigo = e.credor_codigo
    GROUP BY c.credor_codigo, c.credor_nome
    ORDER BY dinheiro;
    """))
    
    for i, row in enumerate(result):
        print(row[0], f'{row[1]:,.2f}')

with engine.connect() as connection:
    #orgaos_que_mais_receberam(connection)
    select_count_from_and_group_by_name('Credor', connection)
    #credores_que_mais_receberam(connection)