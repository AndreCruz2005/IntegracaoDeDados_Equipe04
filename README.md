# IntegracaoDeDados_Equipe04

Respositório para projeto de Integração de Dados - Banco de Dados CIn/UFPE 2025.1

# IntegracaoDeDados_Equipe04

Repositório para projeto de Integração de Dados - Banco de Dados CIn/UFPE 2025.1

## Pré-requisitos

-   Python 3.10 ou superior
-   PostgreSQL rodando localmente (ou ajuste a variável de ambiente `DATABASE_URL`)
-   Instalar dependências do projeto

## Instalação

1. Clone o repositório:

    ```sh
    git clone https://github.com/seu-usuario/IntegracaoDeDados_Equipe04.git
    cd IntegracaoDeDados_Equipe04
    ```

2. Crie e configure o arquivo `.env` (veja `.env.example` para referência):

    ```
    DATABASE_USER="user"
    DATABASE_PASSWORD="pass"
    DATABASE_HOST="localhost"
    DATABASE_PORT="5432"
    DATABASE_NAME="postgres"
    ```

3. Instale as dependências:
    ```sh
    pip install -r requirements.txt
    ```

## Execução

Para rodar a análise e gerar gráficos:

```sh
python main.py
```

Para testar a conexão com o banco de dados PostgreSQL:

```sh
python postgres.py
```

## Estrutura

-   `ETL/main.py`: Código principal de análise e geração de gráficos.
-   `ETL/postgres.py`: Teste de conexão com o banco de dados.
-   `data/`: Arquivos CSV de despesas por ano.
-   `test_output.csv`: Saída de exemplo da análise.

## Observações

-   Certifique-se de que o banco de dados está acessível conforme configurado em `.env`.
-   Os gráficos serão exibidos na tela ao executar o `main.py`.
