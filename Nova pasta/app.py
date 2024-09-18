from flask import Flask, render_template \
    , url_for, request, redirect

from flask_login import LoginManager \
    , login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from models import User
from flask_mysqldb import MySQL


login_manager = LoginManager()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SUPERMEGADIFICIL'
login_manager.init_app(app)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_banco'
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

conexao = MySQL(app)
def obter_conexao():
    return conexao.connection.cursor()


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['pass']
        
        user = User.get_by_email(email)

        if user and check_password_hash(user.senha, senha):
            
            login_user(user)

            return redirect(url_for('dash'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        senha = generate_password_hash(request.form['pass']) 
        
        # Assuming `conexao` is your database connection object
        conn = conexao.connection.cursor()
        
        # Use %s placeholders for MySQL
        INSERT = 'INSERT INTO usuarios(email, senha) VALUES (%s, %s)'
        
        try:
            conn.execute(INSERT, (email, senha))  # Use `execute` instead of calling conn
            conexao.connection.commit()  # Commit the transaction
        except Exception as e:
            print(f"An error occurred: {e}")  # Print the error for debugging
            conexao.connection.rollback()  # Rollback in case of error
        finally:
            conn.close()  # Ensure the cursor is closed

        return redirect(url_for('dash'))

    return render_template('register.html')


@app.route('/dash')
@login_required
def dash():
    return render_template('dash.html')



@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))


