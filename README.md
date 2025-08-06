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

### ETL
1. Extrair dados dos arquivos CSV de data/ e armazena-los, não tratados, em despesas_recife.csv

```sh
python ETL/extração.py
```

2. Transformar os dados de despesas_recife.csv e armazenar em despesas_recife_tratadas.csv

```sh
python ETL/transformação.py
```

3. Carregar os dados tratados no banco de dados PostgreSQL:

```sh
python ETL/carregamento.py
```

### ELT
1. Carregar dados brutos diretamente no PostgreSQL:

```sh
python ELT/cargaRaw2008-2012.py
```

2. Transformar dados no banco de dados:

```sh
python ELT/transformacaoDados.py
```

3. Validar transformações:

```sh
python ELT/testar_transformacao.py
```

## Observações

-   Certifique-se de que o banco de dados está acessível conforme configurado em `.env`.
