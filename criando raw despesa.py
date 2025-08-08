import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
senha = os.getenv("SENHA")

#estabeleci a conecção com o host
engine = create_engine(
    f"postgresql+psycopg2://postgres:{senha}@localhost/despesas_orc",
    connect_args={"options": "-c search_path=raw,analytics"}
    )

df = pd.read_csv(f"./recife-dados-despesas-2003.csv", sep=';', encoding="utf-8")
colunas = df.columns
sql_campos = ",\n".join([f'"{col}" TEXT' for col in colunas])
sql_create = f"""
CREATE TABLE IF NOT EXISTS raw.raw_despesas (
    {sql_campos}
)
"""

with engine.begin() as conn:
    conn.execute(text(sql_create))


#lendo um csv
for x in range(2003,2021):
    df = pd.read_csv(f"./recife-dados-despesas-{x}.csv", sep=';', encoding="utf-8")
    df.to_sql("raw_despesas", engine, if_exists="append", index=False, schema="raw")
# ja ta tudo no postgres agora vamo ver
