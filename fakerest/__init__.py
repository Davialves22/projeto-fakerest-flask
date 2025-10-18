from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# criando o app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'

database = SQLAlchemy(app)

from fakerest import routes
