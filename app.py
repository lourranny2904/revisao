from flask import Flask, render_template, url_for, redirect, request, flash
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase, sessionmaker, session
from sqlalchemy import create_engine, ForeignKey
from flask_login import UserMixin, LoginManager, current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lourranny'
engine = create_engine("sqlite:///banco_dados.db") 
Session = sessionmaker(bind=engine)
login_manager = LoginManager() 

@login_manager.user_loader 
def load_user(user_id):
    return Usuarios.find(id=user_id) 

login_manager.init_app(app)

class Base(DeclarativeBase):
    pass

class Exercicios(Base):
    __tablename__ = 'exercicios' 
    id: Mapped[int] = mapped_column(primary_key=True)
    nome_exercicio: Mapped[str]
    descricao: Mapped[str]
    usuario_id: Mapped[int] = mapped_column(ForeignKey('usuarios.id'))

    usuario = relationship("Usuarios", back_populates="exercicios")

class Usuarios(Base, UserMixin):
    __tablename__ = 'usuarios' 
    id: Mapped[int] = mapped_column(primary_key=True)
    matricula: Mapped[int]
    email: Mapped[str]
    senha: Mapped[str]
    
    exercicios = relationship("Exercicios", back_populates="usuario")
    
    @classmethod
    def find(cls, **kwargs):
        session = Session()  # Cria uma nova sessão
        try:
            if 'matricula' in kwargs:
                return session.query(cls).filter_by(matricula=kwargs['matricula']).first()
            elif 'id' in kwargs:
                return session.query(cls).filter_by(id=kwargs['id']).first()
            else:
                raise AttributeError('A busca deve ser feita por matricula ou id.')
        finally:
            session.close()  # Fecha a sessão

with app.app_context():
    Base.metadata.create_all(bind=engine)  # Cria as tabelas do banco

# rota index sem listagem 
#@app.route('/')
#def index():
#    user = current_user
#   #current_user é uma variavel disponibilizada pelo flask_login para recuperar o usuário logado atualmente pelo comando login_user
#    try:
#       return render_template('index.html', matricula=user.matricula )
#    except:
#       return render_template('index.html')

# rora de index para listar e ver detalhes de exercicios

@app.route('/')
def inicio(): 
    return render_template('inicio.html')


# rora de index para listar e ver detalhes de exercicios
@app.route('/index')
@login_required  # Certifique-se de que o usuário está autenticado
def index():
    try:
        exercicios = current_user.exercicios  # Supondo que 'exercicios' é uma relação no seu modelo
        print(f"Exercícios encontrados: {exercicios}")  # Para depuração
        return render_template('index.html', matricula=current_user.matricula, exercicios=exercicios)
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return render_template('index.html', matricula=current_user.matricula, exercicios=[])

    
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        matricula = request.form['matricula']
        email = request.form['email']
        senha = request.form['senha']

        # Validação básica
        if not matricula or not email or not senha:
            flash('Todos os campos são obrigatórios.')
            return redirect(url_for('register'))

        # Hash da senha e email
        senha_hash = generate_password_hash(senha)
        email_hash = generate_password_hash(senha)

        novo_user = Usuarios(matricula=matricula, senha=senha_hash, email=email_hash)

        # Inicializa a sessão
        Session = sessionmaker(bind=engine)  # Usa a engine que você configurou
        session = Session()

        session.add(novo_user)
        session.commit()  # Executa o commit
        login_user(novo_user)  # Loga o usuário
        session.close()  # Fecha a sessão

        return redirect(url_for('login'))

    return render_template('register.html')

    
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        matricula = request.form['matricula']
        senha = request.form['senha']

        session = Session()  # Cria uma nova sessão
        try:
            usuario = session.query(Usuarios).filter(Usuarios.matricula == matricula).first()  # Use matricula

            if not usuario:  # Verifica se o usuário foi encontrado
                print('Matrícula não encontrada')
                flash('Matrícula não encontrada.')
                return redirect(url_for('login'))  # Redireciona para a página de login

            # Verifica a senha usando check_password_hash
            if check_password_hash(usuario.senha, senha):
                print('Login bem-sucedido')
                login_user(usuario)  # Loga o usuário
                return redirect(url_for('index'))  # Redireciona para a página inicial
            else:
                print('Senha incorreta')
                flash('Senha incorreta.')
                return render_template('exercicios.html', matricula=matricula)

        finally:
            session.close()  # Fecha a sessão após a operação

    return render_template('login.html')  # Retorna o formulário de login

@app.route('/exercicios', methods=['POST', 'GET'])
def exercicios():
    session = Session()

    if request.method == 'POST':
        nome_exercicio = request.form['nome_exercicio']
        descricao = request.form['descricao']

        # Adicionar novo exercício
        novo_exercicio = Exercicios(nome_exercicio=nome_exercicio, descricao=descricao, usuario_id=current_user.id)
        session.add(novo_exercicio)
        session.commit()

        return redirect(url_for('exercicios'))  # Redireciona para a mesma rota

    # Buscar todos os exercícios
    todos_exercicios = session.query(Exercicios).all()
    session.close()

    return render_template('exercicios.html', exercicios=todos_exercicios)

@app.route('/mostrar_exercicios', methods=['GET'])
@login_required  # Protege a rota para usuários autenticados
def mostrar_exercicios():
    session = Session()
    
    # Buscar todos os exercícios do usuário atual
    todos_exercicios = session.query(Exercicios).filter_by(usuario_id=current_user.id).all()
    session.close()

    return render_template('mostrar_exercicios.html', exercicios=todos_exercicios)

@app.route('/exercicio/<int:exercicio_id>')
@login_required
def exercicio_detail(exercicio_id):
    session = Session()
    try:
        exercicio = session.query(Exercicios).filter(Exercicios.id == exercicio_id).first()
        if exercicio:
            return render_template('exercicio_detail.html', exercicio=exercicio)
        else:
            flash('Exercício não encontrado.')
            return redirect(url_for('index'))
    finally:
        session.close()

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado com sucesso.')
    return redirect(url_for('login'))