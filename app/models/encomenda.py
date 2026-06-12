"""
Model: Encomenda
Tabela: encomendas

Registro de movimentações de encomendas (envios e devoluções).
Cada encomenda registra automaticamente o usuário e a data/hora da operação.
"""

from datetime import datetime, timezone, date
from app.extensions import db


class Encomenda(db.Model):
    """Modelo de encomenda (movimentação)."""

    __tablename__ = 'encomendas'

    # Tipos de movimento permitidos
    TIPOS_MOVIMENTO = ['Envio', 'Devolução']

    id = db.Column(db.Integer, primary_key=True)
    tipo_movimento = db.Column(
        db.String(20),
        nullable=False,
        info={'choices': TIPOS_MOVIMENTO}
    )
    marketplace_id = db.Column(
        db.Integer,
        db.ForeignKey('marketplaces.id', ondelete='RESTRICT', onupdate='CASCADE'),
        nullable=False,
        index=True
    )
    transportadora_id = db.Column(
        db.Integer,
        db.ForeignKey('transportadoras.id', ondelete='RESTRICT', onupdate='CASCADE'),
        nullable=False,
        index=True
    )
    funcionario_id = db.Column(
        db.Integer,
        db.ForeignKey('funcionarios.id', ondelete='RESTRICT', onupdate='CASCADE'),
        nullable=False,
        index=True
    )
    quantidade_caixas = db.Column(db.Integer, nullable=False)
    data_envio = db.Column(db.Date, nullable=False, index=True)
    observacoes = db.Column(db.Text, nullable=True)
    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id', ondelete='RESTRICT', onupdate='CASCADE'),
        nullable=False,
        index=True
    )
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

    # Os backrefs são definidos nos outros modelos:
    # - self.marketplace (via Marketplace.encomendas)
    # - self.transportadora (via Transportadora.encomendas)
    # - self.funcionario (via Funcionario.encomendas)
    # - self.usuario (via Usuario.encomendas)

    def __repr__(self):
        return f'<Encomenda {self.id}: {self.tipo_movimento} - {self.data_envio}>'

    @property
    def codigo_formatado(self):
        """Retorna o código formatado com zeros à esquerda (ex: 00123)."""
        return f'{self.id:05d}'

    @property
    def data_envio_formatada(self):
        """Retorna a data de envio formatada em dd/mm/yyyy."""
        if self.data_envio:
            return self.data_envio.strftime('%d/%m/%Y')
        return ''

    @property
    def criado_em_formatado(self):
        """Retorna a data/hora de criação formatada."""
        if self.criado_em:
            return self.criado_em.strftime('%d/%m/%Y %H:%M')
        return ''

    def to_dict(self):
        """Serializa o modelo para dicionário."""
        return {
            'id': self.id,
            'codigo_formatado': self.codigo_formatado,
            'tipo_movimento': self.tipo_movimento,
            'marketplace_id': self.marketplace_id,
            'marketplace_nome': self.marketplace.nome if self.marketplace else None,
            'transportadora_id': self.transportadora_id,
            'transportadora_nome': self.transportadora.nome if self.transportadora else None,
            'funcionario_id': self.funcionario_id,
            'funcionario_nome': self.funcionario.nome if self.funcionario else None,
            'quantidade_caixas': self.quantidade_caixas,
            'data_envio': self.data_envio.isoformat() if self.data_envio else None,
            'data_envio_formatada': self.data_envio_formatada,
            'observacoes': self.observacoes,
            'usuario_id': self.usuario_id,
            'usuario_nome': self.usuario.nome if self.usuario else None,
            'criado_em': self.criado_em.isoformat() if self.criado_em else None,
            'atualizado_em': self.atualizado_em.isoformat() if self.atualizado_em else None,
        }
