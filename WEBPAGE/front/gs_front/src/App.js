import './App.css';
import './index.css';
import Navbar from './components/Navbar';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import AboutUs from './pages/AboutUs';
import Pricing from './pages/Pricing';
import Home from './pages/Home';

function App() {
  return (
    <Router> 
    <div className="App">
      <Navbar />  
      <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<AboutUs />} />
          <Route path="/pricing" element={<Pricing />} />
        </Routes>
    </div>
    </Router>
  );
}

export default App;
