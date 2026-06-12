from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from app.extensions import db
from app.models.marketplace import Marketplace
from app.forms.cadastros import MarketplaceForm
from app.utils.decorators import admin_required

marketplaces_bp = Blueprint('marketplaces', __name__, url_prefix='/admin/marketplaces')


@marketplaces_bp.route('/')
@login_required
@admin_required
def index():
    marketplaces = Marketplace.query.order_by(Marketplace.nome).all()
    return render_template('marketplaces/index.html', marketplaces=marketplaces)


@marketplaces_bp.route('/novo', methods=['GET', 'POST'])
@login_required
@admin_required
def novo():
    form = MarketplaceForm()
    form.ativo.data = True
    if form.validate_on_submit():
        existente = Marketplace.query.filter_by(nome=form.nome.data.strip()).first()
        if existente:
            flash('Já existe um marketplace com este nome.', 'danger')
            return render_template('marketplaces/form.html', form=form, titulo='Novo Marketplace')

        marketplace = Marketplace(
            nome=form.nome.data.strip(),
            nome_conta=form.nome_conta.data.strip() or None,
            ativo=form.ativo.data,
        )
        db.session.add(marketplace)
        db.session.commit()
        flash(f'Marketplace "{marketplace.nome}" criado com sucesso!', 'success')
        return redirect(url_for('marketplaces.index'))

    return render_template('marketplaces/form.html', form=form, titulo='Novo Marketplace')


@marketplaces_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar(id):
    marketplace = db.get_or_404(Marketplace, id)
    form = MarketplaceForm(obj=marketplace)

    if form.validate_on_submit():
        existente = Marketplace.query.filter(
            Marketplace.nome == form.nome.data.strip(),
            Marketplace.id != id
        ).first()
        if existente:
            flash('Já existe um marketplace com este nome.', 'danger')
            return render_template('marketplaces/form.html', form=form, titulo='Editar Marketplace', item=marketplace)

        marketplace.nome = form.nome.data.strip()
        marketplace.nome_conta = form.nome_conta.data.strip() or None
        marketplace.ativo = form.ativo.data
        db.session.commit()
        flash(f'Marketplace "{marketplace.nome}" atualizado com sucesso!', 'success')
        return redirect(url_for('marketplaces.index'))

    return render_template('marketplaces/form.html', form=form, titulo='Editar Marketplace', item=marketplace)


@marketplaces_bp.route('/<int:id>/toggle-ativo', methods=['POST'])
@login_required
@admin_required
def toggle_ativo(id):
    marketplace = db.get_or_404(Marketplace, id)
    marketplace.ativo = not marketplace.ativo
    db.session.commit()
    estado = 'ativado' if marketplace.ativo else 'desativado'
    flash(f'Marketplace "{marketplace.nome}" {estado} com sucesso!', 'success')
    return redirect(url_for('marketplaces.index'))
