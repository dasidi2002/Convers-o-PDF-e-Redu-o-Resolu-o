from flask import Flask, request, jsonify, send_file
import subprocess
import os

app = Flask(__name__)

@app.route('/convert_to_txt', methods=['POST'])
def convert_to_txt():
    file = request.files['file']
    output_file = file.filename.rsplit('.', 1)[0] + '.txt'

    file.save(file.filename)

    pdftotext_command = ['pdftotext', file.filename, output_file]

    try:
        subprocess.run(pdftotext_command, check=True)
        return send_file(output_file, as_attachment=True)
    except subprocess.CalledProcessError as e:
        return jsonify({'error': str(e)}), 500
    finally:
        os.remove(file.filename)
        if os.path.exists(output_file):
            os.remove(output_file)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
