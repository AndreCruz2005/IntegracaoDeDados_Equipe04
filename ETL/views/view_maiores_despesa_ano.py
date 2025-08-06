from sqlalchemy import text

def create_view_maior_valorpago_ano(conn):
    conn.execute(text("""
        CREATE OR REPLACE VIEW vw_maior_valorpago_ano AS
        SELECT
            ano_movimentacao,
            orgao_nome,
            total_valor_pago
        FROM (
            SELECT
                ano_movimentacao,
                orgao_nome,
                SUM(valor_pago) AS total_valor_pago,
                ROW_NUMBER() OVER (
                    PARTITION BY ano_movimentacao
                    ORDER BY SUM(valor_pago) DESC
                ) AS rn
            FROM
                despesas_recife
            GROUP BY
                ano_movimentacao, orgao_nome
        ) AS sub
        WHERE rn = 1;
    """))