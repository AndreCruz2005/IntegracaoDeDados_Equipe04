from sqlalchemy import text

def create_view_total_mes_rolling(conn):
    conn.execute(text("""
    CREATE OR REPLACE VIEW vw_total_mes_rolling AS
    WITH m AS (
      SELECT 
        ano_movimentacao,
        mes_movimentacao,
        SUM(valor_pago) AS total_mes
      FROM despesas_recife
      GROUP BY ano_movimentacao, mes_movimentacao
    )
    SELECT *,
           ROUND(AVG(total_mes) OVER (
             ORDER BY ano_movimentacao, mes_movimentacao
             ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
           ), 2) AS mm3
    FROM m
    ORDER BY ano_movimentacao, mes_movimentacao;
    """))
