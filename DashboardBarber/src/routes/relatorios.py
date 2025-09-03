from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from .auth import token_required

relatorios_bp = Blueprint('relatorios', __name__)

@relatorios_bp.route('/relatorios/dashboard', methods=['GET'])
@token_required
def get_dashboard_data(current_user):
    # Dados mock para o dashboard
    dashboard_data = {
        "agendamentos_hoje": 3,
        "total_clientes": 3,
        "servicos_este_mes": 12,
        "receita_este_mes": 580.00,
        "proximos_agendamentos": [
            {
                "cliente": "João Silva",
                "servico": "Corte e Barba",
                "hora": "14:30",
                "status": "Confirmado"
            },
            {
                "cliente": "Pedro Santos",
                "servico": "Corte",
                "hora": "15:00",
                "status": "Confirmado"
            },
            {
                "cliente": "Carlos Lima",
                "servico": "Barba",
                "hora": "15:30",
                "status": "Pendente"
            }
        ],
        "atividades_recentes": [
            {"acao": "Novo agendamento", "cliente": "João Silva", "tempo": "há 2 horas"},
            {"acao": "Cliente atualizado", "cliente": "Pedro Santos", "tempo": "há 3 horas"},
            {"acao": "Agendamento confirmado", "cliente": "Carlos Lima", "tempo": "há 4 horas"}
        ]
    }
    return jsonify(dashboard_data)

@relatorios_bp.route('/relatorios/mensal', methods=['GET'])
@token_required
def get_relatorio_mensal(current_user):
    # Dados mock para relatório mensal
    relatorio_mensal = {
        "mes": "Setembro 2025",
        "total_atendimentos": 350,
        "receita_total": 15750.00,
        "ticket_medio": 45.00,
        "servicos_mais_procurados": [
            {"servico": "Corte e Barba", "quantidade": 150},
            {"servico": "Corte", "quantidade": 120},
            {"servico": "Barba", "quantidade": 80}
        ]
    }
    return jsonify(relatorio_mensal)

@relatorios_bp.route('/relatorios/n8n', methods=['POST'])
def webhook_n8n():
    """Endpoint para receber dados do N8N - sem autenticação para webhooks"""
    data = request.get_json()
    
    # Aqui você processaria os dados vindos do N8N
    # Por exemplo: novo agendamento, atualização de cliente, etc.
    
    return jsonify({
        "status": "success",
        "message": "Dados recebidos do N8N com sucesso",
        "data": data
    })

