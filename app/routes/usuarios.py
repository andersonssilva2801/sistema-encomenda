from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.extensions import db
from app.models.usuario import Usuario
from app.forms.cadastros import UsuarioForm
from app.utils.decorators import admin_required

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/admin/usuarios')


@usuarios_bp.route('/')
@login_required
@admin_required
def index():
    usuarios = Usuario.query.order_by(Usuario.nome).all()
    return render_template('usuarios/index.html', usuarios=usuarios)


@usuarios_bp.route('/novo', methods=['GET', 'POST'])
@login_required
@admin_required
def novo():
    form = UsuarioForm()
    form.ativo.data = True
    if form.validate_on_submit():
        if not form.senha.data:
            flash('A senha é obrigatória ao criar um usuário.', 'danger')
            return render_template('usuarios/form.html', form=form, titulo='Novo Usuário')

        login_existente = Usuario.query.filter_by(login=form.login.data.strip()).first()
        if login_existente:
            flash('Este login já está em uso.', 'danger')
            return render_template('usuarios/form.html', form=form, titulo='Novo Usuário')

        usuario = Usuario(
            nome=form.nome.data.strip(),
            login=form.login.data.strip(),
            perfil=form.perfil.data,
            ativo=form.ativo.data,
        )
        usuario.set_senha(form.senha.data)
        db.session.add(usuario)
        db.session.commit()
        flash(f'Usuário "{usuario.nome}" criado com sucesso!', 'success')
        return redirect(url_for('usuarios.index'))

    return render_template('usuarios/form.html', form=form, titulo='Novo Usuário')


@usuarios_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar(id):
    usuario = db.get_or_404(Usuario, id)
    form = UsuarioForm(obj=usuario)

    if form.validate_on_submit():
        login_existente = Usuario.query.filter(
            Usuario.login == form.login.data.strip(),
            Usuario.id != id
        ).first()
        if login_existente:
            flash('Este login já está em uso.', 'danger')
            return render_template('usuarios/form.html', form=form, titulo='Editar Usuário', usuario=usuario)

        usuario.nome = form.nome.data.strip()
        usuario.login = form.login.data.strip()
        usuario.perfil = form.perfil.data
        usuario.ativo = form.ativo.data

        if form.senha.data:
            usuario.set_senha(form.senha.data)

        db.session.commit()
        flash(f'Usuário "{usuario.nome}" atualizado com sucesso!', 'success')
        return redirect(url_for('usuarios.index'))

    return render_template('usuarios/form.html', form=form, titulo='Editar Usuário', usuario=usuario)


@usuarios_bp.route('/<int:id>/toggle-ativo', methods=['POST'])
@login_required
@admin_required
def toggle_ativo(id):
    usuario = db.get_or_404(Usuario, id)
    usuario.ativo = not usuario.ativo
    db.session.commit()
    estado = 'ativado' if usuario.ativo else 'desativado'
    flash(f'Usuário "{usuario.nome}" {estado} com sucesso!', 'success')
    return redirect(url_for('usuarios.index'))
