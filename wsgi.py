import os
from app import create_app
from app.extensions import db

app = create_app(os.environ.get('FLASK_ENV', 'production'))

# Cria tabelas novas sem afetar as existentes
with app.app_context():
    db.create_all()
