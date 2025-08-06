from postgres.engine import engine
from views import *

def criar_views():
    with engine.begin() as conn:
        create_view_valor_gasto_ano(conn)
        create_view_maior_valorpago_ano(conn)
        create_view_menor_valorpago_ano(conn)

criar_views()