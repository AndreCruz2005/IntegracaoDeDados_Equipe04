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

# testei a conexao
# with engine.connect() as conexao:
#     resultado = conexao.execute(text("SELECT 1"))
#     print(f"Conectado! Resultado: {resultado.scalar()}")
#lendo um csv
# for x in range(2003,2009):
#     df = pd.read_csv(f"./recife-dados-despesas-{x}.csv", sep=';', encoding="utf-8")
#     # talvez fazer uns ajustes aqui
#     df.to_sql("raw_despesas", engine, if_exists="append", index=False, schema="raw")
#ja ta tudo no postgres agora vamo ver
