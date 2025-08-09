from sqlalchemy import text

def create_view_gap_empenho_pagamento(conn):
    conn.execute(text("""
    CREATE OR REPLACE VIEW vw_gap_empenho_pagamento AS
    SELECT 
      ano_movimentacao,
      orgao_nome,
      SUM(valor_empenhado) AS total_empenhado,
      SUM(valor_pago)      AS total_pago,
      (SUM(valor_empenhado) - SUM(valor_pago)) AS gap_valor,
      ROUND(100.0*(SUM(valor_empenhado)-SUM(valor_pago))/NULLIF(SUM(valor_empenhado),0),2) AS gap_pct
    FROM despesas_recife
    GROUP BY ano_movimentacao, orgao_nome
    ORDER BY ano_movimentacao, gap_valor DESC;
    """))
