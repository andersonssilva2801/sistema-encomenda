"""
Model: Funcionario
Tabela: funcionarios

Cadastro de funcionários responsáveis pelas encomendas.
"""

from datetime import datetime, timezone
from app.extensions import db


class Funcionario(db.Model):
    """Modelo de funcionário."""

    __tablename__ = 'funcionarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
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

    # Relacionamento: encomendas vinculadas a este funcionário
    encomendas = db.relationship(
        'Encomenda',
        backref=db.backref('funcionario', lazy='joined'),
        lazy='dynamic',
        foreign_keys='Encomenda.funcionario_id'
    )

    def __repr__(self):
        return f'<Funcionario {self.id}: {self.nome}>'

    def to_dict(self):
        """Serializa o modelo para dicionário."""
        return {
            'id': self.id,
            'nome': self.nome,
            'ativo': self.ativo,
            'criado_em': self.criado_em.isoformat() if self.criado_em else None,
            'atualizado_em': self.atualizado_em.isoformat() if self.atualizado_em else None,
        }
