# app/suppliers.py
from flask import Blueprint, jsonify, request, session
from app import mysql

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'user_id' not in session:
        return jsonify({'message': 'User not logged in'}), 401
    
    user_id = session['user_id']
    cart_items = request.json.get('cartItems', [])
    
    if not cart_items:
        return jsonify({'message': 'No cart items provided'}), 400
    
    cursor = mysql.connection.cursor()
    for item in cart_items:
        product_id = item['id']
        quantity = item['quantity']
        cursor.execute(
            "INSERT INTO carts (u_id, p_id, qty) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE qty = qty + VALUES(qty)",
            (user_id, product_id, quantity)
        )
    mysql.connection.commit()
    cursor.close()
    
    return jsonify({'message': 'Cart items added successfully!'}), 200

@cart_bp.route('/get_cart_items', methods=['GET'])
def get_cart_items():
    if 'user_id' not in session:
        return jsonify({'message': 'User not logged in'}), 401
    
    user_id = session['user_id']
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT c.p_id, p.name, p.imageURL, s.price, c.qty FROM carts c JOIN products p ON c.p_id = p.p_id join stock s on p.p_id = s.p_id WHERE c.u_id = %s",
        (user_id,)
    )
    cart_items = cursor.fetchall()
    cursor.close()
    
    print('Cart items fetched from database:', cart_items)  # Debug print statement
    
    return jsonify(cart_items), 200


@cart_bp.route('/delete_item', methods=['POST'])
def delete_cart_item():
    if 'user_id' not in session:
        return jsonify({'message': 'User not logged in'}), 401
    
    user_id = session['user_id']
    product_id = request.json.get('product_id')
    
    cursor = mysql.connection.cursor()
    cursor.execute(
        "DELETE FROM carts WHERE u_id = %s AND p_id = %s",
        (user_id, product_id)
    )
    mysql.connection.commit()
    cursor.close()
    
    return jsonify({'message': 'Cart item deleted successfully!'}), 200
