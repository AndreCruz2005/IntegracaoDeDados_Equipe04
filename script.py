import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()
senha = os.getenv("SENHA")

#estabeleci a conecção com o host
engine = create_engine(f"postgresql+psycopg2://postgres:{senha}@localhost/despesas_orc")

with engine.connect() as conexao:
    resultado = conexao.execute("SELECT 1") ##aqui ta dando erro vejo mais amanha
    print(f"Conectado! Resultado: {resultado.scalar()}")
#lendo um csv
# df = pd.read_csv("./recife-dades-despesas-2003.csv")
#talvez fazer uns ajustes aqui
# df.to_sql()
