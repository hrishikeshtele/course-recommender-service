from flask import Flask, request, jsonify

from scrapper import Scrapper
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
"""
Job Scrapper service
"""

scrapper = None


@app.route('/job', methods=['POST'])
def scrape_job():
    # check if the post request has the file part
    args = request.args
    job_title = args.get("job_title").lower().strip()

    if job_title is None or len(job_title) == 0:
        resp = jsonify({'message': 'No job title in the request'})
        resp.status_code = 400
        return resp

    location = args.get("location").lower().strip()

    if job_title is None or len(job_title) == 0:
        resp = jsonify({'message': 'No location in the request'})
        resp.status_code = 400
        return resp

    skills = scrapper.scrape_skills(job_title, location)
    resp = jsonify({'skills': skills})
    resp.status_code = 200
    return resp


@app.route('/all_jobs', methods=['GET'])
def scrape_all_jobs():
    # check if the post request has the file part
    scrapper.scrape_all_jobs()
    resp = jsonify({'skills': 'Added to DB'})
    resp.status_code = 200
    return resp


if __name__ == '__main__':
    scrapper = Scrapper()
    app.run(host='0.0.0.0', port=5002)
