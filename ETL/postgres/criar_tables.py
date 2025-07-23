from sqlalchemy import text
from postgres import engine
from dotenv import load_dotenv
import os

load_dotenv()

# Conectar ao banco de dados e deletar todas as tabelas previamente criadas
# Depois, criar todas as tabelas necessárias
with engine.connect() as connection:
    connection.execute(text(f"""DO $$
    DECLARE
        r RECORD;
    BEGIN
        FOR r IN
            SELECT schemaname, tablename
            FROM pg_tables
            WHERE tableowner = '{os.getenv('DATABASE_USER')}'
        LOOP
            EXECUTE format('DROP TABLE IF EXISTS %I.%I CASCADE', r.schemaname, r.tablename);
        END LOOP;
    END $$;
    """))
    
    connection.execute(text(f"""
    CREATE TABLE Orgao (
        orgao_codigo VARCHAR PRIMARY KEY,
        orgao_nome VARCHAR
    );
    """))

    connection.execute(text(f"""
    CREATE TABLE Unidade (
        unidade_codigo VARCHAR PRIMARY KEY,
        unidade_nome VARCHAR,
        orgao_codigo VARCHAR REFERENCES Orgao(orgao_codigo)
    );
    """))

    connection.execute(text(f"""
    CREATE TABLE CategoriaEconomica (
        categoria_economica_codigo VARCHAR PRIMARY KEY,
        categoria_economica_nome VARCHAR
    );
    """))

    connection.execute(text(f"""
    CREATE TABLE GrupoDespesa (
        grupo_despesa_codigo VARCHAR PRIMARY KEY,
        grupo_despesa_nome VARCHAR
    );
    """))

    connection.execute(text(f"""
    CREATE TABLE ModalidadeAplicacao (
        modalidade_aplicacao_codigo VARCHAR PRIMARY KEY,
        modalidade_aplicacao_nome VARCHAR
    );
    """))

    connection.execute(text(f"""
    CREATE TABLE Elemento (
        elemento_codigo VARCHAR PRIMARY KEY,
        elemento_nome VARCHAR
    );
    """))

    connection.execute(text(f"""
    CREATE TABLE Subelemento (
        subelemento_codigo VARCHAR PRIMARY KEY,
        subelemento_nome VARCHAR,
        elemento_codigo VARCHAR REFERENCES Elemento(elemento_codigo)
    );
    """))

    connection.execute(text(f"""
    CREATE TABLE Funcao (
        funcao_codigo VARCHAR PRIMARY KEY,
        funcao_nome VARCHAR
    );
    """))

    connection.execute(text(f"""
    CREATE TABLE Subfuncao (
        subfuncao_codigo VARCHAR PRIMARY KEY,
        subfuncao_nome VARCHAR,
        funcao_codigo VARCHAR REFERENCES Funcao(funcao_codigo)
    );
    """))

    connection.execute(text(f"""
    CREATE TABLE Programa (
        programa_codigo VARCHAR PRIMARY KEY,
        programa_nome VARCHAR
    );
    """))

    connection.execute(text(f"""
    CREATE TABLE Acao (
        acao_codigo VARCHAR PRIMARY KEY,
        acao_nome VARCHAR,
        programa_codigo VARCHAR REFERENCES Programa(programa_codigo)
    );
    """))

    connection.execute(text(f"""
    CREATE TABLE FonteRecurso (
        fonte_recurso_codigo VARCHAR PRIMARY KEY,
        fonte_recurso_nome VARCHAR
    );
    """))

    connection.execute(text(f"""
    CREATE TABLE ModalidadeEmpenho (
        empenho_modalidade_codigo VARCHAR PRIMARY KEY,
        empenho_modalidade_nome VARCHAR
    );
    """))

    connection.execute(text(f"""
    CREATE TABLE ModalidadeLicitacao (
        modalidade_licitacao_codigo VARCHAR PRIMARY KEY,
        modalidade_licitacao_nome VARCHAR
    );
    """))

    connection.execute(text(f"""
    CREATE TABLE Credor (
        credor_codigo VARCHAR PRIMARY KEY,
        credor_nome VARCHAR
    );
    """))

    connection.execute(text(f"""
    CREATE TABLE Empenho (
        empenho_ano INTEGER,
        empenho_numero VARCHAR,
        subempenho VARCHAR,
        indicador_subempenho VARCHAR,
        valor_empenhado NUMERIC,
        valor_liquidado NUMERIC,
        valor_pago NUMERIC,
        ano_movimentacao INTEGER,
        mes_movimentacao INTEGER,
        
        empenho_modalidade_codigo VARCHAR,
        unidade_codigo VARCHAR,
        categoria_economica_codigo VARCHAR,
        grupo_despesa_codigo VARCHAR,
        modalidade_aplicacao_codigo VARCHAR,
        subelemento_codigo VARCHAR,
        subfuncao_codigo VARCHAR,
        acao_codigo VARCHAR,
        fonte_recurso_codigo VARCHAR,
        credor_codigo VARCHAR,
        modalidade_licitacao_codigo VARCHAR,

        PRIMARY KEY (empenho_ano, empenho_modalidade_codigo, empenho_numero, subempenho),
        
        FOREIGN KEY (empenho_modalidade_codigo) REFERENCES ModalidadeEmpenho(empenho_modalidade_codigo),
        FOREIGN KEY (unidade_codigo) REFERENCES Unidade(unidade_codigo),
        FOREIGN KEY (categoria_economica_codigo) REFERENCES CategoriaEconomica(categoria_economica_codigo),
        FOREIGN KEY (grupo_despesa_codigo) REFERENCES GrupoDespesa(grupo_despesa_codigo),
        FOREIGN KEY (modalidade_aplicacao_codigo) REFERENCES ModalidadeAplicacao(modalidade_aplicacao_codigo),
        FOREIGN KEY (subelemento_codigo) REFERENCES Subelemento(subelemento_codigo),
        FOREIGN KEY (subfuncao_codigo) REFERENCES Subfuncao(subfuncao_codigo),
        FOREIGN KEY (acao_codigo) REFERENCES Acao(acao_codigo),
        FOREIGN KEY (fonte_recurso_codigo) REFERENCES FonteRecurso(fonte_recurso_codigo),
        FOREIGN KEY (credor_codigo) REFERENCES Credor(credor_codigo),
        FOREIGN KEY (modalidade_licitacao_codigo) REFERENCES ModalidadeLicitacao(modalidade_licitacao_codigo)
    );
    """))
    connection.commit()
