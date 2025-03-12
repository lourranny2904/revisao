# controllers/nascimento_controller.py
from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime
from sqlalchemy.orm import joinedload
from database.models import db, Mae, Medico, Bebe, Parto


nascimento= Blueprint('nascimento', __name__)

@nascimento.route('/cadastrar_nascimento', methods=['GET', 'POST'])
def cadastrar_nascimento():
    if request.method == 'POST':
        nome_bebe = request.form['nome']
        data_nascimento_str = request.form['data_nascimento']
        peso = float(request.form['peso'])
        altura = float(request.form['altura'])
        mae_id = request.form['mae_id']
        data_parto_str = request.form['data_parto']
        medico_ids = request.form.getlist('medico_ids')

        try:
            data_nascimento = datetime.strptime(data_nascimento_str, '%Y-%m-%d').date()
            data_parto = datetime.strptime(data_parto_str, '%Y-%m-%d').date()
        except ValueError:
            return "Formato de data inválido. Use YYYY-MM-DD.", 400

        try:
            mae = Mae.query.get(mae_id)
            if not mae:
                return "Mãe não encontrada", 404
            
            parto = Parto(data_parto=data_parto)
            db.session.add(parto)
            db.session.commit()

            bebe = Bebe(
                nome=nome_bebe,
                data_nascimento=data_nascimento,
                peso=peso,
                altura=altura,
                mae_id=mae.id,
                parto_id=parto.id
            )
            db.session.add(bebe)
            db.session.commit()

            # Redirecionar para a página inicial após o cadastro
            return redirect(url_for('index'))  # Usar 'index' sem o prefixo 'app.'

        except Exception as e:
            db.session.rollback()
            return f"Ocorreu um erro: {e}", 500

    maes = Mae.query.all()
    medicos = Medico.query.all()

    return render_template('cadastrar_nascimento.html', maes=maes, medicos=medicos)


@nascimento.route('/listar_nascimentos')
def listar_nascimentos():
    # Buscar todos os nascimentos e carregar as relações com a Mae e Medico
    nascimentos = Bebe.query.options(
        joinedload(Bebe.mae),      # Carrega a relação com Mae
        joinedload(Bebe.parto).joinedload(Parto.medico)  # Carrega a relação com Medico através de Parto
    ).all()

    return render_template('listar_nascimentos.html', nascimentos=nascimentos)


