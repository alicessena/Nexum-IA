import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, URL
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from typing import Generator

load_dotenv()

DIALECT = 'mssql+pyodbc'
DRIVER = 'ODBC Driver 17 for SQL Server' 
SERVER = os.getenv('AZURE_SQL_SERVER')
DATABASE = os.getenv('AZURE_SQL_DATABASE')
USERNAME = os.getenv('AZURE_SQL_USERNAME')
PASSWORD = os.getenv('AZURE_SQL_PASSWORD')

db_url = URL.create(
    DIALECT,
    username=USERNAME,
    password=PASSWORD,
    host=SERVER,
    database=DATABASE,
    query={
        'odbc_connect': f"DRIVER={{{DRIVER}}};TrustServerCertificate=no;Encrypt=yes;"
    }
)

engine = create_engine(
    db_url,
    echo=False,
    pool_recycle=3600
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

class Base(DeclarativeBase):
    pass

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def check_db_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            if result.scalar_one():
                print("Conexão com o banco de dados bem-sucedida.")
            else:
                raise Exception("Falha na execução do teste básico.")
    except Exception as e:
        print(f"Erro na conexão: {e}")
        raise

if __name__ == "__main__":
    check_db_connection()