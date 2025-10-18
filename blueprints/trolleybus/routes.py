from flask import Blueprint, current_app, request
from blueprints.trolleybus.buisness_logic import bus_logic
from blueprints.trolleybus.controller import BLogic_data
from blueprints.trolleybus.views import view

trol_bp = Blueprint('trol', __name__, template_folder='templates', static_folder='static')

@trol_bp.route('/timesheet/', methods=['GET', 'POST'])
def timesheet():
    b_logic_args = BLogic_data(request.base_url, request.args)
    result, config = bus_logic(current_app.config['DB_CONFIG'], b_logic_args)
    return view("timesheet.html", result, config)