# IntegracaoDeDados_Equipe04

Respositório para projeto de Integração de Dados - Banco de Dados CIn/UFPE 2025.1

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

Para criar as entidades no banco de dados PostgreSQL

```sh
python ETL/postgres/criar_tabelas.py
```

Para extrair dados das tabelas CSV, transformar-los e fazer o upload destes para o banco de dados

```sh
python ETL/processar_data.py
```

## Observações

- Certifique-se de que o banco de dados está acessível conforme configurado em `.env`.
