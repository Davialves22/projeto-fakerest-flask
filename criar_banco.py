from fakerest import database,app
from fakerest.models import Usuario, Foto

with app.app_context():
    database.create_all()