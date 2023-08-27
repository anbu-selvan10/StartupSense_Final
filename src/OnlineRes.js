import React from 'react'
import {Link} from 'react-router-dom'
import uber from './Uber-logo.png'
import tn from './tn.jpg'
import spoimg from './Spotify-Logo.wine.svg'
import './onlineRes.css'
import art1 from './art1.jpeg'
import art2 from './Art2.jpeg'
import art3 from './Art3.jpeg'
import book from './book.jpeg'

const OnlineRes = () => {
  return (
    <>
        <h1 className='homeWelcome'>Case Study</h1>
        <br /><br />
        <div className='OnlineReBox'>
        
            <div className="card" style={{ width: '18rem' }}>
                <img src={uber}  className="card-img-top" alt="..." />
                <div className="card-body">
                    <h5 className="card-title">UBER</h5>
                    <p className="card-text">UBER: A disruptive TNC that connects riders with drivers</p>
                    <Link to='/online_resources/uber' className="btn btn-primary" >Read this</Link>
                    </div>
            </div>

            <div className="card" style={{ width: '18rem' }}>
                <img src={tn} style={{backgroundColor:'white'}} className="card-img-top" alt="..." />
                <div className="card-body">
                    <h5 className="card-title">StartupTN</h5>
                    <p className="card-text">StartupTN: Tamil Nadu Government's Startup Ecosystem Support Program</p>
                    <Link to='/online_resources/startuptn' className="btn btn-primary" >Read this</Link>
                    </div>
            </div>

            <div className="card" style={{ width: '18rem' }}>
                <img src={spoimg} style={{backgroundColor:'white'}} className="card-img-top" alt="..." />
                <div className="card-body">
                    <h5 className="card-title">Spotify</h5>
                    <p className="card-text">Spotify: Music streaming pioneer, personalized playlists, global impact, podcast evolution.</p>
                    <Link to='/online_resources/spotify' className="btn btn-primary" >Read this</Link>
                    </div>
            </div>
        </div>
        
        <h1 className='homeWelcome'>Articles</h1>
        <br /><br />
        <div className='OnlineReBox'>
        
            <div className="card" style={{ width: '18rem' }}>
                <img src={art1}  className="card-img-top" alt="..." />
                <div className="card-body">
                    <h5 className="card-title">Four Changes</h5>
                    <p className="card-text">4 Changes: New Companies Should Adopt in 2023 to Set Yourself Up for Success</p>
                    <Link to='/online_resources/art1' className="btn btn-primary" >Read this</Link>
                    </div>
            </div>

            <div className="card" style={{ width: '18rem' }}>
                <img src={art2} style={{backgroundColor:'white'}} className="card-img-top" alt="..." />
                <div className="card-body">
                    <h5 className="card-title">Increase Startup's visibility</h5>
                    <p className="card-text">5 Ways Startups Can Increase Their Visibility</p>
                    <Link to='/online_resources/Art2' className="btn btn-primary" >Read this</Link>
                    </div>
            </div>

            <div className="card" style={{ width: '18rem' }}>
                <img src={art3} style={{backgroundColor:'white'}} className="card-img-top" alt="..." />
                <div className="card-body">
                    <h5 className="card-title">Startup Funding Alternatives</h5>
                    <p className="card-text">Three Alternatives to Startup Venture Capital Funding</p>
                    <Link to='/online_resources/Art3' className="btn btn-primary" >Read this</Link>
                    </div>
            </div>
        </div>
        <h1 className='homeWelcome'>E-Books</h1>
        <div className='Book'>
            

            <div className="card" style={{ width: '18rem' }}>
                <img src={book} style={{backgroundColor:'white'}} className="card-img-top" alt="..." />
                <div className="card-body">
                    <h5 className="card-title">Startup Smart</h5>
                    <p className="card-text"> A Handbook for Entrepreneurs</p>
                    <a href='https://pdf.booksbenefit.com/read-online/4754/' className="btn btn-primary" >Read this E-book</a>
                    </div>
            </div>
        </div>




    </>
  )
}

export default OnlineRes