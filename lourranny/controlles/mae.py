# controllers/mae_controller.py
from flask import Blueprint, render_template, request, redirect, url_for
from database.models import db, Mae
from flask_login import login_user, login_required, logout_user


mae = Blueprint('mae', __name__)

@mae.route('/cadastrar_mae', methods=['POST', 'GET'])
@login_required
def cadastrar_mae():
    if request.method == 'POST':
        nome = request.form.get('nome')
        telefone = request.form.get('telefone')
        idade = request.form.get('idade')

        if nome is None or telefone is None or idade is None:
            return "Dados incompletos", 400

        mae = Mae(nome=nome, telefone=telefone, idade=idade)
        db.session.add(mae)
        db.session.commit()

        return render_template('index.html')

    return render_template('cadastrar_mae.html')

