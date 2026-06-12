"""
Factory da aplicação Flask.

Cria e configura a instância do Flask usando o padrão Application Factory.
Inicializa todas as extensões e registra os Blueprints por domínio.
"""

import os
from flask import Flask
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()


def create_app(config_name=None):
    """
    Cria e configura a aplicação Flask.

    Args:
        config_name: Nome da configuração ('development', 'production', 'testing').
                     Se None, usa a variável FLASK_ENV ou 'development'.

    Returns:
        Instância configurada do Flask.
    """

    app = Flask(__name__)

    # Determina a configuração
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    # Carrega a configuração
    from config import config
    app.config.from_object(config.get(config_name, config['default']))

    # Inicializa extensões
    _init_extensions(app)

    # Registra Blueprints
    _register_blueprints(app)

    # Registra template filters e context processors
    _register_template_utils(app)

    # Cria o diretório instance se não existir (para SQLite local)
    _ensure_instance_folder(app)

    return app


def _init_extensions(app):
    """Inicializa todas as extensões Flask."""
    from app.extensions import db, login_manager, migrate, csrf

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # Callback do Flask-Login para carregar o usuário da sessão
    from app.models.usuario import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(Usuario, int(user_id))


def _register_blueprints(app):
    """Registra todos os Blueprints da aplicação."""
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.usuarios import usuarios_bp
    from app.routes.marketplaces import marketplaces_bp
    from app.routes.transportadoras import transportadoras_bp
    from app.routes.funcionarios import funcionarios_bp
    from app.routes.encomendas import encomendas_bp
    from app.routes.consultas import consultas_bp
    from app.routes.relatorios import relatorios_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(marketplaces_bp)
    app.register_blueprint(transportadoras_bp)
    app.register_blueprint(funcionarios_bp)
    app.register_blueprint(encomendas_bp)
    app.register_blueprint(consultas_bp)
    app.register_blueprint(relatorios_bp)


def _register_template_utils(app):
    """Registra filtros e context processors para os templates Jinja2."""

    @app.template_filter('data_br')
    def data_br_filter(value):
        """Formata data para dd/mm/yyyy."""
        if value is None:
            return ''
        if hasattr(value, 'strftime'):
            return value.strftime('%d/%m/%Y')
        return str(value)

    @app.template_filter('datetime_br')
    def datetime_br_filter(value):
        """Formata data/hora para dd/mm/yyyy HH:MM."""
        if value is None:
            return ''
        if hasattr(value, 'strftime'):
            return value.strftime('%d/%m/%Y %H:%M')
        return str(value)

    @app.template_filter('moeda_br')
    def moeda_br_filter(value):
        """Formata valor monetário para R$ 1.234,56."""
        if value is None:
            return 'R$ 0,00'
        try:
            valor = float(value)
            formatted = f'{valor:,.2f}'
            # Troca separadores para padrão brasileiro
            formatted = formatted.replace(',', 'X').replace('.', ',').replace('X', '.')
            return f'R$ {formatted}'
        except (ValueError, TypeError):
            return 'R$ 0,00'

    @app.template_filter('numero_br')
    def numero_br_filter(value):
        """Formata número com separador de milhar brasileiro."""
        if value is None:
            return '0'
        try:
            valor = int(value)
            formatted = f'{valor:,}'.replace(',', '.')
            return formatted
        except (ValueError, TypeError):
            return '0'

    @app.context_processor
    def inject_global_vars():
        """Injeta variáveis globais em todos os templates."""
        return {
            'app_name': 'Sistema de Encomendas',
            'app_version': '1.0.0',
        }


def _ensure_instance_folder(app):
    """Cria o diretório instance se necessário (para SQLite local)."""
    instance_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance')
    if not os.path.exists(instance_path):
        os.makedirs(instance_path, exist_ok=True)
