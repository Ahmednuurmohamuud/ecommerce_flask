# app/staff.py
from flask import Blueprint, jsonify, render_template, request, url_for, flash, redirect
from app import mysql

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile')
def index_profile():
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    profile = cur.fetchall()
    cur.close()

    return render_template('user/profile.html',profile=profile)





@profile_bp.route('/update', methods=['POST'])
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
    




