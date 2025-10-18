import json

from flask import Flask, render_template, session, request
from blueprints.trolleybus.routes import trol_bp
from blueprints.auth.routes import auth_bp
from blueprints.profile.routes import profile_bp
from blueprints.report.routes import report_bp
from blueprints.basket.routes import basket_bp

from blueprints.auth.db_login_get import dblogin

app = Flask(__name__)

app.secret_key = 'Gji`kYf[eq<kznm'

app.register_blueprint(trol_bp, url_prefix='/trol')
app.register_blueprint(auth_bp, url_prefix='/login')
app.register_blueprint(profile_bp, url_prefix='/profile')
app.register_blueprint(report_bp, url_prefix='/report')
app.register_blueprint(basket_bp, url_prefix='/basket')

app.config['DB_CONFIG'] = json.load(open('configs/db.json'))
app.config['access_config'] = json.load(open('configs/access_config.json'))
app.config['JSON_AS_ASCII'] = False

@app.route('/', methods=['GET'])
def index():
    user_config = dblogin()
    return render_template('main.html', user_config=user_config)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)