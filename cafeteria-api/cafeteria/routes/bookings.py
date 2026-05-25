from flask import Blueprint, Flask,jsonify,request
#from ..db import get_connection

bookings_bp = Blueprint('bookings_bp', __name__)