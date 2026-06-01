from flask import Blueprint, Flask, render_template, request, jsonify

reviews_bp = Blueprint('reviews_bp', __name__)

@reviews_bp.route('/resenas', methods=['GET'] )
def reviews():
    return render_template('reviews.html')# no existe aun