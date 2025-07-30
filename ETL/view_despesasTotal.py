from sqlalchemy import text
from Engine import engine
import pandas as pd

criar_view_sql = """
CREATE OR REPLACE VIEW despesas_por_orgao_ano_total_fmt AS
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
    ROUND((SUM(d.valor_pago) * 100.0 / t.total_ano), 2) AS pct_no_ano_raw
FROM 
    despesas d
JOIN 
    total_por_ano t ON d.ano_movimentacao = t.ano_movimentacao
GROUP BY 
    d.ano_movimentacao, d.orgao_nome, t.total_ano
ORDER BY 
    total_pago DESC;
"""

try:
    with engine.connect() as conn:
        conn.execute(text("DROP VIEW IF EXISTS despesas_por_orgao_ano_total_fmt CASCADE;"))
        conn.execute(text(criar_view_sql))
        conn.commit()
    print("View criada com sucesso.")
except Exception as e:
    print("Erro ao criar a view:")
    print(e)