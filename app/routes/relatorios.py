from datetime import date
from flask import Blueprint, render_template, request
from flask_login import login_required
from sqlalchemy import func
from dateutil.relativedelta import relativedelta
from app.extensions import db
from app.models.encomenda import Encomenda
from app.models.transportadora import Transportadora

relatorios_bp = Blueprint('relatorios', __name__, url_prefix='/relatorios')

PERIODOS = [
    ('mes_atual',      'Mês Atual'),
    ('mes_anterior',   'Mês Anterior'),
    ('ultimos_3_meses','Últimos 3 Meses'),
    ('ultimos_6_meses','Últimos 6 Meses'),
    ('este_ano',       'Este Ano'),
]


def _datas_periodo(periodo):
    hoje = date.today()
    if periodo == 'mes_anterior':
        inicio = (hoje.replace(day=1) - relativedelta(months=1))
        fim    = hoje.replace(day=1) - relativedelta(days=1)
    elif periodo == 'ultimos_3_meses':
        inicio = hoje - relativedelta(months=3)
        fim    = hoje
    elif periodo == 'ultimos_6_meses':
        inicio = hoje - relativedelta(months=6)
        fim    = hoje
    elif periodo == 'este_ano':
        inicio = hoje.replace(month=1, day=1)
        fim    = hoje
    else:  # mes_atual (default)
        inicio = hoje.replace(day=1)
        fim    = (inicio + relativedelta(months=1)) - relativedelta(days=1)
    return inicio, fim


@relatorios_bp.route('/', methods=['GET'])
@login_required
def index():
    periodo = request.args.get('periodo', 'mes_atual')
    if periodo not in dict(PERIODOS):
        periodo = 'mes_atual'
    inicio, fim = _datas_periodo(periodo)

    base = Encomenda.query.filter(Encomenda.data_envio.between(inicio, fim))

    # Totais gerais
    total_encomendas = base.count()
    total_caixas = db.session.query(
        func.coalesce(func.sum(Encomenda.quantidade_caixas), 0)
    ).filter(Encomenda.data_envio.between(inicio, fim)).scalar()

    # Valor total de frete: valor_padrao da transportadora × quantidade_caixas
    valor_total_frete = db.session.query(
        func.coalesce(
            func.sum(Transportadora.valor_padrao * Encomenda.quantidade_caixas), 0
        )
    ).select_from(Encomenda
    ).join(Transportadora, Encomenda.transportadora_id == Transportadora.id
    ).filter(Encomenda.data_envio.between(inicio, fim)).scalar()

    valor_total_frete = float(valor_total_frete or 0)
    media_por_encomenda = valor_total_frete / total_encomendas if total_encomendas else 0

    # Dados gráfico por tipo
    por_tipo = db.session.query(
        Encomenda.tipo_movimento,
        func.count(Encomenda.id).label('total')
    ).filter(
        Encomenda.data_envio.between(inicio, fim)
    ).group_by(Encomenda.tipo_movimento).all()

    tipo_labels = [r.tipo_movimento for r in por_tipo]
    tipo_data   = [r.total for r in por_tipo]

    # Dados gráfico por transportadora (top 5 por qtd caixas)
    por_transp = db.session.query(
        Transportadora.nome,
        func.coalesce(func.sum(Encomenda.quantidade_caixas), 0).label('total_caixas')
    ).select_from(Encomenda
    ).join(Transportadora, Encomenda.transportadora_id == Transportadora.id
    ).filter(
        Encomenda.data_envio.between(inicio, fim)
    ).group_by(Transportadora.nome
    ).order_by(func.sum(Encomenda.quantidade_caixas).desc()
    ).limit(5).all()

    transp_labels = [r.nome for r in por_transp]
    transp_data   = [int(r.total_caixas) for r in por_transp]

    return render_template(
        'relatorios/index.html',
        periodo=periodo,
        periodos=PERIODOS,
        total_encomendas=total_encomendas,
        total_caixas=int(total_caixas),
        valor_total_frete=valor_total_frete,
        media_por_encomenda=media_por_encomenda,
        tipo_labels=tipo_labels,
        tipo_data=tipo_data,
        transp_labels=transp_labels,
        transp_data=transp_data,
        data_inicio=inicio,
        data_fim=fim,
    )
