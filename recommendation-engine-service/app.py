from flask import Flask, request, jsonify

from main import REngine
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
"""
Recommendation service
"""


@app.route('/v1/predict', methods=['POST'])
def predict_v1():
    if request.form['skills'] is None:
        resp = jsonify({'message': 'No skills in the request'})
        resp.status_code = 400
        return resp

    output = REngine.create_sim(request.form['skills'])
    if output.empty:
        resp = jsonify({'message': 'No courses found'})
        resp.status_code = 404
        return resp
    output = output.rename(
        columns={'Course Description': 'course_description', 'Course Name': 'course_name',
                 'Course Rating': 'course_rating',
                 'Course URL': 'course_url', 'Difficulty Level': 'difficulty_level', 'Skills': 'skills',
                 'University': 'university'})

    resp = jsonify(output.to_dict('records'))
    resp.status_code = 200
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
