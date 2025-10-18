from flask import Blueprint, session, redirect
from blueprints.auth.buisness_logic import login, registr
from blueprints.auth.views import view
from blueprints.basket.busness_logic import flush_redis
from acces import login_required

auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/', methods=['GET', 'POST'])
def index():
    config = login()
    return view("login_form.html", config)

@auth_bp.route('/sign_out/')
@login_required()
def sign_out():
    session.clear()
    flush_redis()
    return redirect('http://127.0.0.1:5000/')

@auth_bp.route('/registration/', methods=['GET', 'POST'])
def registration():
    config = registr()
    return view("registration.html", config)