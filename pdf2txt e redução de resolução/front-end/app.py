from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    action = request.form.get('action')
    if action == 'reduce_resolution':
        resolution = request.form.get('resolution')
        response = requests.post('http://gs_service:5000/reduce_resolution', 
                                 files={'file': file},
                                 data={'resolution': resolution})
    elif action == 'convert_to_txt':
        response = requests.post('http://pdftotext_service:5000/convert_to_txt', 
                                 files={'file': file})
    else:
        return 'Invalid action', 400

    if response.status_code == 200:
        return redirect(url_for('download', filename=response.headers['Content-Disposition'].split('"')[1]))
    else:
        return 'Error', 500

@app.route('/download/<filename>')
def download(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
