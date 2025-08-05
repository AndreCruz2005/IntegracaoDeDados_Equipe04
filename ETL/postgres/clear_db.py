from sqlalchemy import text
from engine import engine
from dotenv import load_dotenv
import os

load_dotenv()

# Conectar ao banco de dados e deletar todas as tabelas previamente criadas
with engine.begin() as connection:
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
    