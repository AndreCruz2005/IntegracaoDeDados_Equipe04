import sys
import os

parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_folder)

from postgres.engine import engine
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from sqlalchemy import text

def plot_grafico_valor_gasto_ano():
    with engine.begin() as conn: 
        res = conn.execute(text(""" SELECT * FROM vw_valor_gasto_ano """))

    anos = []
    valores = []

    for row in res:
        anos.append(row[0])
        valores.append(row[1] / 1_000_000)

    plt.figure(figsize=(15, 8))
    plt.plot(anos, valores, marker='o', linewidth=3, markersize=7, color='blue')
    plt.xlabel('Ano')
    plt.ylabel('Valor Total Pago (Milhões de R$)')
    plt.title('Valor Total Pago por Ano')
    plt.xticks(anos, rotation=45)    
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    ax = plt.gca()
    ax.yaxis.set_major_locator(MultipleLocator(500))
    
    plt.savefig('graficos/grafico_valor_gasto_ano.png')

def plot_grafico_media_mensal_historica():
    with engine.begin() as conn:
        res = conn.execute(text(""" SELECT * FROM vw_valor_gasto_medio_mes """))
        
    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    valores = []
    
    for row in res:
        valores.append(row[1]  / 1_000_000)  
        
    #bar graph
    plt.figure(figsize=(15, 8))
    plt.bar(meses, valores, color='orange')
    plt.xlabel('Mês')
    plt.ylabel('Valor Médio Pago (Milhões de R$)')
    plt.title('Valor Médio Pago por Mês (2003-2020)')
    plt.xticks(meses, rotation=45)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('graficos/grafico_media_mensal_historica.png')

plot_grafico_valor_gasto_ano()
plot_grafico_media_mensal_historica()