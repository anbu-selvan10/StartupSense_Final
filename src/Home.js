import React from 'react'

import './Home.css'

const Home = () => {
  return (
    <div className='Home'>
        <h1 className='homeWelcome'>Welcome To StartupSense</h1>
        
        <div className='AllCards'>
        <div className="card indic" style={{width:'18rem'}}>
        
        <div className="card-body">
            <h5 className="card-title">Success Predictor Model</h5>
            <p className="card-text"><pre style={{display:'inline'}}>  It</pre> involves using machine learning algorithms and data analysis techniques to predict the likelihood of a startup's success based on various factors such as funding, market trends, industry type, and more. Users would input relevant information about their startup, and the app would provide them with a prediction or score indicating the potential success of their venture. The prediction could be presented as a categorical classification.</p>
            
        </div>
    </div>
    <div className="card indic" style={{width:'18rem'}}>
        <div className="card-body">
            <h5 className="card-title">EDA of Funding Investors</h5>
            <p className="card-text"><pre style={{display:'inline'}}>  EDA</pre> stands for Exploratory Data Analysis. In this feature, our WebApp would analyze and visualize datasets related to startup funding and investors. Users could explore trends in funding amounts, funding sources (such as venture capital, angel investors), geographical distribution of investors, industries that attract more funding, and so on. Interactive charts, graphs, and data visualizations would help users gain insights into funding patterns and investor behavior, which could inform their decision-making process.</p>
            
        </div>
    </div>

    <div className="card indic" style={{width:'18rem'}}>
        
        <div className="card-body">
            <h5 className="card-title">Online Resources</h5>
            <p className="card-text"><pre style={{display:'inline'}}>  This</pre> feature serves as a knowledge hub for aspiring entrepreneurs. It would provide a curated collection of online resources, articles, videos, and guides related to startup success, business strategies, pitching to investors, market analysis, product development, and more. Users can access valuable information to enhance their understanding of the startup ecosystem and improve their chances of success. This section could also include success stories of well-known startups to inspire and motivate users.</p>
            
        </div>
    </div>
    </div>
    </div>
    
  ) 
}

export default Home