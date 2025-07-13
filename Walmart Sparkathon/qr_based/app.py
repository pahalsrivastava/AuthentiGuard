from flask import Flask, request, jsonify
from product_db import PRODUCTS

app = Flask(__name__)

@app.route('/')
def index():
    return " Product Barcode Validator API is running. "

@app.route('/check-barcode', methods=['POST'])
def check_barcode():
    data = request.get_json()

    if not data or "product_id" not in data:
        return jsonify({
            "found": False,
            "message": "Missing 'product_id' field in request"
        }), 400

    product_id = data["product_id"].strip()

    if product_id in PRODUCTS:
        product = PRODUCTS[product_id]
        return jsonify({
            "found": True,
            "product_id": product_id,
            "name": product["name"],
            "price": product["price"],
            "category": product["category"],
            "authentic": product["authentic"],
            "message": "Product found"
        })
    else:
        return jsonify({
            "found": False,
            "product_id": product_id,
            "message": "Product not found in the database"
        }), 404

if __name__ == '__main__':
    app.run(debug=True)
