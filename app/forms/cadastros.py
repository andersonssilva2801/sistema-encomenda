from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, DecimalField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, Optional, NumberRange, EqualTo, ValidationError


class UsuarioForm(FlaskForm):
    nome = StringField('Nome Completo', validators=[DataRequired(), Length(max=150)])
    login = StringField('Login', validators=[DataRequired(), Length(max=80)])
    perfil = SelectField('Perfil', choices=[
        ('usuario', 'Usuário'),
        ('administrador', 'Administrador')
    ])
    ativo = BooleanField('Ativo')
    senha = PasswordField('Senha', validators=[Optional(), Length(min=6, message='Mínimo 6 caracteres.')])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[
        EqualTo('senha', message='As senhas não coincidem.')
    ])
    submit = SubmitField('Salvar')


class MarketplaceForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(max=100)])
    nome_conta = StringField('Nome da Conta', validators=[Optional(), Length(max=100)])
    ativo = BooleanField('Ativo')
    submit = SubmitField('Salvar')


class TransportadoraForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(max=100)])
    valor_padrao = DecimalField(
        'Valor Padrão de Frete (R$)',
        places=2,
        validators=[Optional(), NumberRange(min=0, message='O valor não pode ser negativo.')],
        default=0
    )
    ativo = BooleanField('Ativo')
    submit = SubmitField('Salvar')


class FuncionarioForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(max=150)])
    ativo = BooleanField('Ativo')
    submit = SubmitField('Salvar')
