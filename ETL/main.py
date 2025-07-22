import pandas as pd
import matplotlib.pyplot as plt

def padronizar_valores_numericos(table: pd.DataFrame):
    colunas_numericas = ('valor_empenhado', 'valor_liquidado', 'valor_pago')
    for coluna in colunas_numericas:
        try:
            table[coluna] =  table[coluna].astype(float)
        except Exception as e:
            table[coluna] =  table[coluna].str.replace(',', '.')
            table[coluna] =  table[coluna].astype(float)
        
def test(ano, categoria):
    table = pd.read_csv(f'data/recife-dados-despesas-{ano}.csv', sep=';')

    # Transformar dados
    padronizar_valores_numericos(table)
    
    # Exemplo de análise, recepientes de mais fundos agrupados por categoria
    agrupado = table.groupby([f'{categoria}_nome'])[['valor_empenhado', 'valor_liquidado', 'valor_pago']].sum().sort_values(by='valor_pago', ascending=False)
    agrupado.to_csv('test_output.csv')
    return round(agrupado['valor_pago'].sum(), 2)

def grafico():
    anos = []
    valores = []
    for i in range(2003, 2024):
        if i == 2022: continue
        print(i)
        anos.append(i)
        valores.append(test(i, 'orgao'))
            
    # Plot
    plt.figure(figsize=(12, 6))
    plt.plot(anos, valores, marker='o', linestyle='-', color='royalblue')

    # Labels e título
    plt.title('Gastos da Prefeitura do Recife por Ano (2003–2023)', fontsize=14)
    plt.xlabel('Ano', fontsize=12)
    plt.ylabel('Gasto Total (Bilhões de R$)', fontsize=12)
    plt.grid(True)
    plt.xticks(anos, rotation=45)
    plt.tight_layout()

    plt.show()

def main():
    # tables = {y:pd.read_csv(f'data/recife-dados-despesas-{y}.csv', sep=';') for y in range(2003, 2024)}

    grafico()
    
    t = test(2023, 'orgao')
    
if __name__ == "__main__":
    main()