"""
Model: Transportadora
Tabela: transportadoras

Cadastro de transportadoras com valor padrão de frete.
"""

from datetime import datetime, timezone
from app.extensions import db


class Transportadora(db.Model):
    """Modelo de transportadora."""

    __tablename__ = 'transportadoras'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    valor_padrao = db.Column(
        db.Numeric(10, 2),
        nullable=False,
        default=0.00
    )
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    criado_em = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    atualizado_em = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    # Relacionamento: encomendas vinculadas a esta transportadora
    encomendas = db.relationship(
        'Encomenda',
        backref=db.backref('transportadora', lazy='joined'),
        lazy='dynamic',
        foreign_keys='Encomenda.transportadora_id'
    )

    def __repr__(self):
        return f'<Transportadora {self.id}: {self.nome}>'

    @property
    def valor_padrao_formatado(self):
        """Retorna o valor formatado em R$."""
        return f'R$ {self.valor_padrao:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

    def to_dict(self):
        """Serializa o modelo para dicionário."""
        return {
            'id': self.id,
            'nome': self.nome,
            'valor_padrao': float(self.valor_padrao) if self.valor_padrao else 0.00,
            'ativo': self.ativo,
            'criado_em': self.criado_em.isoformat() if self.criado_em else None,
            'atualizado_em': self.atualizado_em.isoformat() if self.atualizado_em else None,
        }
