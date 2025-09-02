from flask import Blueprint, request, jsonify

clientes_bp = Blueprint('clientes', __name__)

# Dados mock para demonstração
clientes_mock = [
    {"id": 1, "nome": "João Silva", "telefone": "(11) 99999-9999", "email": "joao@email.com"},
    {"id": 2, "nome": "Pedro Santos", "telefone": "(11) 88888-8888", "email": "pedro@email.com"},
    {"id": 3, "nome": "Carlos Lima", "telefone": "(11) 77777-7777", "email": "carlos@email.com"}
]

@clientes_bp.route('/clientes', methods=['GET'])
def get_clientes():
    return jsonify(clientes_mock)

@clientes_bp.route('/clientes', methods=['POST'])
def create_cliente():
    data = request.get_json()
    novo_cliente = {
        "id": len(clientes_mock) + 1,
        "nome": data.get('nome'),
        "telefone": data.get('telefone'),
        "email": data.get('email')
    }
    clientes_mock.append(novo_cliente)
    return jsonify(novo_cliente), 201

@clientes_bp.route('/clientes/<int:cliente_id>', methods=['PUT'])
def update_cliente(cliente_id):
    data = request.get_json()
    for cliente in clientes_mock:
        if cliente['id'] == cliente_id:
            cliente.update(data)
            return jsonify(cliente)
    return jsonify({'message': 'Cliente não encontrado'}), 404

@clientes_bp.route('/clientes/<int:cliente_id>', methods=['DELETE'])
def delete_cliente(cliente_id):
    global clientes_mock
    clientes_mock = [c for c in clientes_mock if c['id'] != cliente_id]
    return jsonify({'message': 'Cliente removido com sucesso'})

