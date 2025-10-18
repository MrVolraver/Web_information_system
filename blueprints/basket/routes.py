from flask import Blueprint, request, current_app, redirect

from blueprints.basket.busness_logic import bus_logic
from blueprints.basket.controller import BLogic_data
from blueprints.basket.views import view
from acces import login_required

basket_bp = Blueprint('basket', __name__, template_folder='Templates', static_folder='static')

@basket_bp.route('/', methods=['GET', 'POST'])
@login_required()
def basket_index():
    b_logic_args = BLogic_data(request.base_url, request.args)
    result, config = bus_logic(current_app.config['DB_CONFIG'], b_logic_args)
    return view("backet.html", result, config)

@basket_bp.route('/clear/')
@login_required()
def clear_basket(): 
    b_logic_args = BLogic_data(request.base_url, request.args)
    bus_logic(current_app.config['DB_CONFIG'], b_logic_args)
    return redirect('/basket')

@basket_bp.route('/buy/', methods=['GET', 'POST'])
@login_required()
def buy(): 
    b_logic_args = BLogic_data(request.base_url, request.args)
    result, config = bus_logic(current_app.config['DB_CONFIG'], b_logic_args)
    return view("buy.html", result, config)