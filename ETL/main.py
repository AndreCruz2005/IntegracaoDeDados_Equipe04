# main.py
import os
import sys

# Garante que os scripts no mesmo diretório sejam encontrados
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("Iniciando pipeline ETL...\n")

# Executa a extração
try:
    print("Extraindo dados...")
    import Extracao  # Isso executa o código de extração
    print("Extração concluída.\n")
except Exception as e:
    print(f"Erro na extração: {e}")
    sys.exit(1)

# Executa a transformação
try:
    print("Transformando dados...")
    import Transformacao  # Isso executa o código de transformação
    print("Transformação concluída.\n")
except Exception as e:
    print(f"Erro na transformação: {e}")
    sys.exit(1)

# Executa a carga
try:
    print("Carregando dados no PostgreSQL...")
    import Carga  # Isso executa o código de carga
    print("Carga concluída.\n")
except Exception as e:
    print(f" Erro na carga: {e}")
    sys.exit(1)

print("Pipeline ETL finalizado com sucesso!")
