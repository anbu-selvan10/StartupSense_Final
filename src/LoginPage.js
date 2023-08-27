import React, { useState } from 'react'
import "./Home.css"
import image from './bussiness.png' 
import axios from 'axios'
import { useAuth } from './AuthProvider'

const Header = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [bio, setBio] = useState("");
    const [message, setMessage] = useState("");
    const [email, setEmail] = useState("");
    const [showRegister, setShowRegister] = useState(false);
    //new
    const { loginAuth } = useAuth();
    
    const register = () => {
        axios.post('http://localhost:4000/register', { username, password, email, confirm_password: confirmPassword, bio })
            .then(response => {
                console.log(response.data);
                alert(response.data.message);
            })
            .catch(error => {
                console.error("Registration error:", error);
                alert(error.response.data.message);
            });
    };

    const login = () => {
        axios
    .post("http://localhost:4000/login", {username, password})
    .then((res) => {
        if(res.data.token){
        localStorage.setItem("isLoggedIn", true);
      const token = res.data.token;
      localStorage.setItem("authtoken", token);
        alert("Login Successful");
}
    });


}

    console.log(localStorage.getItem('isLoggedIn'));

  return (  
    <div className='Main'>
    
    <img className="Bus" src={image}></img>
    <form>
    {showRegister ? (
                <div className='DetailsSign'>
                    <div className='Username'><input value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Enter Username" /></div>
                    <div className='Username'><input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Enter Email" /></div>
                    <div className='Password'><input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder=" Enter Password" /></div>
                    <div className='Password'><input type="password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} placeholder="Confirm Password" /></div>
                    <div className='Username'><textarea value={bio} onChange={(e) => setBio(e.target.value)} placeholder="Enter Bio" /></div>
                    <div className='Button'><button onClick={register}>Register</button></div>
                    <div className='Button'><button onClick={() => setShowRegister(false)}>Go back to login</button></div>
                <p>{console.log(localStorage.getItem('isLoggedIn'))}</p>

                </div>
            ) : (
                <div>
                    <div className='Username'><input value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Username" /></div>
                    <div className='Password'><input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" /></div>
                    <div className='Button'><button onClick={login}>Login</button></div>
                </div>
            )}
            {!showRegister && <button className='SignUp' onClick={() => setShowRegister(true)}>Signup</button>}
            {message && <p>{message}</p>}
    </form>
    
</div>

  );
}

export default Header