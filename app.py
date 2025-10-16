from flask import Flask, request, jsonify
from flask_cors import CORS
import stock
import sales
import worker
from database.user_manager import GerenciadorUsuarios
import decimal
import datetime

app = Flask(__name__)
CORS(app)

# --- Funções Auxiliares ---
def json_serial(obj):
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError(f"O tipo {type(obj)} não é serializável para JSON")

from flask.json.provider import JSONProvider

class CustomJSONProvider(JSONProvider):
    def dumps(self, obj, **kwargs):
        import json
        return json.dumps(obj, **kwargs, default=json_serial)

app.json = CustomJSONProvider(app)


# --- Rotas da API ---

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "A API Nexum está no ar!"}), 200

# --- Rotas de Produtos (Stock) ---
@app.route('/api/products', methods=['GET'])
def get_all_products():
    products = stock.service_get_all_products()
    return jsonify(products)

# --- Rotas de Usuários ---

@app.route('/api/users/register', methods=['POST'])
def register_user():
    """Endpoint para registrar um novo usuário."""
    data = request.json
    try:
        # Converte a data de string para objeto date
        data['data_nascimento'] = datetime.datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date()
        
        # CORREÇÃO: Chama o worker service que usa o user_manager
        success, message = worker.service_create_worker(data)
        
        if success:
            return jsonify({"message": message}), 201
        else:
            return jsonify({"error": message}), 400
            
    except Exception as e:
        return jsonify({"error": f"Erro interno: {e}"}), 500

@app.route('/api/users/login', methods=['POST'])
def login_user():
    """Endpoint para autenticar um usuário."""
    data = request.json
    try:
        # CORREÇÃO: A função agora retorna (autenticado, mensagem, nível_de_acesso)
        authenticated, message, access_level = worker.service_authenticate_user(data['usuario'], data['senha'])
        
        if authenticated:
            return jsonify({"message": message, "access_level": access_level})
        else:
            return jsonify({"error": message}), 401
    except Exception as e:
        return jsonify({"error": f"Erro de autenticação: {e}"}), 401
        
# --- Rotas de Vendas (Sales) ---

@app.route('/api/sales', methods=['GET'])
def get_all_sales():
    all_sales = sales.service_get_all_sales()
    return jsonify(all_sales)

@app.route('/api/sales', methods=['POST'])
def create_sale():
    data = request.json
    sale_id, message = sales.service_create_sale(**data)
    if sale_id:
        return jsonify({"message": message, "sale_id": sale_id}), 201
    return jsonify({"error": message}), 400

# --- Execução ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)