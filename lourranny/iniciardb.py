# create_db.py
from app import app, db
from database.models import Mae, Medico, Bebe, Parto

with app.app_context():
    db.drop_all()  # Cuidado: Isso removerá todas as tabelas existentes
    db.create_all()  # Cria todas as tabelas definidas nos modelos
    print("Tabelas criadas!")