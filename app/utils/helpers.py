"""
Funções auxiliares (helpers) do sistema.

Contém utilitários reutilizáveis em todo o projeto.
"""

from datetime import datetime, date
from dateutil.relativedelta import relativedelta


def get_primeiro_dia_mes():
    """Retorna o primeiro dia do mês atual."""
    hoje = date.today()
    return hoje.replace(day=1)


def get_ultimo_dia_mes():
    """Retorna o último dia do mês atual."""
    hoje = date.today()
    proximo_mes = hoje.replace(day=1) + relativedelta(months=1)
    return proximo_mes - relativedelta(days=1)


def get_periodo_mes_atual():
    """Retorna tupla (primeiro_dia, ultimo_dia) do mês atual."""
    return get_primeiro_dia_mes(), get_ultimo_dia_mes()


def formatar_data_br(valor):
    """Formata uma data para o padrão brasileiro dd/mm/yyyy."""
    if valor is None:
        return ''
    if isinstance(valor, (date, datetime)):
        return valor.strftime('%d/%m/%Y')
    return str(valor)


def formatar_moeda_br(valor):
    """Formata um valor numérico para R$ com separadores brasileiros."""
    if valor is None:
        return 'R$ 0,00'
    try:
        valor = float(valor)
        formatted = f'{valor:,.2f}'
        formatted = formatted.replace(',', 'X').replace('.', ',').replace('X', '.')
        return f'R$ {formatted}'
    except (ValueError, TypeError):
        return 'R$ 0,00'


def parse_data_br(data_str):
    """
    Converte string de data no formato dd/mm/yyyy para objeto date.

    Returns:
        date ou None se a string for inválida.
    """
    if not data_str:
        return None
    try:
        return datetime.strptime(data_str.strip(), '%d/%m/%Y').date()
    except ValueError:
        return None


def parse_data_iso(data_str):
    """
    Converte string de data no formato yyyy-mm-dd para objeto date.

    Returns:
        date ou None se a string for inválida.
    """
    if not data_str:
        return None
    try:
        return datetime.strptime(data_str.strip(), '%Y-%m-%d').date()
    except ValueError:
        return None
