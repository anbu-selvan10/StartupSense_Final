import React, { useState, useEffect } from 'react';
import './aboutStyle.css'
import image from './bussiness.png' 
import axios from 'axios'
import { useNavigate } from 'react-router-dom';
import { useAuth } from './AuthProvider';

const About = () => {
  const [user, setUser] = useState({
    username: '',
    email: '',
    bio:''
  });

  const { logoutAuth } = useAuth();

  let navigate = useNavigate();

  const token = localStorage.getItem('authtoken');

  useEffect(() => {
    axios.get('http://localhost:4000/userprofile', {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => {
        const { username, email, bio } = response.data;
        setUser({ username, email, bio });
    })
    .catch(error => {
        console.error("Error fetching profile data:", error);
    });
  }, []);

  const logout = () => {
    localStorage.removeItem('authtoken');
    localStorage.setItem('isLoggedIn', false);
    navigate('/Login');
  }

  return (
    <div className='wrap'>
    <div className="profile">
      <div>
      <img 
        src={ image}
        alt={`${user.username}'s Profile`}
        className="profile-image Bus"
      />
      </div>
      <div className="profile-info">
        <section className='details'> 
          <p style={{border:'1px solid black',padding:'0.5rem',paddingLeft:'1rem',paddingRight:'1rem',width:'30vw'}}>Username: {user.username}</p>
          <p style={{border:'1px solid black',padding:'0.5rem',paddingLeft:'1rem',paddingRight:'1rem',width:'30vw'}}>Email: {user.email}</p>
          <p style={{border:'1px solid black',padding:'0.5rem',paddingLeft:'1rem',paddingRight:'1rem',height:'15vh',gap:'0',overflow:'scroll'}}>Bio: {user.bio}</p>
          <div className="button">
                <button onClick={logout}  type='submit' className="submit-button">Logout</button>
        
                
                </div>
          </section>
        </div>
    </div>
    </div>
  );
};

export default About;
