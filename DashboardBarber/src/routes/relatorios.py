from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta

relatorios_bp = Blueprint('relatorios', __name__)

@relatorios_bp.route('/relatorios/dashboard', methods=['GET'])
def get_dashboard_data():
    # Dados mock para o dashboard
    dashboard_data = {
        "atendimentos_hoje": 12,
        "receita_dia": 580.00,
        "proximos_agendamentos": 3,
        "servicos_realizados": 12,
        "proximos_agendamentos_lista": [
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
        "servicos_realizados_lista": [
            {"servico": "Barba", "quantidade": 3},
            {"servico": "Corte e Barba", "quantidade": 5},
            {"servico": "Corte", "quantidade": 2},
            {"servico": "Sobrancelha", "quantidade": 1},
            {"servico": "Corte e Sobrancelha", "quantidade": 1}
        ]
    }
    return jsonify(dashboard_data)

@relatorios_bp.route('/relatorios/mensal', methods=['GET'])
def get_relatorio_mensal():
    # Dados mock para relatório mensal
    relatorio_mensal = {
        "mes": "Agosto 2025",
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
    """Endpoint para receber dados do N8N"""
    data = request.get_json()
    
    # Aqui você processaria os dados vindos do N8N
    # Por exemplo: novo agendamento, atualização de cliente, etc.
    
    return jsonify({
        "status": "success",
        "message": "Dados recebidos do N8N com sucesso",
        "data": data
    })

