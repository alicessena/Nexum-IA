# database.py
from db_session import get_db
from sqlalchemy import text
import pandas as pd

def fetch_all(query: str, params: dict = None):
    """Executa uma query e retorna todos os resultados como uma lista de dicionários."""
    db_gen = get_db()
    db = next(db_gen)
    try:
        result = db.execute(text(query), params or {})
        # CORREÇÃO: Converte o resultado do SQLAlchemy para uma lista de dicionários
        return [dict(row._mapping) for row in result]
    finally:
        db.close()

def fetch_one(query: str, params: dict = None):
    """Executa uma query e retorna o primeiro resultado como um dicionário."""
    db_gen = get_db()
    db = next(db_gen)
    try:
        result = db.execute(text(query), params or {}).first()
        if result:
            return dict(result._mapping)
        return None
    finally:
        db.close()

def execute_query(query: str, params: dict = None):
    """Executa uma query de inserção, atualização ou deleção."""
    db_gen = get_db()
    db = next(db_gen)
    try:
        result = db.execute(text(query), params or {})
        db.commit()
        # Retorna o número de linhas afetadas
        return True, result.rowcount
    except Exception as e:
        db.rollback()
        # Retorna a mensagem de erro
        return False, str(e)
    finally:
        db.close()
