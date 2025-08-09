from sqlalchemy import text

def create_view_share_programa_ano(conn):
    conn.execute(text("""
    CREATE OR REPLACE VIEW vw_share_programa_ano AS
    WITH prog AS (
      SELECT ano_movimentacao, programa_nome, SUM(valor_pago) AS total_programa
      FROM despesas_recife
      GROUP BY ano_movimentacao, programa_nome
    ),
    ano AS (
      SELECT ano_movimentacao, SUM(total_programa) AS total_ano 
      FROM prog 
      GROUP BY ano_movimentacao
    )
    SELECT 
      p.ano_movimentacao, 
      p.programa_nome, 
      p.total_programa,
      ROUND(100.0 * p.total_programa / NULLIF(a.total_ano,0), 2) AS share_pct
    FROM prog p
    JOIN ano a USING (ano_movimentacao)
    ORDER BY p.ano_movimentacao, share_pct DESC;
    """))
