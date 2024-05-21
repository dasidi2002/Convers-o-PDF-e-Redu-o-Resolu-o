from flask import Flask, request, jsonify, send_file
import subprocess
import os

app = Flask(__name__)

@app.route('/reduce_resolution', methods=['POST'])
def reduce_resolution():
    file = request.files['file']
    resolution = request.form.get('resolution', 'default')
    output_file = 'reduced_' + file.filename

    file.save(file.filename)

    gs_command = [
        'gs', '-sDEVICE=pdfwrite',
        '-dCompatibilityLevel=1.4',
        f'-dPDFSETTINGS=/{resolution}',
        '-dNOPAUSE', '-dQUIET', '-dBATCH',
        '-sOutputFile=' + output_file,
        file.filename
    ]

    try:
        subprocess.run(gs_command, check=True)
        return send_file(output_file, as_attachment=True)
    except subprocess.CalledProcessError as e:
        return jsonify({'error': str(e)}), 500
    finally:
        os.remove(file.filename)
        if os.path.exists(output_file):
            os.remove(output_file)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
