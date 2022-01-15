"""
A Flask server to receive files.
The server will accept files as HTTP POST form request.
CAUTION: By running this, you are basically allowing anyone to write to your disk!

Use following command to upload
curl -X POST -F 'file=@<filename>' http://server-ip:9500/
"""

import os
import urllib.request
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename

from flask import Flask

UPLOAD_FOLDER = '.'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    # return True
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return """
    <html>
    <body>
        <form action="/" method="post" enctype="multipart/form-data">
            <input type="file" name="file"><br>
            <input type="submit" name="submit">
        </form>
    </body>
    </html>
    """


@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return 'failed, no file'
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return 'failed, no file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            return 'success'
        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            return 'failed due to type'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='9500')
