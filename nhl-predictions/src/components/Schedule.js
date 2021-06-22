import React, { useEffect, useState, Fragment} from 'react';

const Schedule = () => {
    var dateObj = new Date();
    var month = dateObj.getMonth() + 1; //months from 1-12
    var day = dateObj.getDate();
    var year = dateObj.getFullYear();
    const [scores, setScores] = useState([]);
    const [salami, setSalami] = useState([]);
    const [date, setDate] = useState(year + "-" + month + "-" + day);

    const getScores = async () => {

        try {

            console.log("new Date: " + date);
            const response = await fetch("https://statsapi.web.nhl.com/api/v1/schedule//?date=" + date);
            const jsonData = await response.json();
            var games = jsonData.dates[0].games;
            
            setScores(games);

            var homeScore = 0;
            var awayScore = 0;

            for (var i = 0; i < games.length; i++){
                homeScore += games[i].teams.home.score;
                awayScore += games[i].teams.away.score;
            }

            setSalami([homeScore, awayScore])
            
        } catch (err){
            console.log(err);
        }
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
        <h1><img src={"https://www-league.nhlstatic.com/images/logos/teams-current-primary-light/" + score.teams.home.team.id + ".svg"} alt={score.teams.home.team.name} class="teamLogo"></img> {score.teams.home.score}</h1><br></br>
        {score.status.detailedState}
        <h1><img src={"https://www-league.nhlstatic.com/images/logos/teams-current-primary-light/" + score.teams.away.team.id + ".svg"} alt={score.teams.away.team.name} class="teamLogo"></img> {score.teams.away.score}</h1>
        </div>
      });
    }

return (
    <Fragment>
        <div class="scheduleMarker">
            Schedule
        </div>
        <div class="score">
    <h1 class ="date">{date}</h1>
        </div>
    <div class="scores">{scoresToRender}</div>
    <div class="bottomButtons"><button class="bottomButton" onClick={() => subtractDay()}>Previous Day</button> <button class="bottomButton" onClick={() => addDay()}>Next Day</button></div>
    </Fragment>
    );
};

export default Schedule;