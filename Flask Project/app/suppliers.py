# app/suppliers.py
from flask import Blueprint, jsonify, render_template, request, url_for, flash, redirect
from app import mysql

suppliers_bp = Blueprint('suppliers', __name__)

@suppliers_bp.route('/suppliers')
def index_suppliers():
    cur = mysql.connection.cursor()
    cur.execute("SELECT s.s_id,s.name,s.email,s.phone,s.address FROM suppliers s")
    data = cur.fetchall()
    cur.close()
    return render_template('admin/suppliers.html', suppliers=data)



@suppliers_bp.route('/insert', methods=['POST'])
def insert_suppliers():
    if request.method == "POST":
        flash("supplier Data Inserted Successfully")
        name = request.form['sname']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
      
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO suppliers (name, email, phone, address) VALUES (%s, %s, %s,%s)", (name, email, phone,address))
        mysql.connection.commit()
        return redirect(url_for('suppliers.index_suppliers'))

@suppliers_bp.route('/delete/<string:id_data>', methods=['GET'])
def delete_suppliers(id_data):
    flash("supplier Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM suppliers WHERE s_id =%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('suppliers.index_suppliers'))

@suppliers_bp.route('/update', methods=['POST'])
def update_suppliers():
    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['sname']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE suppliers SET name=%s, email=%s, phone=%s, address=%s
        WHERE s_id=%s
        """, (name, email, phone,address, id_data))
        mysql.connection.commit()
        flash("supplier Data Updated Successfully")
        return redirect(url_for('suppliers.index_suppliers'))
    




