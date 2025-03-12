from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):                      
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)  # O Flask-Login precisa de um método get_id() que retorna o ID do usuário como string



class Mae(db.Model):
    __tablename__ = 'maes'  # Certifique-se de que isso está definido
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    idade = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Mae {self.nome}>'
    
class Bebe(db.Model):
    __tablename__ = 'bebes'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    peso = db.Column(db.Float, nullable=False)
    altura = db.Column(db.Float, nullable=False)

    mae_id = db.Column(db.Integer, db.ForeignKey('maes.id'), nullable=False)  # Referência à tabela 'maes'
    parto_id = db.Column(db.Integer, db.ForeignKey('partos.id'), nullable=False)  # Referência à tabela 'partos'

    mae = db.relationship('Mae', backref='bebes')  # Definindo a relação com Mae

    def __repr__(self):
        return f"<Bebe {self.nome}>"



class Medico(db.Model):
    __tablename__ = 'medicos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    crm = db.Column(db.String(10), unique=True, nullable=False)
    telefone = db.Column(db.String(15), nullable=False)
    
    partos = db.relationship('Parto', backref='medico', lazy=True)

    def __repr__(self):
        return f"<Medico {self.nome}>"


class Parto(db.Model):
    __tablename__ = 'partos'
    id = db.Column(db.Integer, primary_key=True)
    data_parto = db.Column(db.Date, nullable=False)
    
    medico_id = db.Column(db.Integer, db.ForeignKey('medicos.id'), nullable=True)
    bebes = db.relationship('Bebe', backref='parto', lazy=True)  # A relação aqui é correta

    def __repr__(self):
        return f"<Parto {self.data_parto}>"
