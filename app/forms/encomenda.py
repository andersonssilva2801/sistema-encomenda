from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, TextAreaField, SubmitField
from wtforms.fields import DateField
from wtforms.validators import DataRequired, NumberRange, Optional


class EncomendaForm(FlaskForm):
    tipo_movimento = SelectField('Tipo de Movimento', choices=[
        ('Envio', 'Envio'),
        ('Devolução', 'Devolução')
    ], validators=[DataRequired()])
    marketplace_id = SelectField('Marketplace', coerce=int, validators=[DataRequired()])
    transportadora_id = SelectField('Transportadora', coerce=int, validators=[DataRequired()])
    funcionario_id = SelectField('Funcionário', coerce=int, validators=[DataRequired()])
    quantidade_caixas = IntegerField('Quantidade de Caixas', validators=[
        DataRequired(message='Informe a quantidade.'),
        NumberRange(min=1, message='A quantidade deve ser pelo menos 1.')
    ])
    data_envio = DateField('Data de Envio', validators=[DataRequired(message='Informe a data.')])
    observacoes = TextAreaField('Observações', validators=[Optional()])
    submit = SubmitField('Salvar')
