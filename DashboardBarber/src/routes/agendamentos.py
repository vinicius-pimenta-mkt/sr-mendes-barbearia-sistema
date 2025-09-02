from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta

agendamentos_bp = Blueprint('agendamentos', __name__)

# Dados mock para demonstração
agendamentos_mock = [
    {
        "id": 1,
        "cliente": "João Silva",
        "servico": "Corte e Barba",
        "data": "2025-08-28",
        "hora": "14:30",
        "status": "Confirmado",
        "preco": 50.00
    },
    {
        "id": 2,
        "cliente": "Pedro Santos",
        "servico": "Corte",
        "data": "2025-08-28",
        "hora": "15:00",
        "status": "Confirmado",
        "preco": 30.00
    },
    {
        "id": 3,
        "cliente": "Carlos Lima",
        "servico": "Barba",
        "data": "2025-08-28",
        "hora": "15:30",
        "status": "Pendente",
        "preco": 25.00
    }
]

@agendamentos_bp.route('/agendamentos', methods=['GET'])
def get_agendamentos():
    return jsonify(agendamentos_mock)

@agendamentos_bp.route('/agendamentos', methods=['POST'])
def create_agendamento():
    data = request.get_json()
    novo_agendamento = {
        "id": len(agendamentos_mock) + 1,
        "cliente": data.get('cliente'),
        "servico": data.get('servico'),
        "data": data.get('data'),
        "hora": data.get('hora'),
        "status": data.get('status', 'Pendente'),
        "preco": data.get('preco', 0.00)
    }
    agendamentos_mock.append(novo_agendamento)
    return jsonify(novo_agendamento), 201

@agendamentos_bp.route('/agendamentos/<int:agendamento_id>', methods=['PUT'])
def update_agendamento(agendamento_id):
    data = request.get_json()
    for agendamento in agendamentos_mock:
        if agendamento['id'] == agendamento_id:
            agendamento.update(data)
            return jsonify(agendamento)
    return jsonify({'message': 'Agendamento não encontrado'}), 404

@agendamentos_bp.route('/agendamentos/<int:agendamento_id>', methods=['DELETE'])
def delete_agendamento(agendamento_id):
    global agendamentos_mock
    agendamentos_mock = [a for a in agendamentos_mock if a['id'] != agendamento_id]
    return jsonify({'message': 'Agendamento removido com sucesso'})

@agendamentos_bp.route('/agendamentos/hoje', methods=['GET'])
def get_agendamentos_hoje():
    hoje = datetime.now().strftime('%Y-%m-%d')
    agendamentos_hoje = [a for a in agendamentos_mock if a['data'] == hoje]
    return jsonify(agendamentos_hoje)

