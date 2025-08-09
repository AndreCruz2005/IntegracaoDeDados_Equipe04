from sqlalchemy import text

def create_view_hhi_credores_ano(conn):
    conn.execute(text("""
    CREATE OR REPLACE VIEW vw_hhi_credores_ano AS
    WITH cred AS (
      SELECT ano_movimentacao, credor_nome, SUM(valor_pago) AS total_credor
      FROM despesas_recife
      GROUP BY ano_movimentacao, credor_nome
    ),
    tot AS (
      SELECT ano_movimentacao, SUM(total_credor) AS total_ano 
      FROM cred 
      GROUP BY ano_movimentacao
    ),
    share AS (
      SELECT c.ano_movimentacao, c.credor_nome,
             1.0 * c.total_credor / NULLIF(t.total_ano,0) AS share
      FROM cred c 
      JOIN tot t USING(ano_movimentacao)
    )
    SELECT ano_movimentacao,
           ROUND(SUM(POWER(share,2))::numeric, 4) AS hhi
    FROM share
    GROUP BY ano_movimentacao
    ORDER BY ano_movimentacao;
    """))
