import React, {Fragment, useState, useContext} from "react";
import { PieChart } from 'react-minimal-pie-chart';
import { TeamsContext } from "../context/TeamsContext";
import { predictGame } from '../components/predictGame'

const Predictor = () => {
const [homeTeam, setHomeTeam] = useState(1);
const [awayTeam, setAwayTeam] = useState(2);
const teams = useContext(TeamsContext)
const [prediction, setPrediction] = useState(predictGame(teams[1],teams[2], teams[0]));

let homeTeamList;
if (teams) {
  homeTeamList = Object.keys(teams).map(function(key){
    return <div class="selection">
        {key > 0 && <div>
            <label>
            <input 
                type="radio"
                checked ={homeTeam == key}
                value={homeTeam}
                onChange={(e)=>{
                    setHomeTeam(key)
                    setPrediction(predictGame(teams[key], teams[awayTeam], teams[0]))
                    }}/>
                <img src={"https://www-league.nhlstatic.com/images/logos/teams-current-primary-light/" + key + ".svg"}/>
            </label>
        </div>
        }
    </div>
  });
}

let awayTeamList;
if (teams) {
  awayTeamList = Object.keys(teams).map(function(key){
    return <div class="selection">
        {key > 0 && <div>
            <label class="selectorLabel">
            <input 
                type="radio"
                checked ={awayTeam == key}
                value={awayTeam}
                onChange={(e)=>{
                    setAwayTeam(key)
                    setPrediction(predictGame(teams[homeTeam], teams[key], teams[0]))
                    }}/>
                <img src={"https://www-league.nhlstatic.com/images/logos/teams-current-primary-light/" + key + ".svg"}/>
            </label>
        </div>
        }
    </div>
  });
}

return (
    <Fragment>
        {teams && <div>
        <div class="predictorMarker">
            predictor
        </div>
        <div class="predictor">
            <div class="selector">
                <h1>Home</h1>
                <div class="selections">
                    {homeTeamList}
                </div>
            </div>
            <div class="predictorStats">
                    <br></br>
                    <br></br>
                    <br></br>
                    <br></br>
                <div class="scoreDetailsRow">
                    <h4>{teams[homeTeam].team}</h4>
                    <h1>Team</h1>
                    <h4 class="away">{teams[awayTeam].team}</h4>
                </div>
                <div class="scoreDetailsRow">
                    <h2>{prediction.homeESG}</h2>
                    <h4>Expected Even Strength Goals</h4>
                    <h2 class="away">{prediction.awayESG}</h2>
                </div>
                <div class="scoreDetailsRow">
                    <h2>{prediction.homePPG}</h2>
                    <h4>Expected Power Play Goals</h4>
                    <h2 class="away">{prediction.awayPPG}</h2>
                </div>
                <div class="scoreDetailsRow">
                    <h2>{prediction.homeG}</h2>
                    <h4>Expected Score</h4>
                    <h2 class="away">{prediction.awayG}</h2>
                </div>
                <div class="predictorChart">
                <PieChart animate reveal center={[100, 100]} viewBoxSize={[200, 200]} lineWidth="25" paddingAngle="1" totalValue={10} lengthAngle={-180} startAngle={0} labelPosition={120} labelStyle={{fontSize: 14}} label={({ dataEntry }) => `${Math.round(dataEntry.percentage * 10)/10} %`}

                data={[
                    { title: teams[homeTeam].team, value: prediction.awayWP, color: '#666' },
                    { title: "", value: prediction.homeWP, color: '#000000' }
                ]}
                /></div>

            </div>
            <div class="selector">
                <h1 class="away">Away</h1>
                <div class="selections">
                    {awayTeamList}
                </div>
            </div>
        </div>
        </div>
}
    </Fragment>

    );
};

export default Predictor;