from sqlalchemy import text

def create_view_valor_empenhado_gasto(conn):
    conn.execute(text(
        """
        CREATE OR REPLACE VIEW vw_valor_empenhado_gasto AS
        SELECT 
            ano_movimentacao, 
            orgao_nome, 
            sum(valor_empenhado) AS total_valor_empenhado, 
            sum(valor_pago) AS total_valor_pago,
            (sum(valor_pago) / NULLIF(sum(valor_empenhado), 0)) * 100 AS percentual_gasto
        FROM despesas_recife
        GROUP BY
            ano_movimentacao, orgao_nome
        ORDER BY
            ano_movimentacao, total_valor_empenhado DESC
        ;
        """))