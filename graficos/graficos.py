import sys
import os

parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_folder)

from postgres.engine import engine
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from sqlalchemy import text
import pandas as pd

# garante que a pasta de saída existe
os.makedirs('graficos', exist_ok=True)

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
        
    # bar graph
    plt.figure(figsize=(15, 8))
    plt.bar(meses, valores, color='orange')
    plt.xlabel('Mês')
    plt.ylabel('Valor Médio Pago (Milhões de R$)')
    plt.title('Valor Médio Pago por Mês (2003-2020)')
    plt.xticks(meses, rotation=45)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('graficos/grafico_media_mensal_historica.png')


# YOY do total pago (vw_total_pago_yoy)
def plot_yoy_total():
    with engine.begin() as conn:
        df = pd.read_sql(text("""
            SELECT ano_movimentacao, total_pago, crescimento_yoy_pct
            FROM vw_total_pago_yoy
            ORDER BY ano_movimentacao
        """), conn)

    plt.figure(figsize=(15, 8))
    plt.bar(df["ano_movimentacao"], df["crescimento_yoy_pct"])
    plt.title("Crescimento Year-over-Year do Total Pago (%)")
    plt.xlabel("Ano"); plt.ylabel("Variação % vs ano anterior")
    plt.axhline(0, linewidth=1)
    plt.tight_layout()
    plt.savefig('graficos/01_yoy_total_pago_pct.png')

# Top 10 credores — último ano (vw_top10_credores_ano)
def plot_top10_credores_ultimo_ano():
    with engine.begin() as conn:
        ano_max = pd.read_sql(text("""
            SELECT MAX(ano_movimentacao) AS a FROM vw_top10_credores_ano
        """), conn)["a"].iloc[0]
        df = pd.read_sql(text("""
            SELECT credor_nome, total_credor, pos
            FROM vw_top10_credores_ano
            WHERE ano_movimentacao = (SELECT MAX(ano_movimentacao) FROM vw_top10_credores_ano)
            ORDER BY pos
        """), conn)
    df["total_credor_mm"] = df["total_credor"] / 1_000_000

    plt.figure(figsize=(15, 8))
    plt.barh(df["credor_nome"], df["total_credor_mm"])
    plt.title(f"Top 10 Credores — {int(ano_max)}")
    plt.xlabel("Total Pago (Milhões de R$)")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig('graficos/02_top10_credores_ultimo_ano.png')

# Participação dos programas (vw_share_programa_ano) — top 5
def plot_share_programas_area():
    with engine.begin() as conn:
        df = pd.read_sql(text("""
            SELECT ano_movimentacao, programa_nome, share_pct
            FROM vw_share_programa_ano
        """), conn)

    top_programas = (df.groupby("programa_nome")["share_pct"]
                       .mean().sort_values(ascending=False).head(5).index)
    df_top = df[df["programa_nome"].isin(top_programas)].copy()
    pvt = df_top.pivot(index="ano_movimentacao",
                       columns="programa_nome",
                       values="share_pct").fillna(0).sort_index()

    plt.figure(figsize=(15, 8))
    plt.stackplot(pvt.index, pvt.T.values, labels=pvt.columns)
    plt.title("Participação dos Principais Programas (%)")
    plt.xlabel("Ano"); plt.ylabel("% do Total Pago")
    plt.legend(loc="upper left", ncols=2)
    plt.tight_layout()
    plt.savefig('graficos/03_share_programas_area.png')

# Gap empenho x pagamento (vw_gap_empenho_pagamento) — % não pago
def plot_gap_empenho_pagamento():
    with engine.begin() as conn:
        df = pd.read_sql(text("""
            SELECT ano_movimentacao,
                   SUM(total_empenhado) AS emp,
                   SUM(total_pago)      AS pago
            FROM vw_gap_empenho_pagamento
            GROUP BY ano_movimentacao
            ORDER BY ano_movimentacao
        """), conn)
    df["gap_pct"] = 100.0 * (df["emp"] - df["pago"]) / df["emp"].where(df["emp"] != 0)

    plt.figure(figsize=(15, 8))
    plt.plot(df["ano_movimentacao"], df["gap_pct"], marker='o')
    plt.title("Gap Empenhado x Pago — % do Empenhado não Pago")
    plt.xlabel("Ano"); plt.ylabel("Gap (%)")
    plt.axhline(0, linewidth=1)
    plt.tight_layout()
    plt.savefig('graficos/04_gap_empenho_pagamento_pct.png')

# Ticket médio por órgão — top 10 (último ano) (vw_ticket_medio_orgao_ano)
def plot_ticket_medio_orgao_ultimo_ano():
    with engine.begin() as conn:
        ano_max = pd.read_sql(text("""
            SELECT MAX(ano_movimentacao) AS a FROM vw_ticket_medio_orgao_ano
        """), conn)["a"].iloc[0]
        df = pd.read_sql(text(f"""
            SELECT orgao_nome, ticket_medio, qtd_lancamentos
            FROM vw_ticket_medio_orgao_ano
            WHERE ano_movimentacao = {int(ano_max)}
            ORDER BY ticket_medio DESC
            LIMIT 10
        """), conn)

    plt.figure(figsize=(15, 8))
    plt.barh(df["orgao_nome"], df["ticket_medio"])
    plt.title(f"Ticket Médio por Órgão — Top 10 ({int(ano_max)})")
    plt.xlabel("Ticket Médio (R$ por lançamento)")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig('graficos/05_ticket_medio_top10_ultimo_ano.png')

# Concentração de credores — HHI (vw_hhi_credores_ano)
def plot_hhi_credores():
    with engine.begin() as conn:
        df = pd.read_sql(text("""
            SELECT ano_movimentacao, hhi
            FROM vw_hhi_credores_ano
            ORDER BY ano_movimentacao
        """), conn)

    plt.figure(figsize=(15, 8))
    plt.plot(df["ano_movimentacao"], df["hhi"], marker='o')
    plt.title("Concentração de Pagamentos entre Credores (HHI)")
    plt.xlabel("Ano"); plt.ylabel("HHI (0 a 1)")
    plt.tight_layout()
    plt.savefig('graficos/06_hhi_credores_ano.png')

# Top 10 credores — período inteiro (tabela base)
def plot_top10_credores_geral():
    with engine.begin() as conn:
        df = pd.read_sql(text("""
            SELECT credor_nome, SUM(valor_pago) AS total
            FROM public.despesas_recife
            GROUP BY credor_nome
            ORDER BY total DESC
            LIMIT 10
        """), conn)
    df["total_mm"] = df["total"] / 1_000_000

    plt.figure(figsize=(15, 8))
    plt.barh(df["credor_nome"], df["total_mm"])
    plt.title("Top 10 Credores — Período 2003–2020")
    plt.xlabel("Total Pago no Período (Milhões de R$)")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig('graficos/07_top10_credores_geral.png')


plot_grafico_valor_gasto_ano()
plot_grafico_media_mensal_historica()
plot_yoy_total()
plot_top10_credores_ultimo_ano()
plot_share_programas_area()
plot_gap_empenho_pagamento()
plot_ticket_medio_orgao_ultimo_ano()
plot_hhi_credores()
plot_top10_credores_geral()
