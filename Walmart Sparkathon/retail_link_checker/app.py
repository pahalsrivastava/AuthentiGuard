//flask backend
from flask import Flask, request, jsonify
from validators import validate_retail_url
app = Flask(__name__)
@app.route('/')
def index():
    return "Retail Link Verifier is running!"


@app.route('/check-link', methods=['POST'])
def check_link():
    data = request.get_json()
    
    if not data or "url" not in data:
        return jsonify({"valid": False, "reason": "Missing 'url' field in request"}), 400

    url = data["url"].strip()
    is_valid, reason = validate_retail_url(url)

    return jsonify({
        "url": url,
        "valid": is_valid,
        "reason": reason
    })


if __name__ == '__main__':
    app.run(debug=True)
