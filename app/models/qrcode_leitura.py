from datetime import datetime, timezone
from app.extensions import db


class QrcodeLeitura(db.Model):
    __tablename__ = 'qrcode_leituras'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    codigo_lido = db.Column(db.String(1000), nullable=False)
    data_hora = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    identificado = db.Column(db.Boolean, nullable=False, default=False)
    pedido_id = db.Column(db.BigInteger, nullable=True)

    def __repr__(self):
        return f'<QrcodeLeitura {self.id}: {self.codigo_lido[:40]}>'
