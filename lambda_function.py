
try:
    import json
    from selenium.webdriver import Chrome
    from selenium.webdriver.chrome.options import Options
    import os
    import shutil
    import uuid
    import boto3
    from datetime import datetime
    import datetime

    print("All Modules are ok ...")

except Exception as e:

    print("Error in Imports ")

class WebDriver(object):

    def __init__(self):
        self.options = Options()

        self.options.binary_location = '/opt/headless-chromium'
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--start-fullscreen')
        self.options.add_argument('--single-process')
        self.options.add_argument('--disable-dev-shm-usage')

    def get(self):
        driver = Chrome('/opt/chromedriver', options=self.options)
        return driver

instance_ = WebDriver()
driver = instance_.get()

season = '20202021'

# Get 5v5 stats for whole season
driver.get(f'https://www.naturalstattrick.com/teamtable.php?fromseason={season}&thruseason={season}&stype=2&sit=sva&score=all&rate=y&team=all&loc=B&gpf=410&fd=&td=')
teams = {}
for i in range(1,33):
    team = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child(2)').text
    xG = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child(23)').text
    xGA = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child(24)').text
    savePercentage = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child(43)').text
    teams[team] = [xG, xGA, savePercentage]

# Get Power Play stats for full season
driver.get(f'https://www.naturalstattrick.com/teamtable.php?fromseason={season}&thruseason={season}&stype=2&sit=pp&score=all&rate=n&team=all&loc=B&gpf=410&fd=&td=')
for i in range(1,33):
    team = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child(2)').text
    powerPlayGoals = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child(20)').text
    games = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child(3)').text
    powerPlayGoalsPerGame = float(powerPlayGoals)/float(games)
    teams[team].append(powerPlayGoalsPerGame)

# Get Penalty kill stats for full season
driver.get(f'https://www.naturalstattrick.com/teamtable.php?fromseason={season}&thruseason={season}&stype=2&sit=pk&score=all&rate=n&team=all&loc=B&gpf=410&fd=&td=')
for i in range(1,33):
    team = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child(2)').text
    expectedPKGA = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child(24)').text
    games = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child(3)').text
    xPKGAPerGame = float(expectedPKGA)/float(games)
    pkSavePercentage = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child(43)').text
    teams[team].extend([xPKGAPerGame, pkSavePercentage])

recent = ""
#MARK TRUE IF PLAYOFFS
isPlayoffs = True

if(isPlayoffs):
    seasonType = 3
    colsRemoved = 4
    numTeams = 17

    # Get 5v5 stats for playoffs
    driver.get(f'https://www.naturalstattrick.com/teamtable.php?fromseason={season}&thruseason={season}&stype={seasonType}&sit=sva&score=all&rate=y&team=all&loc=B&gpf=10&fd=&td=')
    for i in range(1,numTeams):
        games = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child(3)').text
        team = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child(2)').text
        if int(games) < 7:
            print(team, 'have not played enough playoff games to be accurate')
            continue
        xG = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child({23 - colsRemoved})').text
        xGA = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child({24 - colsRemoved})').text
        savePercentage = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child({43 - colsRemoved})').text
        teams[team].extend([xG, xGA, savePercentage])

    # Get Power Play stats for playoffs
    driver.get(f'https://www.naturalstattrick.com/teamtable.php?fromseason={season}&thruseason={season}&stype={seasonType}&sit=pp&score=all&rate=n&team=all&loc=B&gpf=10&fd=&td=')
    for i in range(1,numTeams):
        games = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child(3)').text
        if int(games) < 7:
            continue
        team = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child(2)').text
        powerPlayGoals = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child({20 - colsRemoved})').text
        powerPlayGoalsPerGame = float(powerPlayGoals)/float(games)
        teams[team].append(powerPlayGoalsPerGame)

    # Get Penalty kill stats for playoffs
    driver.get(f'https://www.naturalstattrick.com/teamtable.php?fromseason={season}&thruseason={season}&stype={seasonType}&sit=pk&score=all&rate=n&team=all&loc=B&gpf=10&fd=&td=')
    for i in range(1,numTeams):
        games = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child(3)').text
        if int(games) < 7:
            continue
        team = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child(2)').text
        expectedPKGA = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child({21 - colsRemoved})').text
        xPKGAPerGame = float(expectedPKGA)/float(games)
        pkSavePercentage = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child({43 - colsRemoved})').text
        teams[team].extend([xPKGAPerGame, pkSavePercentage])

seasonType = 2
colsRemoved = 0
numTeams = 33

# Get 5v5 stats for last 10 of regular season
driver.get(f'https://www.naturalstattrick.com/teamtable.php?fromseason={season}&thruseason={season}&stype={seasonType}&sit=sva&score=all&rate=y&team=all&loc=B&gpf=10&fd=&td=')
for i in range(1,numTeams):
    team = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child(2)').text
    if len(teams[team]) > 6:
        continue
    xG = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child({23 - colsRemoved})').text
    xGA = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child({24 - colsRemoved})').text
    savePercentage = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child({43 - colsRemoved})').text
    teams[team].extend([xG, xGA, savePercentage])

# Get Power Play stats for last 10 of regular season
driver.get(f'https://www.naturalstattrick.com/teamtable.php?fromseason={season}&thruseason={season}&stype={seasonType}&sit=pp&score=all&rate=n&team=all&loc=B&gpf=10&fd=&td=')
for i in range(1,numTeams):
    team = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child(2)').text
    if len(teams[team]) > 9:
        continue
    powerPlayGoals = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child({20 - colsRemoved})').text
    games = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child(3)').text
    powerPlayGoalsPerGame = float(powerPlayGoals)/float(games)
    teams[team].append(powerPlayGoalsPerGame)

# Get Penalty kill stats for last 10 of regular season
driver.get(f'https://www.naturalstattrick.com/teamtable.php?fromseason={season}&thruseason={season}&stype={seasonType}&sit=pk&score=all&rate=n&team=all&loc=B&gpf=10&fd=&td=')
for i in range(1,numTeams):
    team = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child(2)').text
    if len(teams[team]) > 10:
        continue
    expectedPKGA = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child({21 - colsRemoved})').text
    games = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child(3)').text
    xPKGAPerGame = float(expectedPKGA)/float(games)
    pkSavePercentage = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child({43 - colsRemoved})').text
    teams[team].extend([xPKGAPerGame, pkSavePercentage])

    
def lambda_handler(event, context):
    dynamodb = boto3.client('dynamodb')
    totalxGF = 0.0
    totalxGA = 0.0
    totalSVP = 0.0
    totalppGF = 0.0
    totalxPKGA = 0.0
    totalPKSVP = 0.0
    for team, stats in teams.items():
        # Weight stats according to recent games (last 10 reg season or playoffs if applicable)
        weightedxGF = ((2 * float(stats[0]) + float(stats[6]))/3)
        weightedxGA = ((2 * float(stats[1]) + float(stats[7]))/3)
        weightedSVP = ((2 * float(stats[2]) + float(stats[8]))/3)
        weightedppGF = ((2 * float(stats[3]) + float(stats[9]))/3)
        weightedxPKGA = ((2 * float(stats[4]) + float(stats[10]))/3)
        weightedPKSVP = ((2 * float(stats[5]) + float(stats[11]))/3)

        #Keep track of totals to calculate league averages (Used in equation to calculate expected goals)
        totalxGF += weightedxGF
        totalxGA += weightedxGA
        totalSVP += weightedSVP
        totalppGF += weightedppGF
        totalxPKGA += weightedxPKGA
        totalPKSVP += weightedPKSVP

        # Put into dynamo
        dynamodb.put_item(TableName='current_stats', Item={'team':{'S':team},'evenStrengthxGF':{'N':str(weightedxGF)}, 'evenStrengthxGA':{'N':str(weightedxGA)}, 'evenStrengthSVP':{'N':str(weightedSVP)}, 'powerPlayGF':{'N':str(weightedppGF)}, 'penaltyKillxGA':{'N':str(weightedxPKGA)}, 'penaltyKillSVP':{'N':str(weightedPKSVP)}})
    dynamodb.put_item(TableName='current_stats', Item={'team':{'S':'League Average'},'evenStrengthxGF':{'N':str(totalxGF/32)}, 'evenStrengthxGA':{'N':str(totalxGA/32)}, 'evenStrengthSVP':{'N':str(totalSVP/32)}, 'powerPlayGF':{'N':str(totalppGF/32)}, 'penaltyKillxGA':{'N':str(totalxPKGA/32)}, 'penaltyKillSVP':{'N':str(totalPKSVP/32)}})
