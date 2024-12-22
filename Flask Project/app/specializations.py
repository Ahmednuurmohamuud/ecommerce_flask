import MySQLdb
from flask import Blueprint, flash, render_template, session
from app import mysql

spec_bp = Blueprint('specializations', __name__)

# Route to fetch specializations
@spec_bp.route('/')
def logout():
    session.clear()
    flash('You have been logged out.')
    return render_template('user/login.html')
