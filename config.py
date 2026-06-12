"""
Configurações da aplicação Flask.

Define classes de configuração para os ambientes:
- DevelopmentConfig: desenvolvimento local (SQLite)
- ProductionConfig: produção (PostgreSQL no Supabase)
- TestingConfig: testes automatizados
"""

import os
from datetime import timedelta

# Diretório base do projeto
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Configuração base compartilhada por todos os ambientes."""

    # Chave secreta para sessões e CSRF
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 300,
        'pool_pre_ping': True,
    }

    # Flask-Login
    REMEMBER_COOKIE_DURATION = timedelta(days=7)
    REMEMBER_COOKIE_SECURE = False
    REMEMBER_COOKIE_HTTPONLY = True

    # Paginação padrão
    ITEMS_PER_PAGE = 10

    # Upload (se necessário no futuro)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

    # Timezone para exibição
    TIMEZONE = 'America/Sao_Paulo'


class DevelopmentConfig(Config):
    """Configuração para ambiente de desenvolvimento."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        f'sqlite:///{os.path.join(basedir, "instance", "sistema_encomenda.db")}'
    )
    # Log de queries SQL no console
    SQLALCHEMY_ECHO = False


class ProductionConfig(Config):
    """Configuração para ambiente de produção (Render + Supabase)."""

    DEBUG = False

    # Render usa DATABASE_URL com 'postgres://' mas SQLAlchemy precisa de 'postgresql://'
    _database_url = os.environ.get('DATABASE_URL', '')
    if _database_url.startswith('postgres://'):
        _database_url = _database_url.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = _database_url

    # Segurança em produção
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    REMEMBER_COOKIE_SECURE = True

    # Pool de conexões mais robusto para produção
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 300,
        'pool_pre_ping': True,
        'pool_size': 5,
        'max_overflow': 10,
    }


class TestingConfig(Config):
    """Configuração para testes automatizados."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    LOGIN_DISABLED = False


# Mapeamento de configurações por nome
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
}
