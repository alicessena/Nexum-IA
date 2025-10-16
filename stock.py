from datetime import datetime
from database import fetch_all, fetch_one, execute_query

def validate_date_format(date_str):
    try:
        datetime.strptime(date_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def service_get_all_products():
    return fetch_all("SELECT * FROM supply_chain.produtos_estoque")

def service_get_product(product_id):
    try:
        product_id = int(product_id)
    except ValueError: return None
    return fetch_one("SELECT * FROM supply_chain.produtos_estoque WHERE id = ?", (product_id,))

def service_create_product(name, description, entry_date, expiration_date, tipo, saldo_manut, provid_compras, cmm, coef_perda):
    if not name or not entry_date: return None, "Nome e data de entrada são obrigatórios."
    if entry_date and not validate_date_format(entry_date): return None, "Formato de data de entrada inválido. Use DD/MM/AAAA."
    if expiration_date and not validate_date_format(expiration_date): return None, "Formato de data de expiração inválido. Use DD/MM/AAAA."

    query = '''
        INSERT INTO supply_chain.produtos_estoque (nome_produto, descricao, data_entrada, data_expiracao, tipo_produto, saldo_manutencao, providencia_compras, cmm, coeficiente_perda) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    '''
    success, result_or_error = execute_query(
        query,
        (name, description, entry_date, expiration_date, tipo, saldo_manut, provid_compras, cmm, coef_perda)
    )
    
    if success:
    
        return 'ID_INSERIDO', "Produto criado com sucesso!"
    else:
        return None, f"Falha ao criar produto: {result_or_error}"

def service_update_product(product_id, name, description, entry_date, expiration_date, tipo, saldo_manut, provid_compras, cmm, coef_perda):
    current_product = service_get_product(product_id)
    if not current_product: return False, "Produto não encontrado!"

    if (entry_date and not validate_date_format(entry_date)) or (expiration_date and not validate_date_format(expiration_date)):
        return False, "Formato de data inválido. Use DD/MM/AAAA."

    new_name = name if name is not None else current_product.get('nome_produto')
   
    
    query = '''
        UPDATE supply_chain.produtos_estoque SET 
        nome_produto=?, descricao=?, data_entrada=?, data_expiracao=?, tipo_produto=?, 
        saldo_manutencao=?, providencia_compras=?, cmm=?, coeficiente_perda=? 
        WHERE id=?
    '''
    success, updated_count = execute_query(
        query,
        (new_name, description, entry_date, expiration_date, tipo, saldo_manut, provid_compras, cmm, coef_perda, product_id)
    )
    
    return success and updated_count > 0, "Produto atualizado com sucesso!" if success and updated_count > 0 else "Produto não encontrado ou falha na atualização."

def service_remove_product(product_id):
    query = 'DELETE FROM supply_chain.produtos_estoque WHERE id = ?'
    success, deleted_count = execute_query(query, (product_id,))
    return success and deleted_count > 0

def service_generate_acquisition_suggestion():
    query = "EXEC supply_chain.sp_calcular_necessidade_compra" 
    return fetch_all(query) 
def service_check_stock_alerts():
    query = "SELECT * FROM supply_chain.vw_produtos_criticos"
    alerts = fetch_all(query)
    
    return alerts