from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file
from flask_login import login_required, current_user
from app.extensions import db
from app.models.encomenda import Encomenda
from app.models.marketplace import Marketplace
from app.models.transportadora import Transportadora
from app.models.funcionario import Funcionario
from app.forms.encomenda import EncomendaForm

encomendas_bp = Blueprint('encomendas', __name__, url_prefix='/encomendas')


def _popular_choices(form):
    """Popula os SelectFields do formulário com dados ativos do banco."""
    form.marketplace_id.choices = [
        (m.id, m.nome) for m in Marketplace.query.filter_by(ativo=True).order_by(Marketplace.nome).all()
    ]
    form.transportadora_id.choices = [
        (t.id, t.nome) for t in Transportadora.query.filter_by(ativo=True).order_by(Transportadora.nome).all()
    ]
    form.funcionario_id.choices = [
        (f.id, f.nome) for f in Funcionario.query.filter_by(ativo=True).order_by(Funcionario.nome).all()
    ]


@encomendas_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 20

    query = Encomenda.query.order_by(Encomenda.data_envio.desc(), Encomenda.criado_em.desc())
    paginacao = query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('encomendas/index.html', paginacao=paginacao)


@encomendas_bp.route('/nova', methods=['GET', 'POST'])
@login_required
def nova():
    form = EncomendaForm()
    _popular_choices(form)

    if form.validate_on_submit():
        encomenda = Encomenda(
            tipo_movimento=form.tipo_movimento.data,
            marketplace_id=form.marketplace_id.data,
            transportadora_id=form.transportadora_id.data,
            funcionario_id=form.funcionario_id.data,
            quantidade_caixas=form.quantidade_caixas.data,
            data_envio=form.data_envio.data,
            observacoes=form.observacoes.data or None,
            usuario_id=current_user.id,
        )
        db.session.add(encomenda)
        db.session.commit()
        flash(f'Encomenda #{encomenda.codigo_formatado} registrada com sucesso!', 'success')
        return redirect(url_for('encomendas.detalhe', id=encomenda.id))

    return render_template('encomendas/form.html', form=form, titulo='Nova Encomenda')


@encomendas_bp.route('/<int:id>')
@login_required
def detalhe(id):
    encomenda = db.get_or_404(Encomenda, id)
    return render_template('encomendas/detalhe.html', encomenda=encomenda)


@encomendas_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    encomenda = db.get_or_404(Encomenda, id)
    form = EncomendaForm(obj=encomenda)
    _popular_choices(form)

    if form.validate_on_submit():
        encomenda.tipo_movimento = form.tipo_movimento.data
        encomenda.marketplace_id = form.marketplace_id.data
        encomenda.transportadora_id = form.transportadora_id.data
        encomenda.funcionario_id = form.funcionario_id.data
        encomenda.quantidade_caixas = form.quantidade_caixas.data
        encomenda.data_envio = form.data_envio.data
        encomenda.observacoes = form.observacoes.data or None
        db.session.commit()
        flash(f'Encomenda #{encomenda.codigo_formatado} atualizada com sucesso!', 'success')
        return redirect(url_for('encomendas.detalhe', id=encomenda.id))

    return render_template('encomendas/form.html', form=form, titulo='Editar Encomenda', encomenda=encomenda)


@encomendas_bp.route('/<int:id>/excluir', methods=['POST'])
@login_required
def excluir(id):
    encomenda = db.get_or_404(Encomenda, id)
    codigo = encomenda.codigo_formatado
    db.session.delete(encomenda)
    db.session.commit()
    flash(f'Encomenda #{codigo} excluída com sucesso!', 'success')
    return redirect(url_for('encomendas.index'))
