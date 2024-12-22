# app/staff.py
from flask import Blueprint, current_app,  jsonify, session,render_template, request, url_for, flash, redirect
from app import  mysql
import os

user_bp = Blueprint('user_reg', __name__)

@user_bp.route('/user_reg')
def index_user():
     if 'user_id' not in session or session['user_id'] is None:
        flash('Please log in to access this page.')
        return redirect(url_for('login.login'))

     return redirect(url_for('profile.index_profile'))
@user_bp.route('/signUp')
def signUp():
    session.clear()
    
    return render_template('user/user_reg.html')

@user_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('login.login'))

@user_bp.route('/insert', methods=['POST'])
def insert_user():
    if request.method == "POST":
        flash("Wellcome Our official Site And Login")
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        username = request.form['uname']
        password = request.form['password']
      
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, phone, address,username,password) VALUES (%s, %s, %s,%s,%s,%s)", (name, email, phone,address,username,password))
        mysql.connection.commit()
        return redirect(url_for('login.index_login'))



