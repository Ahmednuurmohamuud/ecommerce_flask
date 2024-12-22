# app/pur_products.py
from datetime import datetime
from flask import Blueprint, json, jsonify, render_template, request, url_for, flash, redirect
from app import mysql

pur_products_bp = Blueprint('pur_products', __name__)

@pur_products_bp.route('/pur_products')
def index_pur_products():
    today = datetime.today().strftime('%Y-%m-%d')
    cur = mysql.connection.cursor()
    cur.execute("SELECT s_id, name FROM suppliers")
    supp = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute("SELECT p_id, name FROM products")
    prod = cur.fetchall()
    cur.close()
    return render_template('admin/pur_products.html', supplier=supp, today=today,products=prod)



@pur_products_bp.route('/insert', methods=['GET', 'POST'])
def insert_pur_products():
    if request.method == "POST":
        flash("pur_products Data Inserted Successfully")

        # Fetch data from form
        purchase_supplier = request.form['purchase_supplier']
        invoice_no = request.form['invoice_no']
        purchase_date = request.form['purchase_date']
        purchase_product = request.form.getlist('purchase_product')
        purchase_quantity = request.form.getlist('quantity')
        purchase_cost = request.form.getlist('purchase_cost')
        sell_price = request.form.getlist('sell_price')
        expire_date = request.form.getlist('expire_date')
        amount = request.form.getlist('amount')
        purchase_total = request.form['purchase_total']
        purchase_discount = request.form['purchase_discount']
        purchase_grand_total = request.form['purchase_grand_total']
        purchase_paid = request.form['purchase_paid']
        purchase_rest = request.form['purchase_rest']

        # Create JSON array of items
        items = []
        for i in range(len(purchase_product)):
            items.append({
                "product_id": purchase_product[i],
                "quantity": purchase_quantity[i],
                "cost": purchase_cost[i],
                "sell_price": sell_price[i],
                "expire_date": expire_date[i],
                "amount": amount[i]
            })
        items_json = json.dumps(items)

        cur = mysql.connection.cursor()
        try:
            # Call the stored procedure with the JSON array of items
            cur.callproc('sp_insert_purchase_items', 
                         (purchase_supplier, invoice_no, purchase_date, items_json, 
                          purchase_total, purchase_discount, purchase_grand_total, 
                          purchase_paid, purchase_rest))
            mysql.connection.commit()
        except Exception as e:
            mysql.connection.rollback()
            flash(f"An error occurred: {str(e)}")
        finally:
            cur.close()
    
    return redirect(url_for('pur_products.index_pur_products'))
