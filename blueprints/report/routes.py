from flask import Blueprint, current_app, request
from blueprints.report.views import view
from blueprints.report.controller import BLogic_data
from blueprints.report.buisness_logic import bus_logic_create, bus_logic_read
from acces import login_required

report_bp = Blueprint('report', __name__, template_folder='Templates', static_folder='static')

@report_bp.route('/')
@login_required()
def index():
    return view("report.html", 0, 0)

@report_bp.route('/create_report/', methods=['GET'])
@login_required()
def create_report():
    return view("report.html", 0, 0)

@report_bp.route('/create_report/about_drivers/', methods=['GET', 'POST'])
@login_required()
def about_drivers():
    b_logic_args = BLogic_data(request.base_url, request.args)
    config = bus_logic_create(current_app.config['DB_CONFIG'], b_logic_args)
    return view("report_drivers.html", 0, config)

@report_bp.route('/create_report/about_date/', methods=['GET', 'POST'])
@login_required()
def about_date():
    b_logic_args = BLogic_data(request.base_url, request.args)
    config = bus_logic_create(current_app.config['DB_CONFIG'], b_logic_args)
    return view("report_date.html", 0, config)

@report_bp.route('/read_report/', methods=['GET'])
@login_required()
def read_report():
    b_logic_args = BLogic_data(request.base_url, request.args)
    result = bus_logic_read(current_app.config['DB_CONFIG'], b_logic_args)
    return view("read_report.html", result, 0)