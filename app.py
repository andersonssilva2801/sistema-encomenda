"""
Ponto de entrada da aplicação Flask.

Este arquivo é usado para:
- Executar localmente: python app.py
- Gunicorn em produção: gunicorn app:app

Uso local:
    set FLASK_ENV=development
    python app.py
"""

import os
from app import create_app

# Determina o ambiente (development, production, testing)
config_name = os.environ.get('FLASK_ENV', 'development')

# Cria a instância da aplicação
app = create_app(config_name)

if __name__ == '__main__':
    # Execução local em modo debug
    port = int(os.environ.get('PORT', 5000))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=app.config.get('DEBUG', True)
    )
