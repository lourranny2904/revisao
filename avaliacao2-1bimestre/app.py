from flask import Flask, request, make_response,url_for , render_template, redirect, session

app = Flask(__name__)
app.secret_key = 'lourranny'

usuarios = []
mensagens_usu = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        
        # Verificar se o usuário já existe
        for usuario in usuarios:
            if usuario['nome'] == nome:
                session['nome'] = nome  # Armazenar o nome do usuário na sessão
                res = make_response(redirect(url_for('mensagens')))  
                res.set_cookie('nome', nome, max_age=60*60*24)  # Definir cookie por 1 dia
                return res

        # Se o usuário não existe, adiciona um novo usuário
        usuarios.append({'nome': nome})
        session['nome'] = nome  # Armazenar na sessão depois de adicionar
        return redirect(url_for('mensagens'))  # Redirecionar para a página de mensagens

    # Se o usuário já estiver na sessão, redireciona para mensagens
    if 'nome' in session:
        return redirect(url_for('mensagens'))

    return render_template('login.html')  # Renderizar a página de login

@app.route('/mensagens', methods=['GET', 'POST'])
def mensagens():
    # Inicializa a variável antes de usá-la
    usuario_nome = session.get('nome')

    if request.method == 'POST':
        mensagens = request.form['mensagens']

        # Verifica se o usuário está logado
        if usuario_nome:
            mensagens_usu.append({'usuario': usuario_nome, 'texto': mensagens})
            return redirect(url_for('mensagens'))

    # Filtra mensagens do usuário logado
    mensagens_do_usuario = [msg for msg in mensagens_usu if msg['usuario'] == usuario_nome]

    return render_template('mensagens.html', mensagens=mensagens_do_usuario)

@app.route('/mensagens/<usuario>', methods=['GET'])
def mensagens_por_usuario(usuario):
    # Filtra mensagens para o usuário especificado na URL
    mensagens_do_usuario = [msg for msg in mensagens_usu if msg['usuario'] == usuario]
    return render_template('mensagens.html', mensagens=mensagens_do_usuario)

@app.route('/logout')
def logout():
    session.pop('nome', None)  # Remove o nome da sessão
    return redirect(url_for('login'))  # Redireciona para a página de login

