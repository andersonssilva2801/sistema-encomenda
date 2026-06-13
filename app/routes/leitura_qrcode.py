from datetime import datetime, timezone
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from app.extensions import db, csrf
from app.models.qrcode_leitura import QrcodeLeitura

leitura_qrcode_bp = Blueprint('leitura_qrcode', __name__, url_prefix='/leitura-qrcode')

HISTORICO_POR_PAGINA = 50


@leitura_qrcode_bp.route('/', methods=['GET'])
@login_required
def index():
    pagina = request.args.get('pagina', 1, type=int)
    historico = (
        QrcodeLeitura.query
        .order_by(QrcodeLeitura.data_hora.desc())
        .paginate(page=pagina, per_page=HISTORICO_POR_PAGINA, error_out=False)
    )
    return render_template('leitura_qrcode/index.html', historico=historico)


@csrf.exempt
@leitura_qrcode_bp.route('/excluir/<int:id>', methods=['POST'])
@login_required
def excluir(id):
    leitura = db.session.get(QrcodeLeitura, id)
    if not leitura:
        return jsonify({'ok': False, 'erro': 'Não encontrado'}), 404
    db.session.delete(leitura)
    db.session.commit()
    return jsonify({'ok': True})


@csrf.exempt
@leitura_qrcode_bp.route('/salvar', methods=['POST'])
@login_required
def salvar():
    data = request.get_json(silent=True) or {}
    codigo = (data.get('codigo') or '').strip()
    if not codigo:
        return jsonify({'ok': False, 'erro': 'Código vazio'}), 400

    leitura = QrcodeLeitura(
        codigo_lido=codigo[:1000],
        data_hora=datetime.now(timezone.utc),
        identificado=False,
        pedido_id=None,
    )
    db.session.add(leitura)
    db.session.commit()

    return jsonify({
        'ok': True,
        'id': leitura.id,
        'codigo_lido': leitura.codigo_lido,
        'data_hora': leitura.data_hora.strftime('%d/%m/%Y %H:%M:%S'),
    })
