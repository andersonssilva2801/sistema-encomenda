from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired(message='Informe o login.'), Length(max=80)])
    senha = PasswordField('Senha', validators=[DataRequired(message='Informe a senha.')])
    lembrar = BooleanField('Lembrar-me')
    submit = SubmitField('Entrar')


class TrocarSenhaForm(FlaskForm):
    senha_atual = PasswordField('Senha Atual', validators=[DataRequired(message='Informe a senha atual.')])
    nova_senha = PasswordField('Nova Senha', validators=[
        DataRequired(message='Informe a nova senha.'),
        Length(min=6, message='A senha deve ter pelo menos 6 caracteres.')
    ])
    confirmar_senha = PasswordField('Confirmar Nova Senha', validators=[
        DataRequired(message='Confirme a nova senha.'),
        EqualTo('nova_senha', message='As senhas não coincidem.')
    ])
    submit = SubmitField('Alterar Senha')
