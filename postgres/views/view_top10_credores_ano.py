from sqlalchemy import text

def create_view_top10_credores_ano(conn):
    conn.execute(text("""
    CREATE OR REPLACE VIEW vw_top10_credores_ano AS
    WITH c AS (
      SELECT ano_movimentacao, credor_nome, SUM(valor_pago) AS total_credor
      FROM despesas_recife
      GROUP BY ano_movimentacao, credor_nome
    ),
    r AS (
      SELECT ano_movimentacao, SUM(total_credor) AS total_ano 
      FROM c 
      GROUP BY ano_movimentacao
    ),
    ranked AS (
      SELECT c.*,
             ROW_NUMBER() OVER (PARTITION BY c.ano_movimentacao ORDER BY c.total_credor DESC) AS pos,
             ROUND(100.0*c.total_credor/NULLIF(r.total_ano,0),2) AS share_pct
      FROM c JOIN r USING (ano_movimentacao)
    )
    SELECT * 
    FROM ranked 
    WHERE pos <= 10 
    ORDER BY ano_movimentacao, pos;
    """))
