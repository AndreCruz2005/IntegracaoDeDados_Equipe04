from sqlalchemy import text


def create_view_programa_prefeito(conn):
    conn.execute(text("""
    CREATE OR REPLACE VIEW vw_programa_mais_pago_por_prefeito AS
    WITH programas_por_gestor AS (
        SELECT
            CASE
                WHEN ano_movimentacao BETWEEN 2002 AND 2008 THEN 'João Paulo Lima'
                WHEN ano_movimentacao BETWEEN 2009 AND 2012 THEN 'João da Costa'
                WHEN ano_movimentacao BETWEEN 2013 AND 2020 THEN 'Geraldo Júlio'
                ELSE 'Outro/Desconhecido'
            END AS gestor,
            programa_nome,
            SUM(valor_pago) AS total_valor_pago
        FROM despesas_recife
        WHERE ano_movimentacao BETWEEN 2002 AND 2020
        GROUP BY gestor, programa_nome
    ),
    ranking AS (
        SELECT
            gestor,
            programa_nome,
            total_valor_pago,
            ROW_NUMBER() OVER (PARTITION BY gestor ORDER BY total_valor_pago DESC) AS posicao
        FROM programas_por_gestor
    )
    SELECT
        gestor,
        programa_nome,
        total_valor_pago
    FROM ranking
    WHERE posicao <= 5;
    """))