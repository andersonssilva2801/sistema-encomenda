"""
Extensões Flask centralizadas.

Todas as extensões são inicializadas aqui e importadas
nos demais módulos para evitar imports circulares.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

# Instâncias das extensões (inicializadas sem app)
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()

# Configuração do Flask-Login
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'
login_manager.login_message_category = 'warning'
