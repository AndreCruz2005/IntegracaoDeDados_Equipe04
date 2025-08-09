from engine import engine 
from views import *
from sqlalchemy import text

# Teste de conexão e checagem da tabela
with engine.begin() as conn:
    info = conn.execute(text("""
        SELECT current_database() db,
               current_user usr,
               current_schema() sch,
               (SELECT to_regclass('public.despesas_recife')) existe
    """)).mappings().one()

    print(f"Banco: {info['db']}")
    print(f"Usuário: {info['usr']}")
    print(f"Schema: {info['sch']}")
    print(f"Tabela encontrada? {info['existe']}")

def criar_views():
    with engine.begin() as conn:
        create_view_total_pago_yoy(conn)
        create_view_yoy_por_orgao(conn)
        create_view_share_programa_ano(conn)
        create_view_hhi_credores_ano(conn)
        create_view_gap_empenho_pagamento(conn)
        create_view_ticket_medio_orgao_ano(conn)
        create_view_total_mes_rolling(conn)
        create_view_top10_credores_ano(conn)
        
        create_view_valor_gasto_ano(conn)
        create_view_maior_valorpago_ano(conn)
        create_view_menor_valorpago_ano(conn)
        create_view_valor_empenhado_gasto(conn)
        create_view_valor_gasto_medio_mes(conn)
        create_view_credores_mais_receberam(conn)
        create_view_ranking_programas(conn)
        create_view_programa_prefeito(conn)

if __name__ == "__main__":
    criar_views()