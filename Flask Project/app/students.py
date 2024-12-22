# app/students.py
from flask import Blueprint, render_template, request, url_for, flash, redirect
from app import mysql

student_bp = Blueprint('students', __name__)

@student_bp.route('/students')
def index_students():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', students=data)

@student_bp.route('/insert', methods=['POST'])
def insert_student():
    if request.method == "POST":
        flash("Student Data Inserted Successfully")
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
        mysql.connection.commit()
        return redirect(url_for('students.index_students'))

@student_bp.route('/delete/<string:id_data>', methods=['GET'])
def delete_student(id_data):
    flash("Student Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('students.index_students'))

@student_bp.route('/update', methods=['POST'])
def update_student():
    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE students SET name=%s, email=%s, phone=%s
        WHERE id=%s
        """, (name, email, phone, id_data))
        mysql.connection.commit()
        flash("Student Data Updated Successfully")
        return redirect(url_for('students.index_students'))
