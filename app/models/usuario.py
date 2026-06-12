"""
Model: Usuario
Tabela: usuarios

Armazena os usuários do sistema com controle de perfil de acesso.
Integra com Flask-Login para gerenciamento de sessão.
"""

from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db


class Usuario(UserMixin, db.Model):
    """Modelo de usuário do sistema."""

    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    login = db.Column(db.String(80), nullable=False, unique=True, index=True)
    senha_hash = db.Column(db.String(256), nullable=False)
    perfil = db.Column(
        db.String(20),
        nullable=False,
        default='usuario',
        info={'choices': ['administrador', 'usuario']}
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

    # Relacionamento: encomendas registradas por este usuário
    encomendas = db.relationship(
        'Encomenda',
        backref=db.backref('usuario', lazy='joined'),
        lazy='dynamic',
        foreign_keys='Encomenda.usuario_id'
    )

    def __repr__(self):
        return f'<Usuario {self.id}: {self.login}>'

    def set_senha(self, senha):
        """Gera o hash da senha usando pbkdf2_sha256."""
        self.senha_hash = generate_password_hash(
            senha,
            method='pbkdf2:sha256',
            salt_length=16
        )

    def check_senha(self, senha):
        """Verifica se a senha informada corresponde ao hash armazenado."""
        return check_password_hash(self.senha_hash, senha)

    @property
    def is_admin(self):
        """Retorna True se o usuário tem perfil de administrador."""
        return self.perfil == 'administrador'

    @property
    def is_active(self):
        """Override do Flask-Login: só permite login de usuários ativos."""
        return self.ativo

    def to_dict(self):
        """Serializa o modelo para dicionário (sem senha)."""
        return {
            'id': self.id,
            'nome': self.nome,
            'login': self.login,
            'perfil': self.perfil,
            'ativo': self.ativo,
            'criado_em': self.criado_em.isoformat() if self.criado_em else None,
            'atualizado_em': self.atualizado_em.isoformat() if self.atualizado_em else None,
        }
