from datetime import date
from flask import Blueprint, render_template
from flask_login import login_required
from sqlalchemy import func
from app.extensions import db
from app.models.encomenda import Encomenda
from app.utils.helpers import get_periodo_mes_atual

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/')


@dashboard_bp.route('/')
@login_required
def index():
    hoje = date.today()
    primeiro_dia, ultimo_dia = get_periodo_mes_atual()

    # Total de encomendas registradas hoje
    total_hoje = Encomenda.query.filter(Encomenda.data_envio == hoje).count()

    # Total de caixas enviadas este mês
    total_caixas_mes = db.session.query(
        func.sum(Encomenda.quantidade_caixas)
    ).filter(
        Encomenda.data_envio.between(primeiro_dia, ultimo_dia),
        Encomenda.tipo_movimento == 'Envio'
    ).scalar() or 0

    # Total de devoluções este mês
    total_devolucoes_mes = Encomenda.query.filter(
        Encomenda.data_envio.between(primeiro_dia, ultimo_dia),
        Encomenda.tipo_movimento == 'Devolução'
    ).count()

    # Total de registros este mês
    total_registros_mes = Encomenda.query.filter(
        Encomenda.data_envio.between(primeiro_dia, ultimo_dia)
    ).count()

    # Últimas 5 encomendas registradas
    ultimas_encomendas = Encomenda.query.order_by(
        Encomenda.criado_em.desc()
    ).limit(5).all()

    # Totais por marketplace no mês
    por_marketplace = db.session.query(
        Encomenda.marketplace_id,
        func.sum(Encomenda.quantidade_caixas).label('total_caixas'),
        func.count(Encomenda.id).label('total_registros')
    ).filter(
        Encomenda.data_envio.between(primeiro_dia, ultimo_dia)
    ).group_by(Encomenda.marketplace_id).all()

    return render_template(
        'dashboard/index.html',
        total_hoje=total_hoje,
        total_caixas_mes=total_caixas_mes,
        total_devolucoes_mes=total_devolucoes_mes,
        total_registros_mes=total_registros_mes,
        ultimas_encomendas=ultimas_encomendas,
        por_marketplace=por_marketplace,
        mes_atual=hoje.strftime('%B/%Y'),
    )
