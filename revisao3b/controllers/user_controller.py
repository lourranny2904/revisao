from flask import Flask, render_template, redirect, url_for, request, Blueprint
from .. import app
from ..models.users import User

bp = Blueprint('users', __name__, url_prefix='/users')
@bp.route('/login',  methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('users/login.html')

@bp.route('/register',  methods=['GET', 'POST'])
def register():
    return render_template('users/register.html')

