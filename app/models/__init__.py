# app/models/__init__.py
# Importação centralizada de todos os modelos SQLAlchemy
# Cada modelo é importado aqui para facilitar o acesso via:
#   from app.models import Usuario, Marketplace, etc.

from app.models.usuario import Usuario
from app.models.marketplace import Marketplace
from app.models.transportadora import Transportadora
from app.models.funcionario import Funcionario
from app.models.encomenda import Encomenda

__all__ = [
    'Usuario',
    'Marketplace',
    'Transportadora',
    'Funcionario',
    'Encomenda',
]
