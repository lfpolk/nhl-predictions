import React, {Fragment, useState} from 'react';
import './App.css';
import {BrowserRouter as Router, Switch, Route} from "react-router-dom";

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
      <Router>
      <Header />

        <div className="container">
          <Switch>
            <TeamsContext.Provider value={teams}>
              <Route exact path="/" >
                <Predictor />
              </Route>

              <Route exact path="/schedule" >
                <Schedule />
              </Route>

              <Route exact path="/rankings" >
                <Rankings />
              </Route>
            </TeamsContext.Provider>
          </Switch>
        </div>
      </Router>
      </div>}
    </Fragment>
  );
}

export default App;