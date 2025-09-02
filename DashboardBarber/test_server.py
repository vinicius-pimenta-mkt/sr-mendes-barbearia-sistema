#!/usr/bin/env python3
import os
import sys

# Adicionar o diretório pai ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

try:
    from flask import Flask, send_from_directory
    from flask_cors import CORS
    
    print("Imports básicos OK")
    
    # Importar módulos do projeto
    from src.models.user import db
    from src.routes.user import user_bp
    from src.routes.auth import auth_bp
    from src.routes.clientes import clientes_bp
    from src.routes.agendamentos import agendamentos_bp
    from src.routes.relatorios import relatorios_bp
    
    print("Imports do projeto OK")
    
    app = Flask(__name__, static_folder=os.path.join(current_dir, 'src', 'static'))
    app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'
    
    # Habilitar CORS
    CORS(app)
    
    print("Flask app criado")
    
    # Registrar blueprints
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(clientes_bp, url_prefix='/api')
    app.register_blueprint(agendamentos_bp, url_prefix='/api')
    app.register_blueprint(relatorios_bp, url_prefix='/api')
    
    print("Blueprints registrados")
    
    # Configurar banco de dados
    db_path = os.path.join(current_dir, 'src', 'database', 'app.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    print("Banco de dados configurado")
    
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        static_folder_path = app.static_folder
        if static_folder_path is None:
            return "Static folder not configured", 404
        
        if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
            return send_from_directory(static_folder_path, path)
        else:
            index_path = os.path.join(static_folder_path, 'index.html')
            if os.path.exists(index_path):
                return send_from_directory(static_folder_path, 'index.html')
            else:
                return "index.html not found", 404
    
    print("Rotas configuradas")
    print(f"Static folder: {app.static_folder}")
    print(f"Index.html exists: {os.path.exists(os.path.join(app.static_folder, 'index.html'))}")
    
    print("Iniciando servidor na porta 5003...")
    app.run(host='0.0.0.0', port=5003, debug=False)
    
except Exception as e:
    print(f"Erro: {e}")
    import traceback
    traceback.print_exc()

