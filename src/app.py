import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from datastructures import Family
from utils import APIException, generate_sitemap

app = Flask(__name__)
jackson_family = Family('Jackson')
CORS(app)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_members():
    return jsonify(jackson_family.get_all_members()), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"error": "Miembro no encontrado"}), 400

@app.route('/member', methods=['POST'])
def add_member():
    member_data = request.json
    if 'first_name' in member_data and 'age' in member_data and 'lucky_numbers' in member_data:
        jackson_family.add_member(member_data)
        return jsonify({}), 200
    else:
        return jsonify({"error": "Missing required fields"}), 400

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    if jackson_family.delete_member(member_id):
        return jsonify({"done": True}), 200
    else:
        return jsonify({"error": "Miembro no encontrado"}), 400

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)

