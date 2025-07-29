from sqlalchemy import text
from Engine import engine

sql_criar_tabelas = """
CREATE TABLE IF NOT EXISTS orgao AS
SELECT DISTINCT orgao_codigo, orgao_nome FROM despesas;

ALTER TABLE orgao
ADD CONSTRAINT pk_orgao PRIMARY KEY (orgao_codigo);

CREATE TABLE IF NOT EXISTS unidade AS
SELECT DISTINCT unidade_codigo, unidade_nome, orgao_codigo FROM despesas;

ALTER TABLE unidade
ADD CONSTRAINT pk_unidade PRIMARY KEY (unidade_codigo);

ALTER TABLE unidade
ADD CONSTRAINT fk_unidade_orgao FOREIGN KEY (orgao_codigo)
REFERENCES orgao(orgao_codigo);
"""

with engine.connect() as conn:
    conn.execute(text(sql_criar_tabelas))
    conn.commit()

print("Tabelas  criadas com sucesso.")
