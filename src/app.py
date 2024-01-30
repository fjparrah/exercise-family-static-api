from flask import Flask, jsonify, request
from datastructures import Family

app = Flask(__name__)
jackson_family = Family('Jackson')

@app.route('/members', methods=['GET'])
def get_all_members():
    return jsonify(jackson_family.get_all_members()), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({'error': 'Member not found'}), 404

@app.route('/member', methods=['POST'])
def add_member():
    try:
        data = request.get_json()
        jackson_family.add_member(data)
        return jsonify({}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        jackson_family.delete_member(member_id)
        return jsonify({'done': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    app.run(debug=True)
