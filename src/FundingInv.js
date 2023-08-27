import React, { useState } from 'react'
import './fundingInv.css'
import axios from 'axios'

const FundingInv = () => {

  const [investorName, setInvestorName] = useState("Warburg Pincus");
  const [graphs, setGraphs] = useState({});

  const startupData = [
    "IDG Ventures",
    "Mumbai Angels Network",
    "Amour Infrastructure",
    "Ant Financial",
    "Baillie Gifford",
    "DST Global",
    "Falcon Edge Capital",
    "Foxconn",
    "Greenoaks Capital Partners Hero Enterprise",
    "Info Edge (India) Ltd I",
    "Kalaari Capital",
    "Lightspeed Venture Partners",
    "Matrix Partners",
    "NY based Hedge Fund",
    "Sequoia Capital India Advisors",
    "SIMI Pacific Pte",
    "SoftBank Group",
    "SoftBank Group Corp",
    "SoftBank Vision Fund",
    "Stellaris Venture Partners",
    "Steadview Capital",
    "Tiger Global",
    "Vijay Shekhar Sharma",
    "Warburg Pincus"
  ];
  const selectedStartup="Foxconn"
  const getGraphs = async () => {
    try {
        const response = await axios.post('http://localhost:5000/analyse', { investorName });
        setGraphs(response.data);
    } catch (error) {
        console.error("Error fetching graphs:", error);
    }
}
  
const auth = localStorage.getItem('isLoggedIn');

  return (
    
    <div className="container">
      <p>This <b>Data Analysis Model</b> is completely based on the real-world data. This shows the city, round, yearly investments and industry sectors in which the investor invested to give an overview abouth the investors to the entrepreneurs</p>
      <form className='Form' onSubmit={(e)=>e.preventDefault()}>
        <label htmlFor="startupdata">Select the Investor : </label>
      <div className="input-group">
        
            
      <select
  id="startupdata"
  value={investorName}
  onChange={e => setInvestorName(e.target.value)}
  className="select-input"
>
  {startupData.map((startup, index) => (
    <option
      key={index}
      value={startup}
      selected={startup === "Foxconn"}
    >
      {startup}
    </option>
  ))}
</select>

     
      </div>
      <br></br><br />
                <div className="button">
                <button  type='submit' onClick={getGraphs} className="submit-button">Submit</button>
                </div>
      
           
        </form>

        
        

        <div className='graph'>
  
  {graphs.graph2 ? (
    <h5 className='Letters'>A startup's region decides its success or failure. {investorName} has invested in the startups in the following cities. Give it a go!:</h5>
  ) : null}
  {graphs.graph1 && <img className='datas' src={graphs.graph1} alt="Graph 1" />}
  
  {graphs.graph2 ? (
    <h5 className='Letters'>A startup's perfomance in the rounds shapes its future. {investorName} has invested in the startups in the following rounds. Give it a go!:</h5>
  ) : null}
  {graphs.graph2 && <img className='datas' src={graphs.graph2} alt="Graph 2" />}
  
  {graphs.graph3 ? (
    <h5 className='Letters'>The active investment of the investors show their integrity in unicorn development country. {investorName} has invested in the startups in the years. Give it a go!:</h5>
  ) : null}
  {graphs.graph3 && <img className='datas' src={graphs.graph3} alt="Graph 3" />}
  
  {graphs.graph4 ? (
    <h5 className='Letters'>The investors show a desire for a particular industry sector or their versatility in various sectors. {investorName} has invested in the startups in the following industry sectors. Give it a go!:</h5>
  ) : null}
  {graphs.graph4 && <img className='datas' src={graphs.graph4} alt="Graph 4" />}
</div>

    </div>
    
  )
}

export default FundingInv