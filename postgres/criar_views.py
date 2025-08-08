from engine import engine 
from views import *

def criar_views():
    with engine.begin() as conn:
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