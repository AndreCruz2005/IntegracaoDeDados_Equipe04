from sqlalchemy import text

def create_view_valor_gasto_medio_mes(conn):
    conn.execute(text(
        """
    CREATE OR REPLACE VIEW vw_valor_gasto_medio_mes AS
    SELECT 
        mes_movimentacao,
        ROUND(AVG(valor_total_mes), 2) AS media_valor_pago
    FROM (
        SELECT 
            ano_movimentacao,
            mes_movimentacao,
            SUM(valor_pago) AS valor_total_mes
        FROM despesas_recife
        GROUP BY ano_movimentacao, mes_movimentacao
    ) AS gastos_mensais
    GROUP BY mes_movimentacao
    ORDER BY mes_movimentacao;
        """))