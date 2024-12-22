# app/service.py
from flask import Blueprint, jsonify, render_template, request, url_for, flash, redirect
from app import mysql

service_bp = Blueprint('service', __name__)

@service_bp.route('/service')
def index_service():
    cur = mysql.connection.cursor()
    cur.execute("SELECT s.ser_id,s.name,s.description,s.price FROM service s")
    data = cur.fetchall()
    cur.close()
    return render_template('admin/service.html', service=data)



@service_bp.route('/insert', methods=['POST'])
def insert_service():
    if request.method == "POST":
        flash("Service Data Inserted Successfully")
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
       
      
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO service (name, description, price) VALUES (%s, %s,%s)", (name, description, price))
        mysql.connection.commit()
        return redirect(url_for('service.index_service'))

@service_bp.route('/delete/<string:id_data>', methods=['GET'])
def delete_service(id_data):
    flash("Service Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM service WHERE ser_id =%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('service.index_service'))

@service_bp.route('/update', methods=['POST'])
def update_service():
    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE service SET name=%s, description=%s, price=%s
        WHERE ser_id=%s
        """, (name, description, price, id_data))
        mysql.connection.commit()
        flash("Service Data Updated Successfully")
        return redirect(url_for('service.index_service'))
    




