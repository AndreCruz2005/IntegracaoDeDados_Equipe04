import sys
import os

parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_folder)

from postgres.engine import engine
import matplotlib.pyplot as plt
from sqlalchemy import text

def plot_grafico_valor_gasto_ano():
    with engine.begin() as conn: 
        res = conn.execute(text(""" SELECT * FROM vw_valor_gasto_ano """))

    anos = []
    valores = []

    for row in res:
        anos.append(row[0])
        valores.append(row[1])

    plt.figure(figsize=(15, 8))
    plt.plot(anos, valores, marker='o', linewidth=3, markersize=7, color='blue')
    plt.xlabel('Ano')
    plt.ylabel('Valor Total Pago (Bilhões de R$)')
    plt.title('Valor Total Pago por Ano')
    plt.xticks(anos, rotation=45)    
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('grafico_valor_gasto_ano.png')


plot_grafico_valor_gasto_ano()
