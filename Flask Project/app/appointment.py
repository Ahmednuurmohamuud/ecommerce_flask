# app/staff.py
from flask import Blueprint, current_app, session, jsonify, render_template, request, url_for, flash, redirect
from app import  mysql
import os





appointment_bp = Blueprint('appointment', __name__)

#products_bp.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@appointment_bp.route('/appointment')
def index_app():
    

    cur = mysql.connection.cursor()
    cur.execute("SELECT ser_id, name,price FROM service")
    ser = cur.fetchall()
    cur.close()

    return render_template('user/appointment.html', ser=ser)


@appointment_bp.route('/insert', methods=['POST'])
def insert_app():
    if request.method == "POST":
        
        name = request.form['name']
        date = request.form['date']
        time = request.form['time']
        userid = session['user_id']
        
      
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO appointments (u_id, ser_id, app_date, app_time) VALUES (%s, %s, %s,%s)", (name,userid, date, time))
        mysql.connection.commit()
        flash("Appointment Request is Sent")
        return redirect(url_for('appointment.index_app'))





       




