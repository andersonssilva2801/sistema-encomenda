from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from app.extensions import db
from app.models.transportadora import Transportadora
from app.forms.cadastros import TransportadoraForm
from app.utils.decorators import admin_required

transportadoras_bp = Blueprint('transportadoras', __name__, url_prefix='/admin/transportadoras')


@transportadoras_bp.route('/')
@login_required
@admin_required
def index():
    transportadoras = Transportadora.query.order_by(Transportadora.nome).all()
    return render_template('transportadoras/index.html', transportadoras=transportadoras)


@transportadoras_bp.route('/novo', methods=['GET', 'POST'])
@login_required
@admin_required
def novo():
    form = TransportadoraForm()
    form.ativo.data = True
    if form.validate_on_submit():
        existente = Transportadora.query.filter_by(nome=form.nome.data.strip()).first()
        if existente:
            flash('Já existe uma transportadora com este nome.', 'danger')
            return render_template('transportadoras/form.html', form=form, titulo='Nova Transportadora')

        transportadora = Transportadora(
            nome=form.nome.data.strip(),
            valor_padrao=form.valor_padrao.data or 0,
            ativo=form.ativo.data,
        )
        db.session.add(transportadora)
        db.session.commit()
        flash(f'Transportadora "{transportadora.nome}" criada com sucesso!', 'success')
        return redirect(url_for('transportadoras.index'))

    return render_template('transportadoras/form.html', form=form, titulo='Nova Transportadora')


@transportadoras_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar(id):
    transportadora = db.get_or_404(Transportadora, id)
    form = TransportadoraForm(obj=transportadora)

    if form.validate_on_submit():
        existente = Transportadora.query.filter(
            Transportadora.nome == form.nome.data.strip(),
            Transportadora.id != id
        ).first()
        if existente:
            flash('Já existe uma transportadora com este nome.', 'danger')
            return render_template('transportadoras/form.html', form=form, titulo='Editar Transportadora', item=transportadora)

        transportadora.nome = form.nome.data.strip()
        transportadora.valor_padrao = form.valor_padrao.data or 0
        transportadora.ativo = form.ativo.data
        db.session.commit()
        flash(f'Transportadora "{transportadora.nome}" atualizada com sucesso!', 'success')
        return redirect(url_for('transportadoras.index'))

    return render_template('transportadoras/form.html', form=form, titulo='Editar Transportadora', item=transportadora)


@transportadoras_bp.route('/<int:id>/toggle-ativo', methods=['POST'])
@login_required
@admin_required
def toggle_ativo(id):
    transportadora = db.get_or_404(Transportadora, id)
    transportadora.ativo = not transportadora.ativo
    db.session.commit()
    estado = 'ativada' if transportadora.ativo else 'desativada'
    flash(f'Transportadora "{transportadora.nome}" {estado} com sucesso!', 'success')
    return redirect(url_for('transportadoras.index'))
