from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from database.models import Usuario, db

auth_bp = Blueprint('auth', __name__)

# Rota de login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Usuario.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return render_template('index.html') # Redireciona após o login
        else:
            flash('Usuário ou senha incorretos', 'error')
            return redirect(url_for('auth.login'))  # Redireciona para a página de login

    return render_template('login.html')

# Rota para logout
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# Rota para registro de usuário
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password_confirmation = request.form['password_confirmation']

        # Verifique se o e-mail já está registrado
        if Usuario.query.filter_by(email=email).first():
            flash('Este e-mail já está registrado', 'error')
            return redirect(url_for('auth.register'))

        if password != password_confirmation:
            flash('As senhas não coincidem', 'error')
            return redirect(url_for('auth.register'))

        new_user = Usuario(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Usuário registrado com sucesso', 'success')
        return redirect(url_for('auth.login'))
    return render_template('login_or_register.html')

