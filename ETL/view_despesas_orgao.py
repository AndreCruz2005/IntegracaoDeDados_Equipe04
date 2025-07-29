from sqlalchemy import text
from Engine import engine  

sql = """
CREATE OR REPLACE VIEW despesas_por_orgao_ano_fmt AS
WITH total_por_ano AS (
    SELECT 
        ano_movimentacao,
        SUM(valor_pago) AS total_ano
    FROM despesas
    GROUP BY ano_movimentacao
)
SELECT
    d.ano_movimentacao,
    d.orgao_nome,
    COUNT(*) AS qtd_registros,
    SUM(d.valor_pago) AS total_pago,
    'R$ ' || TO_CHAR(SUM(d.valor_pago), 'FM999G999G999G999D00') AS total_pago_formatado,
    ROUND(
        (SUM(d.valor_pago) * 100.0 / t.total_ano),
        4
    ) AS pct_no_ano,
    REPLACE(TO_CHAR(ROUND(
        (SUM(d.valor_pago) * 100.0 / t.total_ano),
        2
    ), 'FM990D00'), '.', ',') || '%' AS pct_no_ano_formatado
FROM 
    despesas d
JOIN 
    total_por_ano t ON d.ano_movimentacao = t.ano_movimentacao
GROUP BY 
    d.ano_movimentacao, d.orgao_nome, t.total_ano
ORDER BY 
    d.ano_movimentacao, SUM(d.valor_pago) DESC;
"""

with engine.connect() as conn:
    conn.execute(text("DROP VIEW IF EXISTS despesas_por_orgao_ano_fmt;"))
    conn.execute(text(sql))
    conn.commit()