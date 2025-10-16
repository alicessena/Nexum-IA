import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from typing import Generator

load_dotenv()

# Dialeto alterado para 'mssql+pytds'
DIALECT = 'mssql+pytds' 
SERVER = os.getenv('AZURE_SQL_SERVER')
DATABASE = os.getenv('AZURE_SQL_DATABASE')
USERNAME = os.getenv('AZURE_SQL_USERNAME')
PASSWORD = os.getenv('AZURE_SQL_PASSWORD')

# String de conexão para o pytds
db_url = f"{DIALECT}://{USERNAME}:{PASSWORD}@{SERVER}:1433/{DATABASE}"

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
                print("Conexão com o banco de dados (usando pytds) bem-sucedida.")
            else:
                raise Exception("Falha na execução do teste básico.")
    except Exception as e:
        print(f"Erro na conexão: {e}")
        raise

if __name__ == "__main__":
    check_db_connection()
