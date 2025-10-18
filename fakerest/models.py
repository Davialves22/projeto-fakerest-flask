# criar a estrutura do banco de dados

from fakerest import database
from _datetime import datetime


# criando classes - tabelas
class Usuario(database.Model):
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
