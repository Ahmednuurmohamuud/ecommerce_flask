# app/staff.py
from flask import Blueprint, current_app,session,  jsonify, render_template, request, url_for, flash, redirect
from app import ALLOWED_EXTENSIONS, mysql
import os
from werkzeug.utils import secure_filename





menu_bp = Blueprint('menu', __name__)




@menu_bp.route('/menu')
def index_menu():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT 
            p.p_id, p.name, c.CategoryName, p.imageURL, p.description, s.price, p.date, 
            c.CategoryID
        FROM products p 
        JOIN categories c ON p.c_id = c.CategoryID
        JOIN stock s ON p.p_id = s.p_id
        where s.qty >=1
    """)
    data = cur.fetchall()
    cur.close()

    # cur = mysql.connection.cursor()
    # cur.execute("select * from carts where u_id =%s", (session['user_id'] ,))
           
    # cart = cur.fetchall()
    # cur.close()


    return render_template('user/menu.html', products=data)



