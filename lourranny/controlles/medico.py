# controllers/medico_controller.py
from flask import Blueprint, render_template, request, redirect, url_for
from database.models import db, Medico


medico = Blueprint('medico', __name__)

@medico.route('/cadastrar_medico', methods=['GET', 'POST'])
def cadastrar_medico():
    if request.method == 'POST':
        nome = request.form['nome']
        crm = request.form['crm']
        telefone = request.form['telefone']
        medico = Medico(nome=nome, crm=crm, telefone=telefone)
        db.session.add(medico)
        db.session.commit()
        return render_template('index.html')
    
    return render_template('cadastrar_medico.html')
