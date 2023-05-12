import './App.css';
import ResumeForm from './Pages/ResumeForm';
import Landing from './Pages/Landing';
import { BrowserRouter as Router, Route,Routes} from "react-router-dom";


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/landing" element={<ResumeForm/>}/>
        <Route path="/dummy" element={<Landing/>}/>
      </Routes>
    </Router>
  );
}

export default App;
