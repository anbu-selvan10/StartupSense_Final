import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import FundingInv from './FundingInv';
import './Header.css';
import LoginPage from './LoginPage';
import Home from './Home'
import SuccessPre from './SuccessPre';
import OnlineRes from './OnlineRes';
import UberDes from './UberDes';
import SpotifyDes from './SpotifyDes';
import About from './About';
import StartupTN from './StartupTN';
import { Authentication } from './AuthProvider';
import { useAuth } from './AuthProvider';
import Art1 from './Art1';
import Art2 from './Art2';
import Art3 from './Art3';

function App() {
  console.log(localStorage.getItem('isLoggedIn'));
  const isAuthenticated = localStorage.getItem('isLoggedIn');
  return (
  
    <div className="App">
      
        <header>
          <nav className="navbar">
            <div className="logo">
              <p className='logotext'>StartupSense</p>
            </div>
            <ul className="nav-options" >
            <Link  className='li home' to="/Login" style={{padding:"8px"}} ><li >Login</li></Link>
            <Link
              className={`li ${isAuthenticated ? '' : 'disabled'}`}
              to="/success_predictor"
            >
              <li>Success Predictor Model</li>
            </Link>
            <Link
              className={`li ${isAuthenticated ? '' : 'disabled'}`}
              to="/funding_investor"
            >
              <li>EDA of Funding Investors</li>
            </Link>
            <Link
              className={`li ${isAuthenticated ? '' : 'disabled'}`}
              to="/online_resources"
              style={{ padding: "8px" }}
            >
              <li>Online Resources</li>
            </Link>
            <Link
              className={`li ${isAuthenticated ? '' : 'disabled'}`}
              to="/about"
              style={{ padding: "8px" }}
            ><li>Profile</li></Link>
            {/* <Link  className='li home' to="/Login" style={{padding:"8px"}} ><li >Login</li></Link>
              <Link className='li' to="/success_predictor" ><li >Success Predictor Model</li></Link>
              <Link className='li' to="/funding_investor" ><li >EDA of Funding Investors</li></Link>
              <Link className='li' to="/online_resources" style={{padding:"8px"}}><li >Online Resources</li></Link>
              <Link className='li' to='/about' style={{padding:"8px"}}><li >Profile Page</li></Link>
               */}
            </ul>
          </nav>
        </header>

        
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path='/Login' element={<LoginPage />}></Route>
          <Route path='/success_predictor' element={<SuccessPre/>}></Route>
          <Route path='/funding_investor' element={<FundingInv/>}></Route>
          <Route path='/online_resources' element={<OnlineRes/>}></Route>
          <Route path='/online_resources/uber' element={<UberDes/>}></Route>
          <Route path='/online_resources/spotify' element={<SpotifyDes/>}></Route>
          <Route path='/online_resources/startuptn' element={<StartupTN/>}></Route>
          <Route path='/online_resources/Art1' element={<Art1/>}></Route>
          <Route path='/online_resources/Art2' element={<Art2/>}></Route>
          <Route path='/online_resources/Art3' element={<Art3/>}></Route>
          <Route path='/about' element={<About/>}></Route>
        </Routes>
        
        </div>
    
  );
}

export default App;