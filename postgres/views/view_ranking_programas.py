from sqlalchemy import text

def create_view_ranking_programas(conn):
    conn.execute(text("""
    CREATE OR REPLACE VIEW vw_ranking_programas_acoes AS
    SELECT
        programa_nome,
        acao_nome,
        SUM(valor_pago) AS total_valor_pago
    FROM despesas_recife
    GROUP BY
        programa_nome,
        acao_nome
    ORDER BY
        total_valor_pago DESC;
    """))
