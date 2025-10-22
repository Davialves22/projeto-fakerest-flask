# criar a estrutura do banco de dados
from sqlalchemy.testing.pickleable import User

from fakerest import database, login_manager
from _datetime import datetime
from flask_login import  UserMixin #vai gerenciar o login

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

# criando classes - tabelas
class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(150), nullable=False)
    email = database.Column(database.String(150), nullable=False, unique=True)
    senha = database.Column(database.String(150), nullable=False)
    fotos = database.relationship("Foto", backref="usuario", lazy=True)  # classe relacionavel


class Foto(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    imagem = database.Column(database.String(150), default="default.png")
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())
    id_usuario = database.Column(database.Integer, database.ForeignKey("usuario.id"),
                                 nullable=False)  # classe relacionavel de foto com usuario
