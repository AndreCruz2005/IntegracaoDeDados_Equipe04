from sqlalchemy import text
from postgres import engine

with engine.connect() as connection:
    result = connection.execute(text(f"""
    SELECT e.empenho_ano, SUM(e.valor_pago) FROM public."Empenho" e
    GROUP BY e.empenho_ano;
    """))

    print("ANO | DESPESA")
    for i, row in enumerate(result):
        print(f"{row[0]} | R$ {row[1]:.2f}")