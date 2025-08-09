from sqlalchemy import text

def create_view_yoy_por_orgao(conn):
    conn.execute(text("""
    CREATE OR REPLACE VIEW vw_yoy_por_orgao AS
    WITH orgao_ano AS (
      SELECT orgao_nome, ano_movimentacao, SUM(valor_pago) AS total_pago
      FROM despesas_recife
      GROUP BY orgao_nome, ano_movimentacao
    )
    SELECT 
      orgao_nome, 
      ano_movimentacao, 
      total_pago,
      ROUND(100.0 * (total_pago - LAG(total_pago) OVER (PARTITION BY orgao_nome ORDER BY ano_movimentacao))
            / NULLIF(LAG(total_pago) OVER (PARTITION BY orgao_nome ORDER BY ano_movimentacao),0), 2) AS yoy_pct
    FROM orgao_ano
    ORDER BY orgao_nome, ano_movimentacao;
    """))
