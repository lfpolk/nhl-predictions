import React, { useEffect, useState, Fragment, useContext } from 'react';
import { TeamsContext } from "../context/TeamsContext";
import { predictGame } from '../components/predictGame'

const Schedule = () => {
    const teams = useContext(TeamsContext)
    var dateObj = new Date();
    var month = dateObj.getMonth() + 1; //months from 1-12
    var day = dateObj.getDate();
    var year = dateObj.getFullYear();
    const [scores, setScores] = useState([]);
    const [date, setDate] = useState(year + "-" + month + "-" + day);

    const getScores = async () => {

        try {

            console.log("new Date: " + date);
            const response = await fetch("https://statsapi.web.nhl.com/api/v1/schedule//?date=" + date);
            const jsonData = await response.json();
            var games = jsonData.dates[0].games;
            
            games.forEach(addPrediction)

            setScores(games);
            
        } catch (err){
            console.log(err);
        }
    }

    function addPrediction(item) {
        let result = predictGame(teams[item.teams.home.team.id], teams[item.teams.away.team.id], teams[0])
        item.teams.home['winPercentage'] = result.homeWP;
        item.teams.home['xG'] = result.homeG;
        item.teams.away['winPercentage'] = result.awayWP;
        item.teams.away['xG'] = result.awayG;
    }

    function addDay() {
        var a = date.split(/[^0-9]/);
        var d = new Date (a[0],a[1]-1,a[2]);
        let temp = new Date(d);
        temp.setDate(temp.getDate() + 1);
        setDate(temp.getFullYear() + "-" + (temp.getMonth() + 1) + "-" + temp.getDate());   
    }

    function subtractDay() {
        var a = date.split(/[^0-9]/);
        var d = new Date (a[0],a[1]-1,a[2]);
        let temp = new Date(d);
        temp.setDate(temp.getDate() - 1);
        setDate(temp.getFullYear() + "-" + (temp.getMonth() + 1) + "-" + temp.getDate());
    }



    useEffect(() => {
        getScores();
    }, [date])


    let scoresToRender;
    if (scores) {
      scoresToRender = scores.map(score => {
        return <div class="score">
            <div></div>
        <div class="logoDiv">
        <img src={"https://www-league.nhlstatic.com/images/logos/teams-current-primary-light/" + score.teams.home.team.id + ".svg"} alt={score.teams.home.team.name} class="teamLogo"></img>
        </div>
        <div class="scoreDetails">
            <h2>Expected</h2>
            <div class="scoreDetailsRow">
                <h2>{score.teams.home.xG}</h2> 
                <h4>{score.teams.home.winPercentage > 5 && <div>{score.teams.home.team.name} {Math.round(score.teams.home.winPercentage * 100)/10}%</div>}</h4>
                <h4>{score.teams.home.winPercentage <= 5 && <div>{score.teams.away.team.name} {Math.round(score.teams.away.winPercentage * 100)/10}%</div>}</h4>
                <h2>{score.teams.away.xG}</h2> 
            </div>
            <h2>Result</h2>
            <div class="scoreDetailsRow">
                <h1>{score.teams.home.score}</h1>
                <h4>{score.status.detailedState}</h4>
                <h1>{score.teams.away.score}</h1>
            </div>
        </div>
        <div class="logoDiv">
        <img src={"https://www-league.nhlstatic.com/images/logos/teams-current-primary-light/" + score.teams.away.team.id + ".svg"} alt={score.teams.away.team.name} class="teamLogo"></img>
        </div>
        <div></div>
        </div>
      });
    }



return (
    <Fragment>
        <div class="scheduleMarker">
            Schedule
        </div>
        <div class="date">
        <h1>{date}</h1>
        </div>
    <div class="scores">{scoresToRender}</div>
    <div class="bottomButtons"><button class="bottomButton" onClick={() => subtractDay()}>Previous Day</button> <button class="bottomButton" onClick={() => addDay()}>Next Day</button></div>
    </Fragment>
    );
};

export default Schedule;