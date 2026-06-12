"""
Model: Marketplace
Tabela: marketplaces

Cadastro de marketplaces de e-commerce (ex: Mercado Livre, Amazon, Shopee).
"""

from datetime import datetime, timezone
from app.extensions import db


class Marketplace(db.Model):
    """Modelo de marketplace."""

    __tablename__ = 'marketplaces'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    nome_conta = db.Column(db.String(100), nullable=True)
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

    # Relacionamento: encomendas vinculadas a este marketplace
    encomendas = db.relationship(
        'Encomenda',
        backref=db.backref('marketplace', lazy='joined'),
        lazy='dynamic',
        foreign_keys='Encomenda.marketplace_id'
    )

    def __repr__(self):
        return f'<Marketplace {self.id}: {self.nome}>'

    def to_dict(self):
        """Serializa o modelo para dicionário."""
        return {
            'id': self.id,
            'nome': self.nome,
            'nome_conta': self.nome_conta,
            'ativo': self.ativo,
            'criado_em': self.criado_em.isoformat() if self.criado_em else None,
            'atualizado_em': self.atualizado_em.isoformat() if self.atualizado_em else None,
        }
