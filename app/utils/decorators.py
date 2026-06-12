"""
Decorators personalizados para controle de acesso.

Contém decorators para proteção de rotas:
- admin_required: restringe acesso a administradores
"""

from functools import wraps
from flask import flash, redirect, url_for, abort
from flask_login import current_user


def admin_required(f):
    """
    Decorator que restringe o acesso a usuários com perfil 'administrador'.

    Uso:
        @app.route('/admin')
        @login_required
        @admin_required
        def admin_page():
            ...

    Nota: Sempre use @login_required ANTES de @admin_required.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Por favor, faça login para acessar esta página.', 'warning')
            return redirect(url_for('auth.login'))
        if not current_user.is_admin:
            flash('Acesso restrito. Você não tem permissão para acessar esta página.', 'danger')
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
