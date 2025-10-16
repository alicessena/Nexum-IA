# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import stock
import sales
import worker
from database.user_manager import GerenciadorUsuarios
import decimal
import datetime

# --- Configuração da Aplicação ---
app = Flask(__name__)
# Habilita o CORS para permitir que um front-end em outro domínio acesse a API
CORS(app)

# --- Funções Auxiliares ---
# Converte dados do banco (com decimais e datas) para um formato JSON válido
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError ("Type %s not serializable" % type(obj))

# Sobrescreve o json_provider padrão do Flask para usar nosso serializador
from flask.json.provider import JSONProvider
class CustomJSONProvider(JSONProvider):
    def dumps(self, obj, **kwargs):
        import json
        return json.dumps(obj, **kwargs, default=json_serial)

app.json = CustomJSONProvider(app)


# --- Rotas da API ---

# Rota principal para testar se a API está no ar
@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "Nexum API is running!"}), 200

# --- Rotas de Produtos (Stock) ---

@app.route('/api/products', methods=['GET'])
def get_all_products():
    """Endpoint para listar todos os produtos."""
    products = stock.service_get_all_products()
    return jsonify(products)

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Endpoint para buscar um produto específico pelo ID."""
    product = stock.service_get_product(product_id)
    if product:
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

# NOTA: A criação e atualização de produtos não estavam totalmente implementadas
# no seu `stock.py`. Adicionei uma estrutura básica que você pode expandir.
@app.route('/api/products', methods=['POST'])
def create_product():
    """Endpoint para criar um novo produto."""
    data = request.json
    # Adapte os campos conforme a sua tabela `produtos_estoque`
    success, message = stock.service_create_product(**data)
    if success:
        return jsonify({"message": message}), 201
    return jsonify({"error": message}), 400

@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Endpoint para atualizar um produto existente."""
    data = request.json
    success, message = stock.service_update_product(product_id, **data)
    if success:
        return jsonify({"message": message}), 200
    return jsonify({"error": message}), 404

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Endpoint para remover um produto."""
    if stock.service_remove_product(product_id):
        return jsonify({"message": "Product removed successfully"}), 200
    return jsonify({"error": "Product not found or could not be removed"}), 404

@app.route('/api/suggestions/acquisition', methods=['GET'])
def get_acquisition_suggestions():
    """Endpoint que retorna sugestões de compra calculadas pela Stored Procedure."""
    suggestions = stock.service_generate_acquisition_suggestion()
    return jsonify(suggestions)

@app.route('/api/alerts/stock', methods=['GET'])
def get_stock_alerts():
    """Endpoint que retorna produtos críticos (usando a View)."""
    alerts = stock.service_check_stock_alerts()
    return jsonify(alerts)


# --- Rotas de Usuários (Worker/User Manager) ---

@app.route('/api/users/register', methods=['POST'])
def register_user():
    """Endpoint para registrar um novo usuário."""
    data = request.json
    try:
        # A função em user_manager.py espera um objeto `date`
        data['data_nascimento'] = datetime.datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date()
        
        manager = GerenciadorUsuarios()
        manager.conectar()
        result = manager.criar_usuario(**data)
        manager.desconectar()
        
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/users/login', methods=['POST'])
def login_user():
    """Endpoint para autenticar um usuário."""
    data = request.json
    try:
        auth_result = worker.service_authenticate_user(data['usuario'], data['senha'])
        if auth_result[0]: # Se a autenticação foi bem-sucedida
            return jsonify({"message": auth_result[1], "access_level": auth_result[2]})
        else:
            return jsonify({"error": auth_result[1]}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 401

# --- Rotas de Vendas (Sales) ---
# Similar às de produtos, implementando os serviços de `sales.py`.

@app.route('/api/sales', methods=['GET'])
def get_all_sales():
    """Endpoint para listar todas as vendas."""
    all_sales = sales.service_get_all_sales()
    return jsonify(all_sales)

@app.route('/api/sales', methods=['POST'])
def create_sale():
    """Endpoint para criar um novo registro de venda."""
    data = request.json
    sale_id, message = sales.service_create_sale(**data)
    if sale_id:
        return jsonify({"message": message, "sale_id": sale_id}), 201
    return jsonify({"error": message}), 400


# --- Execução da Aplicação ---
if __name__ == '__main__':
    # Usar `debug=True` apenas em ambiente de desenvolvimento
    app.run(host='0.0.0.0', port=5000, debug=True)