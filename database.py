# database.py
import pyodbc
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração da conexão com o banco de dados
AZURE_SQL_CONFIG = {
    'server': os.getenv('AZURE_SQL_SERVER'),
    'database': os.getenv('AZURE_SQL_DATABASE'),
    'username': os.getenv('AZURE_SQL_USERNAME'),
    'password': os.getenv('AZURE_SQL_PASSWORD'),
    # Use o driver correto para o ambiente Vercel (Linux)
    'driver': '{ODBC Driver 18 for SQL Server}'
}

def get_connection():
    """Cria e retorna uma nova conexão com o banco de dados."""
    conn_str = (
        f"DRIVER={AZURE_SQL_CONFIG['driver']};"
        f"SERVER={AZURE_SQL_CONFIG['server']};"
        f"DATABASE={AZURE_SQL_CONFIG['database']};"
        f"UID={AZURE_SQL_CONFIG['username']};"
        f"PWD={AZURE_SQL_CONFIG['password']};"
        f"Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    )
    try:
        conn = pyodbc.connect(conn_str)
        return conn
    except Exception as e:
        print(f"Erro de conexão com o banco de dados: {e}")
        # Em um ambiente de produção, você pode querer logar o erro
        # em vez de apenas imprimir.
        raise

def fetch_all(query, params=None):
    """Executa uma query e retorna todos os resultados como uma lista de dicionários."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results
    finally:
        cursor.close()
        conn.close()

def fetch_one(query, params=None):
    """Executa uma query e retorna o primeiro resultado como um dicionário."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
            
        columns = [column[0] for column in cursor.description]
        row = cursor.fetchone()
        if row:
            return dict(zip(columns, row))
        return None
    finally:
        cursor.close()
        conn.close()

def execute_query(query, params=None):
    """Executa uma query de inserção, atualização ou deleção."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        # Retorna o número de linhas afetadas
        return True, cursor.rowcount
    except Exception as e:
        conn.rollback()
        # Retorna a mensagem de erro
        return False, str(e)
    finally:
        cursor.close()
        conn.close()