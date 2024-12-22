from flask import Flask, render_template
from flask_mysqldb import MySQL
#app = Flask(__name__, static_url_path='/static')

UPLOAD_FOLDER = 'app/static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'many random bytes'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'yes'
app.config['MYSQL_DB'] = 'cosmaticsdb'

mysql = MySQL(app)

from app.products import products_bp
from app.categories import category_bp
from app.staff import staff_bp
from app.suppliers import suppliers_bp
from app.pur_products import pur_products_bp
from app.menu import menu_bp
from app.user_reg import user_bp
from app.login import login_bp
from app.profile import profile_bp
from app.cart import cart_bp
from app.service import service_bp
from app.appointment import appointment_bp
from app.payment import payment_bp


app.register_blueprint(products_bp, url_prefix='/products')
app.register_blueprint(category_bp, url_prefix='/categories')
app.register_blueprint(staff_bp, url_prefix='/staff')
app.register_blueprint(suppliers_bp, url_prefix='/suppliers')
app.register_blueprint(pur_products_bp, url_prefix='/pur_products')
app.register_blueprint(menu_bp,url_prefix='/menu')
app.register_blueprint(user_bp,url_prefix='/user_reg')
app.register_blueprint(login_bp,url_prefix='/login')
app.register_blueprint(profile_bp,url_prefix='/profile')
app.register_blueprint(cart_bp,url_prefix='/cart')
app.register_blueprint(service_bp,url_prefix='/service')
app.register_blueprint(appointment_bp,url_prefix='/appointment')
app.register_blueprint(payment_bp,url_prefix='/payment')


@app.route('/')
def index():
    return render_template('admin/base.html')
