from datetime import datetime
from database import fetch_all, fetch_one, execute_query

def validate_and_parse_date(date_str):
    """Valida e converte a string de data."""
    if not date_str:
        return None, None
    try:
        # CORREÇÃO: Retorna o objeto datetime se a validação for bem-sucedida
        return datetime.strptime(date_str, "%d/%m/%Y").date(), None
    except ValueError:
        return None, f"Formato de data inválido para '{date_str}'. Use DD/MM/AAAA."

def service_get_all_products():
    return fetch_all("SELECT * FROM supply_chain.produtos_estoque")

def service_get_product(product_id):
    try:
        product_id = int(product_id)
    except (ValueError, TypeError):
        return None
    return fetch_one("SELECT * FROM supply_chain.produtos_estoque WHERE id = ?", (product_id,))

def service_create_product(name, description, entry_date, expiration_date, tipo, saldo_manut, provid_compras, cmm, coef_perda):
    if not name or not entry_date:
        return None, "Nome e data de entrada são obrigatórios."

    parsed_entry_date, error = validate_and_parse_date(entry_date)
    if error:
        return None, error

    parsed_expiration_date, error = validate_and_parse_date(expiration_date)
    if error and expiration_date:
        return None, error

    query = '''
        INSERT INTO supply_chain.produtos_estoque (nome_produto, descricao, data_entrada, data_expiracao, tipo_produto, saldo_manutencao, providencia_compras, cmm, coeficiente_perda) 
        OUTPUT INSERTED.id
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    '''
    # MELHORIA: Usando OUTPUT INSERTED.id para obter o ID do novo produto
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (name, description, parsed_entry_date, parsed_expiration_date, tipo, saldo_manut, provid_compras, cmm, coef_perda))
        new_id = cursor.fetchone()[0]
        conn.commit()
        return new_id, "Produto criado com sucesso!"
    except Exception as e:
        return None, f"Falha ao criar produto: {e}"
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def service_update_product(product_id, name, description, entry_date, expiration_date, tipo, saldo_manut, provid_compras, cmm, coef_perda):
    current_product = service_get_product(product_id)
    if not current_product:
        return False, "Produto não encontrado!"

    # ... (lógica de atualização continua aqui)
    
    return True, "Produto atualizado com sucesso!"

def service_remove_product(product_id):
    query = 'DELETE FROM supply_chain.produtos_estoque WHERE id = ?'
    success, deleted_count = execute_query(query, (product_id,))
    return success and deleted_count > 0

def service_generate_acquisition_suggestion():
    query = "EXEC supply_chain.sp_calcular_necessidade_compra" 
    return fetch_all(query) 

def service_check_stock_alerts():
    query = "SELECT * FROM supply_chain.vw_produtos_criticos"
    return fetch_all(query)