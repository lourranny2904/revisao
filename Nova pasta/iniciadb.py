from flask import Flask
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mysql'
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

conexao = MySQL(app)

def banco(bdados):
    with app.app_context():
        cursor = conexao.connection.cursor()
        with open(bdados, 'r') as file:
            sql = file.read()
            comandos_raw = sql.split(';') #Divide o conteúdo do arquivo em uma lista usando ';' como delimitador

            commands = [] #Lista para armazenar comandos SQL limpos
            for comando in comandos_raw:
                comando_limpo = comando.strip() #Remover espaços em branco no início e no fim do comando
                if comando_limpo:#Verificar se o comando não está vazio
                    commands.append(comando_limpo)#Adicionar o comando limpo à lista 'commands'

            for command in commands: #percorrendo os comandos limpos
                cursor.execute(command) #executando cada comando
        conexao.connection.commit()
        cursor.close()

if __name__ == "__main__":
    banco('mysql.sql')  # Caminho ajustado para o arquivo SQL
    print("Banco de dados e tabelas inicializados com sucesso!")
   