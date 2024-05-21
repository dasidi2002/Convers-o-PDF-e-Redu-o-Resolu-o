from flask import Flask, request, jsonify

app = Flask(__name__)

logs = []

@app.route('/log', methods=['POST'])
def log():
    token = request.headers.get('Authorization')
    if token != 'valid_token':
        return jsonify({'error': 'Unauthorized'}), 401

    log_entry = request.json
    logs.append(log_entry)
    return jsonify({'message': 'Log entry added'}), 200

@app.route('/logs', methods=['GET'])
def get_logs():
    token = request.headers.get('Authorization')
    if token != 'valid_token':
        return jsonify({'error': 'Unauthorized'}), 401

    return jsonify(logs), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
