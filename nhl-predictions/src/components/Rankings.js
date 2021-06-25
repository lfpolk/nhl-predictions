import React, {Fragment, useContext} from "react";
import { TeamsContext } from "../context/TeamsContext";
import { predictGame } from '../components/predictGame';

const Rankings = () => {

    const teams = useContext(TeamsContext)
    var winP = 0
    let teamList = []
    
    for (const [key, value] of Object.entries(teams)) {
        teams[key]['winP'] = predictGame(teams[key], teams[0], teams[0]).homeWP
        if(key!=0){
            teamList.push([teams[key].winP, teams[key].team, key])
        }
      }
    
      function compare(a, b) {
        // Use toUpperCase() to ignore character casing
        const teamA = a[0];
        const teamB = b[0];
      
        let comparison = 0;
        if (teamA > teamB) {
          comparison = -1;
        } else if (teamA < teamB) {
          comparison = 1;
        }
        return comparison;
      }
      
      teamList.sort(compare);

    
console.log("https://www-league.nhlstatic.com/images/logos/teams-current-primary-light/" + teamList[0][2] + ".svg")

let rankingsList;
if (teamList) {
    rankingsList = teamList.map(team => {
    return <tr class="selection">
        {<tr>
            <td>{teamList.indexOf(team)+1}</td>
            <td> <img class="tableImg" src={"https://www-league.nhlstatic.com/images/logos/teams-current-primary-light/" + team[2] + ".svg"} /></td>
            <td>{team[1]}</td>
        </tr>
        }
    </tr>
  });
}

return (
    <Fragment>
        <div class="rankingsMarker">
            rankings
        </div>
        <div class="rankingsTable">
            <table>
        <tr><th></th><th></th><th></th></tr>
            {rankingsList}
            </table>
        </div>
    </Fragment>
    );
};

export default Rankings;