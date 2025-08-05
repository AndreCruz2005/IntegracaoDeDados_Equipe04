from postgres.engine import engine
from sqlalchemy import text

with engine.begin() as conn:  
    conn.execute(text("""
        CREATE OR REPLACE VIEW vw_valor_gasto_ano AS
        SELECT
            ano_movimentacao,
            total_valor_pago
        FROM (
            SELECT
                ano_movimentacao,
                SUM(valor_pago) AS total_valor_pago,
                ROW_NUMBER() OVER (
                    PARTITION BY ano_movimentacao
                ) AS rn
            FROM
                despesas_recife
            GROUP BY
                ano_movimentacao
        ) AS sub
        WHERE rn = 1;
    """))