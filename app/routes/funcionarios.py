from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from app.extensions import db
from app.models.funcionario import Funcionario
from app.forms.cadastros import FuncionarioForm
from app.utils.decorators import admin_required

funcionarios_bp = Blueprint('funcionarios', __name__, url_prefix='/admin/funcionarios')


@funcionarios_bp.route('/')
@login_required
@admin_required
def index():
    funcionarios = Funcionario.query.order_by(Funcionario.nome).all()
    return render_template('funcionarios/index.html', funcionarios=funcionarios)


@funcionarios_bp.route('/novo', methods=['GET', 'POST'])
@login_required
@admin_required
def novo():
    form = FuncionarioForm()
    form.ativo.data = True
    if form.validate_on_submit():
        funcionario = Funcionario(
            nome=form.nome.data.strip(),
            ativo=form.ativo.data,
        )
        db.session.add(funcionario)
        db.session.commit()
        flash(f'Funcionário "{funcionario.nome}" criado com sucesso!', 'success')
        return redirect(url_for('funcionarios.index'))

    return render_template('funcionarios/form.html', form=form, titulo='Novo Funcionário')


@funcionarios_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar(id):
    funcionario = db.get_or_404(Funcionario, id)
    form = FuncionarioForm(obj=funcionario)

    if form.validate_on_submit():
        funcionario.nome = form.nome.data.strip()
        funcionario.ativo = form.ativo.data
        db.session.commit()
        flash(f'Funcionário "{funcionario.nome}" atualizado com sucesso!', 'success')
        return redirect(url_for('funcionarios.index'))

    return render_template('funcionarios/form.html', form=form, titulo='Editar Funcionário', item=funcionario)


@funcionarios_bp.route('/<int:id>/toggle-ativo', methods=['POST'])
@login_required
@admin_required
def toggle_ativo(id):
    funcionario = db.get_or_404(Funcionario, id)
    funcionario.ativo = not funcionario.ativo
    db.session.commit()
    estado = 'ativado' if funcionario.ativo else 'desativado'
    flash(f'Funcionário "{funcionario.nome}" {estado} com sucesso!', 'success')
    return redirect(url_for('funcionarios.index'))
