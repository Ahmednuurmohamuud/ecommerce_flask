# app/staff.py
from flask import Blueprint, current_app,  jsonify, render_template, request, url_for, flash, redirect
from app import ALLOWED_EXTENSIONS, mysql
import os
from werkzeug.utils import secure_filename



#UPLOAD_FOLDER = 'static/images'
#ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

products_bp = Blueprint('products', __name__)

#products_bp.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@products_bp.route('/products')
def index_products():
    cur = mysql.connection.cursor()
    cur.execute("SELECT p.p_id,p.name,p.c_id,p.imageURL,p.description,p.date,c.CategoryID,c.CategoryName FROM products p join categories c on p.c_id = c.CategoryID")
    data = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute("SELECT CategoryID, CategoryName FROM categories")
    cat = cur.fetchall()
    cur.close()

    return render_template('admin/products.html', products=data, cat=cat)



@products_bp.route('/insert', methods=['POST'])
def insert_products():
   if request.method == "POST":
        flash("Product Data Inserted Successfully")
        name = request.form.get('pname')
        c_id = request.form.get('c_id')
        desc = request.form.get('description')
        
        # Handle file upload
        file = request.files.get('img')
        
        if file and file.filename != '' and allowed_file(file.filename):
            # Ensure the upload folder exists
            upload_folder = current_app.config['UPLOAD_FOLDER']
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            
            filename = secure_filename(file.filename)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            img_url = f'{filename}'  # Save relative path to the database
        else:
            img_url = None
       
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO products (name, c_id, imageURL, description) VALUES (%s, %s, %s,%s)", (name, c_id, img_url,desc))
        mysql.connection.commit()
        return redirect(url_for('products.index_products'))

@products_bp.route('/delete/<string:id_data>', methods=['GET'])
def delete_products(id_data):
    flash("Product Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM products WHERE p_id =%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('products.index_products'))

@products_bp.route('/update', methods=['POST'])
def update_products():
    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['pname']
        c_id = request.form['c_id']
        img = request.form.get('img')  # Assuming imgs is from a Flask request form
        if not img:  # Check if imgs is empty or None
          img = request.form.get('h_img')  # Assign 'h_img' if imgs is empty
        else:
         img = img 
        desc = request.form['description']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE products SET name=%s, c_id=%s, imageURL=%s, description=%s
        WHERE p_id=%s
        """, (name, c_id, img,desc,id_data))
        mysql.connection.commit()
        flash("Product Data Updated Successfully")
        return redirect(url_for('products.index_products'))
    




