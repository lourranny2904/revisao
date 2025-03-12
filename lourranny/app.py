from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, current_user
from database.models import db, Usuario
from config import DevelopmentConfig
from config import Config
from controlles.mae import mae
from controlles.medico import medico
from auth.auth_bp import auth_bp
from controlles.nascimento import nascimento

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Inicializa o SQLAlchemy com a aplicação Flask
db.init_app(app)

app.config.from_object(Config)  # Carrega as configurações do config.py

# Inicializa o LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

# Define a URL de redirecionamento para o login
login_manager.login_view = "auth.login"  # Define qual rota será usada para login, caso o usuário não esteja autenticado.

# Função que carrega o usuário pelo ID
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Registrando os Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(mae)
app.register_blueprint(medico)
app.register_blueprint(nascimento)

@app.route('/')
def index():
    # Se o usuário já estiver logado, redireciona para a página principal
    if current_user.is_authenticated:
        return redirect(url_for('medico.cadastrar_medico'))  # Ou a página que você quer mostrar após o login
    return render_template('login_or_register.html')

if __name__ == '__main__':
    app.run(debug=True)
