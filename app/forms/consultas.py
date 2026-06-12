from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.fields import DateField
from wtforms.validators import Optional


class ConsultaForm(FlaskForm):
    class Meta:
        csrf = False  # Formulário de busca GET não precisa de CSRF

    data_inicio = DateField('Data Início', validators=[Optional()])
    data_fim = DateField('Data Fim', validators=[Optional()])
    marketplace_id = SelectField('Marketplace', coerce=int, validators=[Optional()])
    transportadora_id = SelectField('Transportadora', coerce=int, validators=[Optional()])
    funcionario_id = SelectField('Funcionário', coerce=int, validators=[Optional()])
    tipo_movimento = SelectField('Tipo de Movimento', choices=[
        (0, 'Todos'),
        ('Envio', 'Envio'),
        ('Devolução', 'Devolução')
    ], validators=[Optional()])
    submit = SubmitField('Consultar')
