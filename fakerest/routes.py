# criar as rotas
from flask import render_template, url_for, redirect, flash
from flask_login import login_required, login_user, logout_user, current_user
from fakerest import app, database, bcrypt
from fakerest.forms import *
from fakerest.models import *


# colocando no ar com rotas
@app.route('/', methods=["GET", "POST"])  # caminho do link do site.
def homepage():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):
            login_user(usuario)
            return redirect(url_for('perfil', usuario=usuario.username))
    return render_template('homepage.html', form=formlogin)  # -> vai retornar a pagina html dentro do template


@app.route("/criarconta", methods=["GET", "POST"])
def criarconta():
    form_criarconta = FormCriarConta()

    if form_criarconta.validate_on_submit():
        # 🔎 Verificar se o e-mail já existe
        usuario_existente = Usuario.query.filter_by(email=form_criarconta.email.data).first()
        if usuario_existente:
            flash('⚠️ Este e-mail já está cadastrado. Tente outro.', 'warning')
            return redirect(url_for('criarconta'))

        # 🔐 Criptografar senha e criar novo usuário
        senha_hash = bcrypt.generate_password_hash(form_criarconta.senha.data).decode('utf-8')
        novo_usuario = Usuario(
            username=form_criarconta.username.data,
            email=form_criarconta.email.data,
            senha=senha_hash
        )

        # 💾 Salvar no banco
        database.session.add(novo_usuario)
        database.session.commit()

        # 🔓 Fazer login automático
        login_user(novo_usuario, remember=True)

        flash('✅ Conta criada com sucesso! Bem-vindo ao Fakerest.', 'success')
        return redirect(url_for('perfil', usuario=novo_usuario.username))

    return render_template('criarconta.html', form=form_criarconta)


@app.route('/perfil/<usuario>')
@login_required
def perfil(usuario):  # vai exibir a página com os dados do usuario
    return render_template('perfil.html', usuario=usuario)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))
