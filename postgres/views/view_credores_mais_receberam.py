from sqlalchemy import text

def create_view_credores_mais_receberam(conn):
    conn.execute(text(
    """
    CREATE OR REPLACE VIEW vw_credores_mais_receberam AS
    SELECT credor_nome, ROUND(SUM(valor_pago), 2) AS total_pago
    FROM despesas_recife
    GROUP BY credor_nome
    ORDER BY total_pago DESC; 
    """))