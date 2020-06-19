import os
import traceback
from urllib.parse import quote

from flask import Flask, make_response, render_template, request, url_for

from splitter import splitter

app = Flask(__name__)
app.config.from_object('config')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/split', methods=['POST'])
def split():
    if 'uploadFile' not in request.files:
        message = 'uploadFile is required.'
        return make_response(message, 400)

    pdf_file = request.files['uploadFile']
    basename, ext = os.path.splitext(pdf_file.filename)

    if ext not in ('.pdf', '.PDF'):
        message = 'File extention must be ".pdf" or ".PDF"'
        return make_response(message, 400)

    output = splitter(pdf_file.stream, request.form['split_type'])

    response = make_response()
    response.data = output
    download_name = quote(f'{basename}_split.pdf')
    response.headers['Content-Disposition'] = f'attachment; filename={download_name}'
    response.mimetype = 'application/pdf'

    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
