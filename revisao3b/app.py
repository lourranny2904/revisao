from flask import Flask
from .controllers import user_controller
from .controllers import tarefa_controller

app = Flask(__name__)
app.register_blueprint(user_controller.bp)

@app.route('/')
def home():
    return "oii!"

if __name__ == '__main__':
    app.run(debug=True)