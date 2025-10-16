# database.py
from db_session import get_db
from sqlalchemy import text

def fetch_all(query: str, params=None):
    """Executa uma query e retorna todos os resultados como uma lista de dicionários."""
    # Garante que os parâmetros sejam um dicionário
    params = params or {}
    db_gen = get_db()
    db = next(db_gen)
    try:
        # Passa os parâmetros para o método execute
        result = db.execute(text(query), params)
        return [dict(row._mapping) for row in result]
    finally:
        db.close()

def fetch_one(query: str, params=None):
    """Executa uma query e retorna o primeiro resultado como um dicionário."""
    # Garante que os parâmetros sejam um dicionário
    params = params or {}
    db_gen = get_db()
    db = next(db_gen)
    try:
        result = db.execute(text(query), params).first()
        if result:
            return dict(result._mapping)
        return None
    finally:
        db.close()

def execute_query(query: str, params=None):
    """Executa uma query de inserção, atualização ou deleção."""
    # Garante que os parâmetros sejam um dicionário
    params = params or {}
    db_gen = get_db()
    db = next(db_gen)
    try:
        result = db.execute(text(query), params)
        db.commit()
        return True, result.rowcount
    except Exception as e:
        db.rollback()
        return False, str(e)
    finally:
        db.close()
