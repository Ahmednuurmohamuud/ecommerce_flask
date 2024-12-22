# app/staff.py
from flask import Blueprint, jsonify, render_template, request, url_for, flash, redirect
from app import mysql

staff_bp = Blueprint('staff', __name__)

@staff_bp.route('/staff')
def index_staff():
    cur = mysql.connection.cursor()
    cur.execute("SELECT sf.StaffID,sf.FirstName,sf.LastName,sf.Email,sf.Phone,s.SpecializationID,s.Name FROM staff sf join Specialization s on sf.SpecializationID = s.SpecializationID ")
    data = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute("SELECT SpecializationID, Name FROM Specialization")
    spec = cur.fetchall()
    cur.close()

    return render_template('admin/staff.html', staff=data, spec=spec)



@staff_bp.route('/insert', methods=['POST'])
def insert_staff():
    if request.method == "POST":
        flash("Staff Data Inserted Successfully")
        FirstName = request.form['fname']
        LastName = request.form['lname']
        Email = request.form['email']
        Phone = request.form['phone']
        SpecializationID = request.form['spID']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO staff (FirstName, LastName, Email, Phone, SpecializationID) VALUES (%s, %s, %s,%s, %s)", (FirstName, LastName, Email,Phone,SpecializationID))
        mysql.connection.commit()
        return redirect(url_for('staff.index_staff'))

@staff_bp.route('/delete/<string:id_data>', methods=['GET'])
def delete_staff(id_data):
    flash("Staff Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM staff WHERE StaffID =%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('staff.index_staff'))

@staff_bp.route('/update', methods=['POST'])
def update_staff():
    if request.method == 'POST':
        id_data = request.form['id']
        FirstName = request.form['fname']
        LastName = request.form['lname']
        Email = request.form['email']
        Phone = request.form['phone']
        SpecializationID = request.form['spID']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE staff SET FirstName=%s, LastName=%s, Email=%s, Phone=%s, SpecializationID=%s
        WHERE StaffID=%s
        """, (FirstName, LastName, Email,Phone,SpecializationID, id_data))
        mysql.connection.commit()
        flash("Staff Data Updated Successfully")
        return redirect(url_for('staff.index_staff'))
    




