import json
from flask import Blueprint, request, current_app
from acces import login_required
from blueprints.profile.buisness_logic import bus_logic
from blueprints.profile.controller import BLogic_data
from blueprints.profile.views import view

profile_bp = Blueprint('profile', __name__, template_folder='templates')

@profile_bp.route('/', methods=['GET'])
@login_required()
def index():
    return view("profile.html", 0, 0)

@profile_bp.route('/timesheet/', methods=['GET'])
@login_required()
def my_timesheet():
    b_logic_args = BLogic_data(request.base_url, request.args)
    result = bus_logic(current_app.config['DB_CONFIG'], b_logic_args)
    return view("timesheetdriver.html", result, 0)

@profile_bp.route('/add_timesheet/', methods=['GET', 'POST'])
@login_required()
def add_timesheet():
    b_logic_args = BLogic_data(request.base_url, request.args)
    config = bus_logic(current_app.config['DB_CONFIG'], b_logic_args)
    return view("add_timesheet.html", 0, config)

@profile_bp.route('/my_routes/', methods=['GET'])
@login_required()
def my_routes():
    b_logic_args = BLogic_data(request.base_url, request.args)
    result = bus_logic(current_app.config['DB_CONFIG'], b_logic_args)
    return view("my_routes.html", result, 0)

@profile_bp.route('/my_drivers/', methods=['GET'])
@login_required()
def my_drivers():
    b_logic_args = BLogic_data(request.base_url, request.args)
    result = bus_logic(current_app.config['DB_CONFIG'], b_logic_args)
    return view("my_drivers.html", result, 0)

@profile_bp.route('/history_routes/', methods=['GET', 'POST'])
@login_required()
def history_routes():
    b_logic_args = BLogic_data(request.base_url, request.args)
    result = bus_logic(current_app.config['DB_CONFIG'], b_logic_args)
    return view("history_routes.html", result, 0)