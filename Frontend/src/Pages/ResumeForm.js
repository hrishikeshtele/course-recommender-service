import React, { useState } from 'react';
import axios from 'axios';

function ResumeForm() {
  const [resume, setResume] = useState(null);
  const [jobTitle, setJobTitle] = useState('');

  const handleResumeChange = (event) => {
    setResume(event.target.files[0]);
  }

  const handleJobTitleChange = (event) => {
    setJobTitle(event.target.value);
  }

  const handleSubmit = (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append('resume', resume);
    formData.append('jobTitle', jobTitle);
    const url = "http://localhost:8080/accept";
    axios.post(url, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    .then((response) => {
      console.log(response.data);
    })
    .catch((error) => {
      console.error(error);
    });
  }

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Job Title:
        <input type="text" value={jobTitle} onChange={handleJobTitleChange} />
      </label>
      <label>
        Resume:
        <input type="file" onChange={handleResumeChange} />
      </label>
      <button type="submit">Submit</button>
    </form>
  );
}

export default ResumeForm;
