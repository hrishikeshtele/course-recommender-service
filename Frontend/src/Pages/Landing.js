import axios from "axios";
import { useState } from "react";
import {
  TextField,
  InputLabel,
  Button,
  Grid,
  Fab,
} from "@material-ui/core";
import videobg from "../Media/video1.mp4";
import videobg1 from "../Media/video2.mp4";
import videobg2 from "../Media/video3.mp4";
import videobg3 from "../Media/video4.mp4";
import "../App.css";
import "bootstrap/dist/css/bootstrap.min.css";
import "./Landing.scss";

export default function Landing() {
  const [resume, setResume] = useState(null);
  const [jobTitle, setJobTitle] = useState("");
  const [jobLocation, setJobLocation] = useState("");
  const [jobSkills, setJobSkills] = useState([]);
  const [resumeSkills, setResumeSkills] = useState([]);
  const [selectedSkills, setSelectedSkills] = useState([]);
  const [combinedSkills, setCombinedSkills] = useState([]);
  const [open, setOpen] = useState(false);
  const [courses, setCourses] = useState([]);
  const [name, setName] = useState("");

  const handleResumeChange = (event) => {
    setResume(event.target.files[0]);
  };

  const handleJobTitleChange = (event) => {
    setJobTitle(event.target.value);
  };

  const handleJobLocationChange = (event) => {
    setJobLocation(event.target.value);
  };

  const handleClose = () => {
    setOpen(false);
  };
  const handleOpen = () => {
    setOpen(true);
  };

  function refreshPage() {
    window.location.reload();
  }

  const handleViewCourses = async (event) => {
    try {
      event.preventDefault();
      const url = "http://localhost:5001/v1/predict";
      const skills = selectedSkills.join(' ');
      console.log(skills);
      const courseResponse = await axios.get(url,
        {
            params: {
                skills:skills
              
            }}       
       
       
       )
      setCourses(courseResponse.data);
      console.log(courseResponse.data);
    } catch (error) {
      console.log(error);
    }
  };

  const handleSubmitAsync = async (event) => {
    try {
      handleOpen();
      event.preventDefault();
      const url1 = "http://localhost:5002/job";
      const url2 = "http://localhost:5003/resume/parse";
      const formData = new FormData();
      formData.append("file", resume);
      var jobSkillRes;
      const resumeSkillsRes = await axios.post(url2, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      
      setResumeSkills(resumeSkillsRes.data[0].skills);
      try{
      jobSkillRes = await axios.get(url1, {
        params: {
          job_title: jobTitle,
          location:'United states',
        },
      });
    }
    catch(error){
      console.log(error);

    }
   

    var skillsList1=[];
    
    if(jobSkillRes!= undefined && jobSkillRes.data.skills.length>0){
      skillsList1 = jobSkillRes.data.skills[0][1].map((skill) => skill.toLowerCase());
    }
    const skillsList2 = resumeSkillsRes.data[0].skills.map((skill) => skill.toLowerCase());

    const finalSkills = [...new Set([...skillsList1, ...skillsList2])];
    
    setCombinedSkills(finalSkills);
    setName(resumeSkillsRes.data.name);
    handleClose();
    } 
    catch (error) {
      console.log(error);
      console.log("some error occured");
    }
  };

  const handleSkillChange = (event) => {
    const skill = event.target.value;
    const isChecked = event.target.checked;

    if (isChecked) {
      setSelectedSkills([...selectedSkills, skill]);
    } else {
      const updatedSkills = selectedSkills.filter(
        (selectedSkill) => selectedSkill !== skill
      );
      setSelectedSkills(updatedSkills);
    }
  };

  return (
    <div>
      <div>
        <video
          style={{ width: "100%", objectFit: "fill" }}
          src={videobg}
          autoPlay
          loop
          muted
        />
        <div
          style={{
            position: "absolute",
            height: "100%",
            width: "100%",
            top: "0",
            display: "flex",
            color: "white",
            paddingLeft: "450px",
            paddingTop: "50px",
            fontFamily: "Roboto",
          }}
        >
          <h1>Career accelaration starts here</h1>
        </div>
        <div
          style={{
            position: "absolute",
            top: "0",
            paddingLeft: "300px",
            paddingTop: "160px",
            fontFamily: "serif",
          }}
        >
          <Grid
            style={{ paddingTop: "20px", paddingLeft: "50px" }}
            container
            spacing={2}
          >
            <Grid item xs={7} style={{ color: "white" }}>
              <InputLabel
                style={{
                  paddingBottom: "10px",
                  color: "white",
                  fontFamily: "serif",
                }}
              >
                <strong>Job Title</strong>
              </InputLabel>
              <TextField
                style={{ width: "300px" }}
                inputProps={{ style: { color: "white" } }}
                onChange={handleJobTitleChange}
                id="filled-basic"
                variant="filled"
                size="small"
              />
            </Grid>
            <Grid item xs={5}>
              <InputLabel
                style={{
                  paddingBottom: "10px",
                  color: "white",
                  fontFamily: "serif",
                }}
              >
                <strong>Job Location</strong>
              </InputLabel>
              <TextField
                style={{ width: "300px" }}
                inputProps={{ style: { color: "white" } }}
                onChange={handleJobLocationChange}
                id="filled-basic"
                variant="filled"
                size="small"
              />
            </Grid>

            <br></br>
          </Grid>
          <div style={{ paddingTop: "100px", paddingLeft: "290px" }}>
            <label htmlFor="resume">
              <input
                style={{ display: "none" }}
                id="resume"
                name="resume"
                type="file"
                onChange={handleResumeChange}
              />

              <Fab
                style={{
                  border: "2.5px black",
                  height: "38px",
                  width: "180px",
                }}
                size="small"
                component="span"
                aria-label="add"
                variant="extended"
                color="primary"
              >
                <div
                  style={{
                    color: "white",
                  }}
                >
                  <strong style={{ fontFamily: "serif" }}>
                    Upload a resume
                  </strong>
                </div>
              </Fab>
            </label>
            <br></br>
          </div>
          <div style={{ paddingLeft: "290px", paddingTop: "80px" }}>
            <Button
              style={{ width: "180px", fontFamily: "serif" }}
              color="primary"
              variant="contained"
              size="medium"
              onClick={handleSubmitAsync}
            >
              <strong>Search</strong>
            </Button>
          </div>
          {open && (
            <div style={{ paddingLeft: "320px", color: "white" }}>
              <h1>Loading....</h1>
            </div>
          )}
        </div>

        <div></div>
      </div>
      {/* {combinedSkills.length==0 && <div></div>} */}

      {combinedSkills.length > 0 && (
        <div className="container">
          <div class="row">
            <div class="col-3"></div>

            <div class="col-6" style={{ textAlign: "center" }}>
              <table className="styled-table" style={{ width: "100%" }}>
                <thead>
                  <tr style={{ background: "#04AA6D", color: "white" }}>
                    <th
                      colSpan="2"
                      className="table-header"
                      style={{ textAlign: "center" }}
                    >
                      <h3> Recommended Skills</h3>
                    </th>
                  </tr>
                </thead>
                {combinedSkills.map((skill, index) => (
                  <tr className="active-row">
                    <td style={{ border: "1px solid #ddd" }}>
                      <div key={index}>
                        <input
                          type="checkbox"
                          value={skill}
                          checked={selectedSkills.includes(skill)}
                          onChange={handleSkillChange}
                        />
                      </div>
                    </td>
                    <td
                      style={{
                        textAlign: "center",
                        color: "black",
                        border: "1px solid #ddd",
                      }}
                    >
                      {skill}
                    </td>
                  </tr>
                ))}
              </table>
              <div style={{ paddingTop: "20px" }}>
                <Button
                  style={{ width: "180px" }}
                  color="primary"
                  variant="contained"
                  size="medium"
                  onClick={handleViewCourses}
                >
                  <strong>View Courses</strong>
                </Button>
              </div>
              <div class="col-3"></div>
            </div>
          </div>
        </div>
      )}

      {courses.length > 0 && (
        <div className="container">
          <h2 style={{ textAlign: "center" }}>Recommended Courses</h2>
          <div className="row">
            <div class="col-2"></div>

            <div class="col-8">
              {courses.map((course, index) => (
                <div key={index} className="course-card">
                  <table className="course-table">
                    <thead>
                      <tr>
                        <th
                          colSpan="2"
                          className="table-header"
                          style={{ textAlign: "center" }}
                        >
                          <h3>{course.course_name}</h3>
                        </th>
                      </tr>
                    </thead>

                    <tbody>
                      <tr>
                        <th>Description </th>
                        <td>
                          <div class="show-hide-text wrapper">
                            <a
                              id="show-more"
                              class="show-less"
                              href="#show-less"
                            >
                              Show less
                            </a>
                            <a
                              id="show-less"
                              class="show-more"
                              href="#show-more"
                            >
                              Show more
                            </a>
                            <p>{course.course_description} </p>
                          </div>
                        </td>
                      </tr>

                      <tr>
                        <th>Skills </th>
                        <td>
                          <p>
                            {" "}
                            <p>{course.skills}</p>
                          </p>
                        </td>
                      </tr>
                      <tr>
                        <th>Difficulty Level</th>
                        <td>
                          <p> {course.difficulty_level}</p>
                        </td>
                      </tr>
                      <tr>
                        <th>Course Rating </th>
                        <td>
                          <p>{course.course_rating}</p>
                        </td>
                      </tr>
                      <tr>
                        <th>University</th>
                        <td>
                          <p> {course.university}</p>
                        </td>
                      </tr>
                      <tr>
                        <th> Course URL </th>
                        <td>
                          <p>
                            {" "}
                            <p>
                              <a href={course.course_url}>
                                {course.course_url}
                              </a>
                            </p>
                          </p>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              ))}
            </div>
            <div class="col-2"></div>
          </div>

          <div className="container">
        <div class="row">
          <button
            type="button"
            class="btn btn-primary btn-lg"
            onClick={refreshPage}
          >
            Try another
          </button>
        </div>
      </div>
        </div>

        
      )}
      
      <div>
        <Grid container spacing={2}>
          <Grid item xs={5}>
            <div style={{ paddingLeft: "30px" }}>
              <video
                style={{ width: "110%", objectFit: "contain" }}
                src={videobg1}
                autoPlay
                loop
                muted
              />
            </div>
          </Grid>
          <Grid item xs={2}>
            <div
              style={{
                fontFamily: "serif",
                color: "indigo",
                paddingTop: "200px",
                paddingLeft: "240px",
              }}
            >
              <h1>Smart&nbsp;Parsing</h1>
            </div>
          </Grid>
        </Grid>
      </div>

      <div>
        <Grid container spacing={2}>
          <Grid item xs={5}>
            <div
              style={{
                fontFamily: "serif",
                color: "darkorange",
                paddingTop: "170px",
                paddingLeft: "150px",
                paddingTop: "250px",
              }}
            >
              <h1>Smart&nbsp;Skills&nbsp;Engine</h1>
            </div>
          </Grid>
          <Grid item xs={5}>
            <div style={{ paddingLeft: "30px" }}>
              <video
                style={{ width: "110%", objectFit: "contain" }}
                src={videobg2}
                autoPlay
                loop
                muted
              />
            </div>
          </Grid>
        </Grid>
      </div>

      <div>
        <Grid container spacing={2}>
          <Grid item xs={5}>
            <div style={{ paddingLeft: "30px" }}>
              <video
                style={{ width: "110%", objectFit: "contain" }}
                src={videobg3}
                autoPlay
                loop
                muted
              />
            </div>
          </Grid>
          <Grid item xs={2}>
            <div
              style={{
                fontFamily: "serif",
                paddingTop: "200px",
                paddingLeft: "240px",
              }}
            >
              <h1>Extract&nbsp;and&nbsp;harmonize</h1>
              <h1>key&nbsp;elements&nbsp;from</h1>
              <h1>jobs</h1>
            </div>
          </Grid>
        </Grid>
      </div>
    </div>
  );
}
