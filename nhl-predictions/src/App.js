import React, {Fragment, useState} from 'react';
import './App.css';
import {HashRouter as Router, Link, Route} from "react-router-dom";

// Components

import Schedule from "./components/Schedule";
import Predictor from "./components/Predictor";
import Rankings from "./components/Rankings";
import Header from "./components/Header";
import { TeamsContext } from './context/TeamsContext';


function App() {

  const getStats = async () => {

    try {

        const response = await fetch("https://kxbiyq2zxl.execute-api.us-east-2.amazonaws.com/v1/current-stats");
        const data = await response.json();
        const teamStats = data.teams
        let teamMap = {};
        for (var i = 0; i < teamStats.length; i++) {
          teamMap[teamStats[i].id] =  {team: teamStats[i].team, evenStrengthxGF: teamStats[i].evenStrengthxGF, evenStrengthxGA: teamStats[i].evenStrengthxGA, evenStrengthSVP: teamStats[i].evenStrengthSVP, penaltyKillSVP: teamStats[i].penaltyKillSVP, penaltyKillxGA: teamStats[i].penaltyKillxGA, powerPlayGF: teamStats[i].powerPlayGF}
      }

        //teamStats.forEach(console.log())

        setTeams(teamMap);
        
    } catch (err){
        console.log(err);
    }
}


const [teams, setTeams] = useState(["empty"])
if (teams == "empty"){
  getStats()
}


  return (
    <Fragment>
      {teams != "empty" && <div>
      <Router  hashType='noslash'>
      <Header />

        <div className="container">
          
            <TeamsContext.Provider value={teams}>
              <Route exact path="/" component={Predictor} />

              <Route exact path="/schedule" component={Schedule} />


              <Route exact path="/rankings" component={Rankings} />

            </TeamsContext.Provider>
         
        </div>
      </Router>
      </div>}
    </Fragment>
  );
}

export default App;