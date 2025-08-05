from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import urllib.parse


load_dotenv()

user = os.getenv("DB_USER")
password = urllib.parse.quote_plus(os.getenv("DB_PASSWORD"))  
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
dbname = os.getenv("DB_NAME")

engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{dbname}")

