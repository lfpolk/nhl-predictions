export function predictGame(home, away, avg) {

    var homeESG = 0
    var homePPG = 0
    var homeG = 0
    var homeWP = 0
    var awayESG = 0
    var awayPPG = 0
    var awayG = 0
    var awayWP =  0


    //homeESG = Math.round(((home.evenStrengthxGF/2 + away.evenStrengthxGA/2) + (home.evenStrengthxGF - avg.evenStrengthxGF) + (away.evenStrengthxGA - avg.evenStrengthxGA))*10)/10
    //awayESG = Math.round(((away.evenStrengthxGF/2 + home.evenStrengthxGA/2) + (away.evenStrengthxGF - avg.evenStrengthxGF) + (home.evenStrengthxGA - avg.evenStrengthxGA))*10)/10

    homeESG = Math.round((((home.evenStrengthxGF / avg.evenStrengthxGF) * away.evenStrengthxGA/2) + avg.evenStrengthxGF/2) * (1 + (1 - away.evenStrengthSVP/100)) * 93)/100
    awayESG = Math.round((((away.evenStrengthxGF / avg.evenStrengthxGF) * home.evenStrengthxGA/2) + avg.evenStrengthxGF/2) * (1 + (1 - home.evenStrengthSVP/100)) * 87)/100
    homePPG = Math.round((((home.powerPlayGF / avg.powerPlayGF) * away.penaltyKillxGA/2) + avg.powerPlayGF/2) * (1 + (1 - away.penaltyKillSVP/100)) * 103)/100
    awayPPG = Math.round((((away.powerPlayGF / avg.powerPlayGF) * home.penaltyKillxGA/2) + avg.powerPlayGF/2) * (1 + (1 - home.penaltyKillSVP/100)) * 97)/100
    homeG = Math.round((homeESG + homePPG)*100)/100
    awayG = Math.round((awayESG + awayPPG)*100)/100

    //Calculate pythagenpat exponent
    var pythagenpat = (homeG + awayG) ** .458

    //Calculate win percentage
    var homeWP = Math.round((homeG ** pythagenpat / (awayG ** pythagenpat + homeG ** pythagenpat))*1000)/100
    var awayWP = Math.round((10 - homeWP)* 100)/100
    
    var result = {
        homeESG:  homeESG,
        homePPG: homePPG,
        homeG: homeG,
        homeWP: homeWP,
        awayESG:  awayESG,
        awayPPG: awayPPG,
        awayG: awayG,
        awayWP: awayWP
      };
      // Return it
      return result;
}