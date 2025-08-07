from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = f"postgresql+psycopg2://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}"
engine = create_engine(DATABASE_URL)

with engine.begin() as conn:
    # Ensure the connection is established
    RESULT = conn.execute(text("SELECT NOW();"))  # Simple query to check connection
    for row in RESULT:
        print(f"Connection successful: {row[0]}")
    print("Database connection established successfully.")

