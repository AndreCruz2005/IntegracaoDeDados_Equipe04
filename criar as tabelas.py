from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
senha = os.getenv("SENHA")

engine = create_engine(
    f"postgresql+psycopg2://postgres:{senha}@localhost/despesas_orc",
    connect_args={"options": "-c search_path=analytics"}
)

sql = """
CREATE TABLE IF NOT EXISTS orgao (
    orgao_codigo INT PRIMARY KEY,
    orgao_nome VARCHAR(64)
);

CREATE TABLE IF NOT EXISTS unidade (
    unidade_codigo INT PRIMARY KEY,
    unidade_nome VARCHAR(64),
    orgao_codigo INT REFERENCES analytics.orgao(orgao_codigo)
);

CREATE TABLE IF NOT EXISTS categoria_economica (
    categoria_economica_codigo INT PRIMARY KEY,
    categoria_economica_nome VARCHAR(64)
);

CREATE TABLE IF NOT EXISTS grupo_despesa (
    grupo_despesa_codigo INT PRIMARY KEY,
    grupo_despesa_nome VARCHAR(64)
);

CREATE TABLE IF NOT EXISTS modalidade_aplicacao (
    modalidade_aplicacao_codigo INT PRIMARY KEY,
    modalidade_aplicacao_nome VARCHAR(64)
);

CREATE TABLE IF NOT EXISTS elemento (
    elemento_codigo INT PRIMARY KEY,
    elemento_nome VARCHAR(64)
);

CREATE TABLE IF NOT EXISTS subelemento (
    subelemento_codigo INT PRIMARY KEY,
    subelemento_nome VARCHAR(64),
    elemento_codigo INT REFERENCES analytics.elemento(elemento_codigo)
);

CREATE TABLE IF NOT EXISTS funcao (
    funcao_codigo INT PRIMARY KEY,
    funcao_nome VARCHAR(64)
);

CREATE TABLE IF NOT EXISTS subfuncao (
    subfuncao_codigo INT PRIMARY KEY,
    subfuncao_nome VARCHAR(64),
    funcao_codigo INT REFERENCES analytics.funcao(funcao_codigo)
);

CREATE TABLE IF NOT EXISTS programa (
    programa_codigo INT PRIMARY KEY,
    programa_nome VARCHAR(64)
);

CREATE TABLE IF NOT EXISTS acao (
    acao_codigo INT PRIMARY KEY,
    acao_nome VARCHAR(64),
    programa_codigo INT REFERENCES analytics.programa(programa_codigo)
);

CREATE TABLE IF NOT EXISTS fonte_recurso (
    fonte_recurso_codigo INT PRIMARY KEY,
    fonte_recurso_nome VARCHAR(64)
);

CREATE TABLE IF NOT EXISTS modalidade_empenho (
    empenho_modalidade_codigo INT PRIMARY KEY,
    empenho_modalidade_nome VARCHAR(64)
);

CREATE TABLE IF NOT EXISTS modalidade_licitacao (
    modalidade_licitacao_codigo INT PRIMARY KEY,
    modalidade_licitacao_nome VARCHAR(64)
);

CREATE TABLE IF NOT EXISTS credor (
    credor_codigo INT PRIMARY KEY,
    credor_nome VARCHAR(128)
);

CREATE TABLE IF NOT EXISTS empenho (
    empenho_ano INT,
    empenho_modalidade_codigo INT,
    empenho_numero INT,
    subempenho INT,
    indicador_subempenho VARCHAR(8),
    ano_movimentacao INT,
    mes_movimentacao INT,
    unidade_codigo INT,
    categoria_economica_codigo INT,
    grupo_despesa_codigo INT,
    modalidade_aplicacao_codigo INT,
    subelemento_codigo INT,
    subfuncao_codigo INT,
    acao_codigo INT,
    fonte_recurso_codigo INT,
    credor_codigo INT,
    modalidade_licitacao_codigo INT,
    valor_empenhado DECIMAL(14,2),
    valor_liquidado DECIMAL(14,2),
    valor_pago DECIMAL(14,2),
    PRIMARY KEY (
        empenho_ano,
        empenho_modalidade_codigo,
        empenho_numero,
        subempenho
    ),
    FOREIGN KEY (empenho_modalidade_codigo) REFERENCES analytics.modalidade_empenho(empenho_modalidade_codigo),
    FOREIGN KEY (unidade_codigo) REFERENCES analytics.unidade(unidade_codigo),
    FOREIGN KEY (categoria_economica_codigo) REFERENCES analytics.categoria_economica(categoria_economica_codigo),
    FOREIGN KEY (grupo_despesa_codigo) REFERENCES analytics.grupo_despesa(grupo_despesa_codigo),
    FOREIGN KEY (modalidade_aplicacao_codigo) REFERENCES analytics.modalidade_aplicacao(modalidade_aplicacao_codigo),
    FOREIGN KEY (subelemento_codigo) REFERENCES analytics.subelemento(subelemento_codigo),
    FOREIGN KEY (subfuncao_codigo) REFERENCES analytics.subfuncao(subfuncao_codigo),
    FOREIGN KEY (acao_codigo) REFERENCES analytics.acao(acao_codigo),
    FOREIGN KEY (fonte_recurso_codigo) REFERENCES analytics.fonte_recurso(fonte_recurso_codigo),
    FOREIGN KEY (credor_codigo) REFERENCES analytics.credor(credor_codigo),
    FOREIGN KEY (modalidade_licitacao_codigo) REFERENCES analytics.modalidade_licitacao(modalidade_licitacao_codigo)
);
"""
##aparentemente n pode ser tudo de uma vez tem q separa cada comando sql

##n eh pra usar connect e pra usar begin pq ele faz commit quando sai e connect nao
with engine.begin() as conexao:
    comandos = sql.split(";")
    for comando in comandos:
        if comando.strip(): ##isso aqui evita executar com elemento vazio na lista de comandos (e tem mesmo eu testei)
            conexao.execute(text(sql))

