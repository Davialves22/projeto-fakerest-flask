# criar as rotas
from flask import render_template, url_for, redirect, flash, request
from flask_login import login_required, login_user, logout_user, current_user
from fakerest import app, database, bcrypt
from fakerest.forms import *
from fakerest.models import *
import os
from werkzeug.utils import secure_filename


# colocando no ar com rotas
@app.route('/', methods=["GET", "POST"])  # caminho do link do site.
def homepage():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):
            login_user(usuario)
            return redirect(url_for('perfil', id_usuario=usuario.id))
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
        return redirect(url_for('perfil', id_usuario=novo_usuario.id))

    return render_template('criarconta.html', form=form_criarconta)


@app.route('/perfil/<id_usuario>', methods=["GET", "POST"])
@login_required
def perfil(id_usuario):  # vai exibir a página com os dados do usuario
    if int(id_usuario) == int(current_user.id):  # o usuario ta vendo o proprio perfil senao ta vendo o de outro usuario
        form_foto = FormFoto()
        if form_foto.validate_on_submit():
            arquivo = form_foto.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            # salvar o arquivo na pasta
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),  # o caminho onde esta o codigo escrito
                                   app.config['UPLOAD_FOLDER'], nome_seguro)
            arquivo.save(caminho)

            # registrar o arquivo no banco
            foto = Foto(imagem=nome_seguro, id_usuario=current_user.id)
            database.session.add(foto)  # adiciona a foto
            database.session.commit()  # registra no banco

        return render_template('perfil.html', usuario=current_user, form=form_foto)
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template('perfil.html', usuario=usuario, form=None)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@app.route("/feed")
@login_required
def feed():
    # Pega a página da query string, padrão é 1
    page = request.args.get('page', 1, type=int)
    per_page = 10  # quantidade de fotos por página

    # Retorna um objeto Pagination
    fotos_pag = Foto.query.order_by(Foto.data_criacao.desc()).paginate(page=page, per_page=per_page)

    return render_template('feed.html', fotos=fotos_pag)
