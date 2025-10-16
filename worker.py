from user_manager import GerenciadorUsuarios 
from database import fetch_all, fetch_one, execute_query

user_manager = GerenciadorUsuarios()

def service_get_all_workers():

    query = "SELECT matricula, usuario, nivel_acesso FROM supply_chain.users" 
    return fetch_all(query)

def service_get_worker(matricula):
    query = "SELECT matricula, usuario, nivel_acesso FROM supply_chain.users WHERE matricula = ?"
    return fetch_one(query, (matricula,))

def service_create_worker(usuario, senha, matricula, nivel_acesso):

    success, msg_or_error = user_manager.criar_usuario(usuario, senha, matricula, nivel_acesso)
    
    if success:
        return matricula, "Registro de usuário concluído com sucesso!"
    else:
        return None, msg_or_error

def service_update_worker(matricula, usuario=None, senha=None, nivel_acesso=None):
  
    success, msg = user_manager.atualizar_usuario(matricula, usuario, senha, nivel_acesso)
    return success, msg

def service_remove_worker(matricula):
    query = "DELETE FROM supply_chain.users WHERE matricula = ?"
    success, deleted_count = execute_query(query, (matricula,))
    return success and deleted_count > 0

def service_authenticate_user(usuario, senha):
    
    authenticated, msg, nivel = user_manager.autenticar(usuario, senha)
    return authenticated, msg, nivel