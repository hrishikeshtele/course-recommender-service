# Course Recommendation
A Revolutionized Course Recommendation Approach Based On User Background & Career Goals

## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install required libs.

```bash
pip install -r job-scrapper-service/requirements.txt
pip install -r recommendation-engine-service/requirements.txt
pip install -r resume-parser-service/requirements.txt
python -m spacy download en_core_web_lg
python -m spacy download en_core_web_sm
python -m spacy download en
```

## Database
```
Create a postgres db and update the credentials in job-scrapper-service/dbwrapper.py
```
## Running the Services
```bash
python job-scrapper-service/app.py
python recommendation-engine-service/app.py
python resume-parser-service/app.py
```

## APIs
```
http://127.0.0.1:5001/v1/predict?skills=aws python database
    skills is a query paramter
    
http://127.0.0.1:5002/v1/job?job_title=Software Engineer&location=united states
    job_title and locations are query paramters
    
http://127.0.0.1:5003/v1/resume/parse
    Attach resume file as a file key in form data
```

## Frontend
Download and install nodejs https://nodejs.org/en/download
```bash
cd Frontend
npm install
npm start
```


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.