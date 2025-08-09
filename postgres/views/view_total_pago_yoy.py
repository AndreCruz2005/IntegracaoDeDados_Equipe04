from sqlalchemy import text

def create_view_total_pago_yoy(conn):
    conn.execute(text("""
    CREATE OR REPLACE VIEW vw_total_pago_yoy AS
    WITH base AS (
      SELECT ano_movimentacao, SUM(valor_pago) AS total_pago
      FROM despesas_recife
      GROUP BY ano_movimentacao
    )
    SELECT 
      ano_movimentacao,
      total_pago,
      LAG(total_pago) OVER (ORDER BY ano_movimentacao) AS total_anterior,
      ROUND(100.0 * (total_pago - LAG(total_pago) OVER (ORDER BY ano_movimentacao))
            / NULLIF(LAG(total_pago) OVER (ORDER BY ano_movimentacao),0), 2) AS crescimento_yoy_pct
    FROM base
    ORDER BY ano_movimentacao;
    """))
