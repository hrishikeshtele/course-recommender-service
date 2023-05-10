import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import resume_parser
from flask_cors import CORS


ALLOWED_EXTENSIONS = {'txt', 'doc', 'docx', 'pdf'}
UPLOAD_FOLDER = './resumes/'

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CORS(app)

"""
Resume parser service
"""


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/resume/parse', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    files = request.files.getlist("file")
    resumes = []
    for file in files:
        if file.filename == '':
            resp = jsonify({'message': 'No file selected for uploading'})
            resp.status_code = 400
            return resp
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            resumes.append(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            resp = jsonify({'message': 'Allowed file types are txt, doc, docx, pdf'})
            resp.status_code = 400
            return resp

    resp = jsonify(resume_parser.parse_resume(resumes))
    resp.status_code = 200
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
