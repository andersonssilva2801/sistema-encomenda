from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models.usuario import Usuario
from app.forms.auth import LoginForm, TrocarSenhaForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(login=form.login.data.strip()).first()
        if usuario and usuario.ativo and usuario.check_senha(form.senha.data):
            login_user(usuario, remember=form.lembrar.data)
            next_page = request.args.get('next')
            flash(f'Bem-vindo, {usuario.nome}!', 'success')
            return redirect(next_page or url_for('dashboard.index'))
        flash('Login ou senha inválidos.', 'danger')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/trocar-senha', methods=['GET', 'POST'])
@login_required
def trocar_senha():
    form = TrocarSenhaForm()
    if form.validate_on_submit():
        if not current_user.check_senha(form.senha_atual.data):
            flash('Senha atual incorreta.', 'danger')
        else:
            current_user.set_senha(form.nova_senha.data)
            db.session.commit()
            flash('Senha alterada com sucesso!', 'success')
            return redirect(url_for('dashboard.index'))

    return render_template('auth/trocar_senha.html', form=form)
