# app/staff.py
import datetime
from flask import Blueprint, current_app,  jsonify, session,render_template, request, url_for, flash, redirect
from app import  mysql
import os

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/paymentsd')
def index_payy():
     if 'user_id' not in session or session['user_id'] is None:
        
        return redirect(url_for('login.login'))

     return render_template('user/payment.html')


@payment_bp.route('/save_cart', methods=['POST'])
def save_cart():
    try:
        if 'user_id' not in session or session['user_id'] is None:
            return jsonify(success=False, message='User not logged in'), 403

        data = request.get_json()
        if not data:
            return jsonify(success=False, message='Invalid data'), 400

        cart_items = data.get('cartItems')
        total = data.get('total')
        discount = data.get('discount')
        grand_total = data.get('grandTotal')

        # Fetch the current last invoice number
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT last_invoice_number FROM invoice_counter ORDER BY id DESC LIMIT 1")
        last_invoice_number = cursor.fetchone()[0]

        # Increment the invoice number
        new_invoice_number = last_invoice_number + 1
        invoice = f"INV-{new_invoice_number}"

        # Update the invoice number in the database
        cursor.execute("UPDATE invoice_counter SET last_invoice_number = %s ORDER BY id DESC LIMIT 1", (new_invoice_number,))
        mysql.connection.commit()

        session['cart_items'] = cart_items
        session['total'] = total
        session['discount'] = discount
        session['grand_total'] = grand_total
        session['invoice'] = invoice

        return jsonify(success=True)

    except Exception as e:
        current_app.logger.error(f"Error in save_cart: {e}")
        return jsonify(success=False, message='Internal server error'), 500


@payment_bp.route('/payments', methods=['GET', 'POST'])
def index_pay():
    if 'user_id' not in session or session['user_id'] is None:
        return redirect(url_for('login.login'))

    if request.method == 'POST':
        phone = request.form['phone']
        user_id = session['user_id']
        cart_items = session.get('cart_items', [])
        total = session.get('total', 0)
        discount = session.get('discount', 0)
        grand_total = session.get('grand_total', 0)
        invoice = session.get('invoice')

        try:
            cursor = mysql.connection.cursor()

            # Insert into orders_invoice table
            cursor.execute("""
                INSERT INTO orders_invoice (u_id, invoice, total, discount, g_total, status, phone, date)
                VALUES (%s, %s, %s, %s, %s, 'pending', %s, %s)
            """, (user_id, invoice, total, discount, grand_total, phone, datetime.datetime.now()))

            # Insert into orders_tbl table
            for item in cart_items:
                cursor.execute("""
                    INSERT INTO orders_tbl (u_id, invoice, p_id, qty, price, amount, date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (user_id, invoice, item['p_id'], item['qty'], item['price'], item['amount'], datetime.datetime.now()))
                cursor.execute("UPDATE stock SET qty = qty - %s where p_id = %s", (item['qty'],item['p_id']))

            cursor.execute("DELETE FROM carts WHERE u_id = %s", (user_id,))
            mysql.connection.commit()

            return redirect(url_for('payment.view_invoice', invoice_id=invoice))

        except Exception as e:
            current_app.logger.error(f"Error in index_pay: {e}")
            return render_template('user/payment.html', error='Internal server error')

    return render_template('user/payment.html')




@payment_bp.route('/invoice/<invoice_id>')
def view_invoice(invoice_id):
    if 'user_id' not in session or session['user_id'] is None:
        return redirect(url_for('login.login'))

    user_id = session['user_id']
    try:
        cursor = mysql.connection.cursor()

        # Fetch invoice details
        cursor.execute("""
            SELECT invoice, total, discount, g_total, status, phone, date 
            FROM orders_invoice 
            WHERE u_id = %s AND invoice = %s
        """, (user_id, invoice_id))
        invoice_data = cursor.fetchone()

        if not invoice_data:
            return "Invoice not found", 404

        # Fetch ordered items
        cursor.execute("""
            SELECT p_id, qty, price, amount 
            FROM orders_tbl 
            WHERE u_id = %s AND invoice = %s
        """, (user_id, invoice_id))
        order_items = cursor.fetchall()

        return render_template('user/invoice.html', invoice=invoice_data, items=order_items)

    except Exception as e:
        current_app.logger.error(f"Error in view_invoice: {e}")
        return "Internal server error", 500
