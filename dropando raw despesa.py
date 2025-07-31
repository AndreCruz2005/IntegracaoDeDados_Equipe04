import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
senha = os.getenv("SENHA")

#estabeleci a conecção com o host
engine = create_engine(
    f"postgresql+psycopg2://postgres:{senha}@localhost/despesas_orc",
    connect_args={"options": "-csearch_path=raw,analytics"}
    )

with engine.begin() as conexao:
    conexao.execute(text("DROP TABLE IF EXISTS raw.raw_despesas"))
