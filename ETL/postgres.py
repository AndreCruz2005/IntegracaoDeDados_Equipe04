from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

# Formato: postgresql+psycopg2://user:password@host:port/dbname
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)

# Conectar e executar query no banco de dados
with engine.connect() as connection:
    result = connection.execute(text("SELECT NOW();")) 
    for row in result:
        print("Current time:", row[0])
