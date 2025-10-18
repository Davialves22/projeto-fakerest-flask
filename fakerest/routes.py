#criar as rotas
from flask import render_template, url_for
from fakerest import app


# colocando no ar com rotas
@app.route('/')  # caminho do link do site.
def homepage():
    return render_template('homepage.html')  # -> vai retornar a pagina html dentro do template


@app.route('/perfil/<usuario>')
def perfl(usuario): #vai exibir a página com os dados do usuario
    return render_template('perfil.html', usuario=usuario)
