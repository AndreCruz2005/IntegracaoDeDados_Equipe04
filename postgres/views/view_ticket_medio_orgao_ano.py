from sqlalchemy import text

def create_view_ticket_medio_orgao_ano(conn):
    conn.execute(text("""
    CREATE OR REPLACE VIEW vw_ticket_medio_orgao_ano AS
    SELECT 
      ano_movimentacao,
      orgao_nome,
      COUNT(*) AS qtd_lancamentos,
      ROUND(AVG(valor_pago),2) AS ticket_medio
    FROM despesas_recife
    GROUP BY ano_movimentacao, orgao_nome
    ORDER BY ano_movimentacao, ticket_medio DESC;
    """))
