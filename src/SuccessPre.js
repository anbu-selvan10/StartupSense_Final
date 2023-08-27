import React, { useState, useRef } from 'react';
import axios from 'axios';
import danger from './danger.jpg';
import './successPre.css';

const SuccessPre = () => {
     
  const [selectValues, setSelectValues] = useState({});
  const [predictionReceived, setPredictionReceived] = useState(false);
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);
  
  const predictionRef = useRef(null);

    const industryCodes = {
        'Administrative Services': 0,
        'Advertising': 1,
        'Agriculture and Farming': 2,
        'Apps': 3,
        'Artificial Intelligence': 4,
        'Biotechnology': 5,
        'Clothing and Apparel': 6,
        'Commerce and Shopping': 7,
        'Community and Lifestyle': 8,
        'Consumer Electronics': 9,
        'Consumer Goods': 10,
        'Content and Publishing': 11,
        'Data and Analytics': 12,
        'Design': 13,
        'Education': 14,
        'Energy': 15,
        'Events': 16,
        'Financial Services': 17,
        'Food and Beverage': 18,
        'Gaming': 19,
        'Government and Military': 20,
        'Hardware': 21,
        'Health Care': 22,
        'Information Technology': 23,
        'Internet Services': 24,
        'Manufacturing': 25,
        'Media and Entertainment': 26,
        'Messaging and Telecommunication': 27,
        'Mobile': 28,
        'Natural Resources': 29,
        'Navigation and Mapping': 30,
        'Other': 31,
        'Platforms': 32,
        'Privacy and Security': 33,
        'Professional Services': 34,
        'Real Estate': 35,
        'Sales and Marketing': 36,
        'Science and Engineering': 37,
        'Software': 38,
        'Sports': 39,
        'Sustainability': 40,
        'Transportation': 41,
        'Travel and Tourism': 42
      };
      
      const countryCodes = {
        'ALB': 0, 'ARE': 1, 'ARG': 2, 'ARM': 3, 'AUS': 4, 'AUT': 5, 'AZE': 6, 'BEL': 7, 'BGD': 8, 'BGR': 9,
        'BHR': 10, 'BHS': 11, 'BLR': 12, 'BMU': 13, 'BRA': 14, 'BRN': 15, 'BWA': 16, 'CAN': 17, 'CHE': 18,
        'CHL': 19, 'CHN': 20, 'CIV': 21, 'CMR': 22, 'COL': 23, 'CRI': 24, 'CYM': 25, 'CYP': 26, 'CZE': 27,
        'DEU': 28, 'DNK': 29, 'DOM': 30, 'DZA': 31, 'ECU': 32, 'EGY': 33, 'ESP': 34, 'EST': 35, 'FIN': 36,
        'FRA': 37, 'GBR': 38, 'GHA': 39, 'GIB': 40, 'GRC': 41, 'GTM': 42, 'HKG': 43, 'HRV': 44, 'HUN': 45,
        'IDN': 46, 'IND': 47, 'IRL': 48, 'ISL': 49, 'ISR': 50, 'ITA': 51, 'JAM': 52, 'JOR': 53, 'JPN': 54,
        'KEN': 55, 'KHM': 56, 'KOR': 57, 'KWT': 58, 'LAO': 59, 'LBN': 60, 'LIE': 61, 'LTU': 62, 'LUX': 63,
        'LVA': 64, 'MAF': 65, 'MAR': 66, 'MCO': 67, 'MDA': 68, 'MEX': 69, 'MKD': 70, 'MLT': 71, 'MMR': 72,
        'MUS': 73, 'MYS': 74, 'NGA': 75, 'NIC': 76, 'NLD': 77, 'NOR': 78, 'NPL': 79, 'NZL': 80, 'OMN': 81,
        'PAK': 82, 'PAN': 83, 'PER': 84, 'PHL': 85, 'POL': 86, 'PRT': 87, 'ROM': 88, 'RUS': 89, 'SAU': 90,
        'SGP': 91, 'SLV': 92, 'SOM': 93, 'SRB': 94, 'SVK': 95, 'SVN': 96, 'SWE': 97, 'SYC': 98, 'THA': 99,
        'TTO': 100, 'TUN': 101, 'TUR': 102, 'TWN': 103, 'TZA': 104, 'UGA': 105, 'UKR': 106, 'URY': 107,
        'USA': 108, 'UZB': 109, 'VNM': 110, 'ZAF': 111, 'ZWE': 112
      };
      const funding_rnd={
        '0-2':0,
        '2-20':1
      }
      const funding_year={
        '0-2':0,
        '2-49':1
      }
      
      const total_investment={
        '0-112500':0,
        '112500-1400300':1,
        '14400300-8205200':2,
        '8205200-40079503000':3

      }
      
      const venture={
        '0-85038.5':0,
        '85038.5-6000000':1,
        '6000000-2451000000':3
      }
    
      const seed={
        '0-28000':0,
        '28000-140000000':1
    }
    const debtf={
        'No':0,
        'Yes':1
    }
    const angel={
        'No':0,
        'Yes':1

    }
    const private_eq={
        'No':0,
        'Yes':1
    }
    const A={
        'No':0,
        'Yes':1
    }
    const B={
      'No':0,
      'Yes':1
  }
  const C={
    'No':0,
    'Yes':1
}
const D={
  'No':0,
  'Yes':1
}
const E={
  'No':0,
  'Yes':1
}
const F={
  'No':0,
  'Yes':1
}


      // function CountryOptions() {
      //   const options = Object.keys(countryCodes).map(countryCode => (
      //     <option key={countryCodes[countryCode]} value={countryCodes[countryCode]}>
      //       {countryCode}
      //     </option>
      //   ));
      //   }

        const auth = localStorage.getItem('authStatus');

        function handleSelectChange(event) {
          const { name, value } = event.target;
          setSelectValues(prevState => ({ ...prevState, [name]: value }));
          console.log(selectValues)
        }
        /*
        {
          ['a]:1,
        }
        */

      function handleSubmit(e) {
        e.preventDefault();

        const data = {
        cat_industry_group: selectValues.industryCode,
        cat_country_code: selectValues.countryCode,
        cat_funding_rounds: selectValues.fundingRounds,
        cat_diff_funding_year: selectValues.fundingYear,
        cat_total_investment: selectValues.totalInvestment,
        cat_venture: selectValues.venture,
        cat_seed: selectValues.seed,
        cat_debt_financing: selectValues.debtFinancing,
        cat_angel: selectValues.angel,
        cat_private_equity: selectValues.privateEquity,
        cat_round_A: selectValues.seriesA,
        cat_round_B: selectValues.seriesB,
        cat_round_C: selectValues.seriesC,
        cat_round_D: selectValues.seriesD,
        cat_round_E: selectValues.seriesE,
        cat_round_F: selectValues.seriesF
        };
        axios.post('http://localhost:5000/submit', data)
        .then(response => {
          setPredictionReceived(true);
          if (predictionRef.current) {
            predictionRef.current.scrollIntoView({ behavior: 'smooth' });
          }
          setPrediction(response.data.prediction);
          setError(null);
        })
        .catch(error => {
          setError("An error occurred while predicting.");
          console.log(error);
          setPrediction(null);
        });
    }

        return (
          
            <div className="container">
              <section style={{display:'flex'}}>
              <img src={danger} alt="" style={{height:'25px', width:'20px'}} />
              <h4 style={{textAlign:'left'}}>NOTE:</h4>
              
              </section>
             <h5>
              <ul><li>The machine learning model we employ demonstrates an impressive <b>accuracy rate of 87%</b> and we are fine-tuning to get the maximum accuracy with real-world data.</li> <li>We gather the necessary inputs solely for the purpose of predicting startup success.</li><li>It's important to note that we <b>prioritize the security and confidentiality </b>of our customer's details at all times.</li><li>This ML model is solely based on data over the years and <b> if you believe in Data Analysis-ML models</b> then give it a go!</li><li> 
              Our web app is accessible to the <strong>general public without requiring login but their data will be used for fine-tuning</strong>.<li>Authenticated users' data will not be used.</li></li></ul> </h5>
              <form className='Form' onSubmit={handleSubmit}>
                <div className="input-group">
                <label htmlFor="ingrp" >Industry Group of the Startup:</label>
                <select id="ingrp" name="industryCode" onChange={handleSelectChange} className="select-input" defaultValue="0">
                  {Object.keys(industryCodes).map(industrycode => (
                    <option key={industryCodes[industrycode]} value={industryCodes[industrycode]}>
                      {industrycode}
                    </option>
                  ))}

                </select>
                </div>
                <br></br>

                <div className="input-group">
                <label htmlFor="countcode">Country Code of the startup:</label>
                <select id="countcode" name="countryCode" onChange={handleSelectChange} className="select-input" defaultValue="0">
                  {Object.keys(countryCodes).map(countryCode => (
                    <option key={countryCodes[countryCode]} value={countryCodes[countryCode]}>
                      {countryCode}
                    </option>
                  ))}
                </select></div>
                <br></br> 

                <div className="input-group">
                <label htmlFor="funr">Funding Rounds of the startup in which it received investments:</label>
                <select id="funr" name="fundingRounds" onChange={handleSelectChange} className="select-input" defaultValue="0">
                  {Object.keys(funding_rnd).map(fundv => (
                    <option key={funding_rnd[fundv]} value={funding_rnd[fundv]}>
                      {fundv}
                    </option>
                  ))}
                </select> </div>
                <br></br>

                <div className="input-group">
                <label htmlFor="funy">Difference of Funding Years(Last Funded at - First Funded at):</label>
                <select id="funy" name="fundingYear" onChange={handleSelectChange} className="select-input" defaultValue="0">
                  {Object.keys(funding_year).map(fundy => (
                    <option key={funding_year[fundy]} value={funding_year[fundy]}>
                      {fundy}
                    </option>
                  ))}
                </select> </div>
                <br></br>

                <div className="input-group">
                <label htmlFor="totalinv">Total Investment of the startup (in USD):</label>
                <select id="totalinv" name="totalInvestment" onChange={handleSelectChange} className="select-input" defaultValue="0">
                  {Object.keys(total_investment).map(ti => (
                    <option key={total_investment[ti]} value={total_investment[ti]}>
                      {ti}
                    </option>
                  ))}
                </select> </div>
                <br></br>

                <div className="input-group">
                <label htmlFor="venture">Has the startup received venture in USD: </label>
                <select id="venture" name="venture" onChange={handleSelectChange} className="select-input" defaultValue="0">
                  {Object.keys(venture).map(vent => (
                    <option key={venture[vent]} value={venture[vent]}>
                      {vent}
                    </option>
                  ))}
                </select> </div>
                <br></br>

                <div className="input-group">
                <label htmlFor="seed">Has the startup received seed (in USD): </label>
                <select id="seed" name="seed" onChange={handleSelectChange} className="select-input" defaultValue="0">
                  {Object.keys(seed).map(se => (
                    <option key={seed[se]} value={seed[se]}>
                      {se}
                    </option>
                  ))}
                </select> </div>
                <br></br>

                <div className="input-group">
                <label htmlFor="debtf">Has the company received Debt Financing (in USD):</label>
                <select id="debtf" name="debtFinancing" onChange={handleSelectChange} className="select-input" defaultValue="0">
                  {Object.keys(debtf).map(debt => (
                    <option key={debtf[debt]} value={debtf[debt]}>
                      {debt}
                    </option>
                  ))}
                </select> </div>
                <br></br>

                <div className="input-group">
                <label htmlFor="angel">Has the company received from an Angel (in USD):</label>
                <select id="angel" name="angel" onChange={handleSelectChange} className="select-input" defaultValue="0">
                  {Object.keys(angel).map(ang => (
                    <option key={angel[ang]} value={angel[ang]}>
                      {ang}
                    </option>
                  ))}
                </select>
                </div>
                <br></br>

                <div className="input-group">
                <label htmlFor="private">Has the company received from Private Equity (in USD):</label>
                <select id="private" name="privateEquity" onChange={handleSelectChange} className="select-input" defaultValue="0">
                  {Object.keys(private_eq).map(pri => (
                    <option key={private_eq[pri]} value={private_eq[pri]}>
                      {pri}
                    </option>
                  ))}
                </select>
                </div>
                <br></br>
                <label >Has the company completed series A-F funding (in USD):</label>
                <br />
                <br />
                <div className='Rounds'>
                <div className="input-group Round">
                
                <label htmlFor="A">Series A?</label>
                <select id="A" name="seriesA" onChange={handleSelectChange} className="select-input" defaultValue="0">
                  {Object.keys(A).map(a => (
                    <option key={A[a]} value={A[a]}>
                      {a}
                    </option>
                  ))}
                </select>
                </div>

                

                <div className="input-group Round">
                <label htmlFor="B">Series B?</label>
                <select id="B" name="seriesB" onChange={handleSelectChange} className="select-input" defaultValue="0">
                  {Object.keys(B).map(b => (
                    <option key={B[b]} value={B[b]}>
                      {b}
                    </option>
                  ))}
                </select>
                </div>

                

                <div className="input-group Round">
                <label htmlFor="C">Series C?</label>
                <select id="C" name="seriesC" onChange={handleSelectChange} className="select-input" defaultValue="0">
                  {Object.keys(C).map(c => (
                    <option key={C[c]} value={C[c]}>
                      {c}
                    </option>
                  ))}
                </select>
                </div>

                

                <div className="input-group Round">
                <label htmlFor="D">Series D?</label>
                <select id="D" name="seriesD" onChange={handleSelectChange} className="select-input" defaultValue="0">
                  {Object.keys(D).map(d => (
                    <option key={D[d]} value={D[d]}>
                      {d}
                    </option>
                  ))}
                </select>
                </div>

                

                <div className="input-group Round">
                <label htmlFor="E">Series E?</label>
                <select id="E" name="seriesE" onChange={handleSelectChange} className="select-input" defaultValue="0">
                  {Object.keys(E).map(e => (
                    <option key={E[e]} value={E[e]}>
                      {e}
                    </option>
                  ))}
                </select>
                </div>

                

                <div className="input-group Round">
                <label htmlFor="F">Series F?</label>
                <select id="F" name="seriesF" onChange={handleSelectChange} className="select-input" defaultValue="0">
                  {Object.keys(F).map(f => (
                    <option key={F[f]} value={F[f]}>
                      {f}
                    </option>
                  ))}
                </select>
                </div>
                </div>
                <br></br>
                <div className="button">
                <button  type='submit'  className="submit-button">Submit</button>
        
                
                </div>
              </form>
              
        
              {predictionReceived && (
        <>
          {prediction === 0 && (
            <p ref={predictionRef} className="prediction-closed">
              Sorry! Your startup has a high chance of failure and getting closed. This model uses the principle of correlation matrix in which the total investments and rounds are the important aspects. So, if the startup gets more investment and performs well in the Series A-F rounds, it'll be a success.
            </p>
          )}
          {prediction === 1 && (
            <p ref={predictionRef} className="prediction-success">
              Congratulations! It will operate and has a high chance of success. The total investment and the perfomance of the startup in Series A-F rounds is very good. The industry and the country of the startup is also entrepreneur-friendly. So, go ahead.
            </p>
          )}
          {prediction === 2 && (
            <p ref={predictionRef} className="prediction-acquired">
              It has a high chance of getting acquired by other companies. The interest of seed, venture, angel and debt financing investors show a very good chance that the starup will operate and will be acquired by some bigger companies. So, it is uncertain but don't lose the hope.
            </p>
          )}
        </>
      )}
    </div>
  );
};

        
export default SuccessPre