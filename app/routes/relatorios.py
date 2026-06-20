from datetime import date
from flask import Blueprint, render_template, request
from flask_login import login_required
from sqlalchemy import func
from dateutil.relativedelta import relativedelta
from app.extensions import db
from app.models.encomenda import Encomenda
from app.models.marketplace import Marketplace
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

    # Filtro de marketplace
    marketplace_id = request.args.get('marketplace_id', '', type=str)
    marketplace_id = int(marketplace_id) if marketplace_id.isdigit() else None
    marketplaces = Marketplace.query.filter_by(ativo=True).order_by(Marketplace.nome).all()

    # Filtros-base de período (e marketplace quando selecionado)
    filtros_base = [Encomenda.data_envio.between(inicio, fim)]
    if marketplace_id:
        filtros_base.append(Encomenda.marketplace_id == marketplace_id)

    base = Encomenda.query.filter(*filtros_base)

    # Totais gerais
    total_encomendas = base.count()
    total_caixas = db.session.query(
        func.coalesce(func.sum(Encomenda.quantidade_caixas), 0)
    ).filter(*filtros_base).scalar()

    # Valor total de frete: valor_padrao da transportadora × quantidade_caixas
    valor_total_frete = db.session.query(
        func.coalesce(
            func.sum(Transportadora.valor_padrao * Encomenda.quantidade_caixas), 0
        )
    ).select_from(Encomenda
    ).join(Transportadora, Encomenda.transportadora_id == Transportadora.id
    ).filter(*filtros_base).scalar()

    valor_total_frete = float(valor_total_frete or 0)
    media_por_encomenda = valor_total_frete / total_encomendas if total_encomendas else 0

    # Dados gráfico por tipo
    por_tipo = db.session.query(
        Encomenda.tipo_movimento,
        func.count(Encomenda.id).label('total')
    ).filter(
        *filtros_base
    ).group_by(Encomenda.tipo_movimento).all()

    tipo_labels = [r.tipo_movimento for r in por_tipo]
    tipo_data   = [r.total for r in por_tipo]

    # Cards por tipo: caixas + valor frete
    por_tipo_stats = db.session.query(
        Encomenda.tipo_movimento,
        func.coalesce(func.sum(Encomenda.quantidade_caixas), 0).label('total_caixas'),
        func.coalesce(func.sum(Transportadora.valor_padrao * Encomenda.quantidade_caixas), 0).label('valor_frete')
    ).select_from(Encomenda
    ).join(Transportadora, Encomenda.transportadora_id == Transportadora.id
    ).filter(*filtros_base
    ).group_by(Encomenda.tipo_movimento).all()

    stats_por_tipo = {r.tipo_movimento: {'caixas': int(r.total_caixas), 'valor': float(r.valor_frete)}
                      for r in por_tipo_stats}
    envio_stats    = stats_por_tipo.get('Envio',     {'caixas': 0, 'valor': 0.0})
    devolucao_stats = stats_por_tipo.get('Devolução', {'caixas': 0, 'valor': 0.0})
    saldo_valor    = envio_stats['valor'] - devolucao_stats['valor']
    saldo_caixas   = envio_stats['caixas'] - devolucao_stats['caixas']

    # Dados gráfico por transportadora (top 5 por qtd caixas)
    por_transp = db.session.query(
        Transportadora.nome,
        func.coalesce(func.sum(Encomenda.quantidade_caixas), 0).label('total_caixas')
    ).select_from(Encomenda
    ).join(Transportadora, Encomenda.transportadora_id == Transportadora.id
    ).filter(
        *filtros_base
    ).group_by(Transportadora.nome
    ).order_by(func.sum(Encomenda.quantidade_caixas).desc()
    ).limit(5).all()

    transp_labels = [r.nome for r in por_transp]
    transp_data   = [int(r.total_caixas) for r in por_transp]

    return render_template(
        'relatorios/index.html',
        periodo=periodo,
        periodos=PERIODOS,
        marketplace_id=marketplace_id,
        marketplaces=marketplaces,
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
        envio_stats=envio_stats,
        devolucao_stats=devolucao_stats,
        saldo_valor=saldo_valor,
        saldo_caixas=saldo_caixas,
    )
