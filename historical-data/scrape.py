from selenium import webdriver
import datetime
import csv

PATH = '/Users/larsonpolk/Downloads/chromedriver'


# TODO 
#Set limit so server can handle scrape
MAX_DAYS = 8

driver = webdriver.Chrome(PATH)

seasons = []
seasons.append({"year": "20132014", "startDate": datetime.date(2013, 10, 1), "end_date": datetime.date(2014, 4, 16), "numTeams": 30})
seasons.append({"year": "20142015", "startDate": datetime.date(2014, 10, 8), "end_date": datetime.date(2015, 4, 15), "numTeams": 30})
seasons.append({"year": "20152016", "startDate": datetime.date(2015, 10, 7), "end_date": datetime.date(2016, 4, 13), "numTeams": 30})
seasons.append({"year": "20162017", "startDate": datetime.date(2016, 10, 12), "end_date": datetime.date(2017, 4, 12), "numTeams": 30})
seasons.append({"year": "20172018", "startDate": datetime.date(2017, 10, 4), "end_date": datetime.date(2018, 4, 11), "numTeams": 31})
seasons.append({"year": "20182019", "startDate": datetime.date(2018, 10, 3), "end_date": datetime.date(2019, 4, 10), "numTeams": 31})
seasons.append({"year": "20192020", "startDate": datetime.date(2019, 10, 2), "end_date": datetime.date(2020, 8, 1), "numTeams": 31})
seasons.append({"year": "20202021", "startDate": datetime.date(2021, 1, 1), "end_date": datetime.date(2021, 5, 15), "numTeams": 31})

delta = datetime.timedelta(days=1)

currentURL = ""

dailyStats = []

for season in seasons:
    print(season)
    date = season['startDate'] + delta * 30
    while date <= season['end_date']:
        teams = {}
        print(date)

        currentURL = f'https://www.naturalstattrick.com/teamtable.php?fromseason={season["year"]}&thruseason={season["year"]}&stype=2&sit=sva&score=all&rate=y&team=all&loc=B&gpf=410&fd={season["startDate"]}&td={date}'
        driver.get(currentURL)
        for i in range(1,season["numTeams"] + 1):
            # Get 5v5 stats for whole season
            team = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child(2)').text
            xESGF = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child(23)').text
            xESGA = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child(24)').text
            saveP = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child(43)').text
            teams[team] = [xESGF, xESGA, saveP]
        

        # Get Power Play stats for full season
        currentURL = f'https://www.naturalstattrick.com/teamtable.php?fromseason={season["year"]}&thruseason={season["year"]}&stype=2&sit=pp&score=all&rate=n&team=all&loc=B&gpf=410&fd={season["startDate"]}&td={date}'
        driver.get(currentURL)
        for i in range(1,season["numTeams"] + 1):
            team = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child(2)').text
            powerPlayGoals = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child(20)').text
            games = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child(3)').text
            xPPGF = float(powerPlayGoals)/float(games)
            teams[team].append(xPPGF)

        # Get Penalty kill stats for full season
        currentURL = f'https://www.naturalstattrick.com/teamtable.php?fromseason={season["year"]}&thruseason={season["year"]}&stype=2&sit=pk&score=all&rate=n&team=all&loc=B&gpf=410&fd={season["startDate"]}&td={date}'
        driver.get(currentURL)
        for i in range(1,season["numTeams"] + 1):
            team = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child(2)').text
            expectedPKGA = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child(24)').text
            games = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child(3)').text
            xPKGA = float(expectedPKGA)/float(games)
            PKSVP = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child(43)').text
            teams[team].extend([xPKGA, PKSVP])

        recent = ""
        #MARK TRUE IF PLAYOFFS
        isPlayoffs = False

        if (isPlayoffs):
            colsRemoved = 4
            seasonType = 3
        else:
            colsRemoved = 0
            seasonType = 2

        # Get 5v5 stats for last 10 of regular season
        currentURL = f'https://www.naturalstattrick.com/teamtable.php?fromseason={season["year"]}&thruseason={season["year"]}&stype={seasonType}&sit=sva&score=all&rate=y&team=all&loc=B&gpf=10&fd={season["startDate"]}&td={date}'
        driver.get(currentURL)
        for i in range(1,season["numTeams"] + 1):
            team = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child(2)').text
            if len(teams[team]) > 6:
                continue
            xESGFRecent = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child({23 - colsRemoved})').text
            xESGARecent = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child({24 - colsRemoved})').text
            savePRecent = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child({43 - colsRemoved})').text
            teams[team].extend([xESGFRecent, xESGARecent, savePRecent])

        # Get Power Play stats for last 10 of regular season
        currentURL = f'https://www.naturalstattrick.com/teamtable.php?fromseason={season["year"]}&thruseason={season["year"]}&stype={seasonType}&sit=pp&score=all&rate=n&team=all&loc=B&gpf=10&fd={season["startDate"]}&td={date}'
        driver.get(currentURL)
        for i in range(1,season["numTeams"] + 1):
            team = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child(2)').text
            if len(teams[team]) > 9:
                continue
            powerPlayGoals = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child({20 - colsRemoved})').text
            games = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child(3)').text
            xPPGFRecent = float(powerPlayGoals)/float(games)
            teams[team].append(xPPGFRecent)

        # Get Penalty kill stats for last 10 of regular season
        currentURL = f'https://www.naturalstattrick.com/teamtable.php?fromseason={season["year"]}&thruseason={season["year"]}&stype={seasonType}&sit=pk&score=all&rate=n&team=all&loc=B&gpf=10&fd={season["startDate"]}&td={date}'
        driver.get(currentURL)
        for i in range(1,season["numTeams"] + 1):
            team = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child(2)').text
            if len(teams[team]) > 10:
                continue
            expectedPKGA = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child({21 - colsRemoved})').text
            games = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child(3)').text
            xPKGARecent = float(expectedPKGA)/float(games)
            PKSVPRecent = driver.find_element_by_css_selector(f'#teams > tbody > tr:nth-child({i}) > td:nth-child({43 - colsRemoved})').text
            teams[team].extend([xPKGARecent, PKSVPRecent]) 



        for team, stats in teams.items():
            # Weight stats according to recent games (last 10 reg season or playoffs if applicable)
            """
            weightedxGF = ((2 * float(stats[0]) + float(stats[6]))/3)
            weightedxGA = ((2 * float(stats[1]) + float(stats[7]))/3)
            weightedSVP = ((2 * float(stats[2]) + float(stats[8]))/3)
            weightedppGF = ((2 * float(stats[3]) + float(stats[9]))/3)
            weightedxPKGA = ((2 * float(stats[4]) + float(stats[10]))/3)
            weightedPKSVP = ((2 * float(stats[5]) + float(stats[11]))/3)
            """
            dailyStats.append([date + delta, team, stats[0], stats[1], stats[2], stats[3], stats[4], stats[5], stats[6], stats[7], stats[8], stats[9], stats[10], stats[11]])

        date += delta

fields = ['date', 'team', 'xESGF', 'xESGA', 'saveP', 'xPPGF', 'xPKGA', 'PKSVP', 'xESGFRecent', 'xESGARecent', 'savePRecent', 'xPPGFRecent', 'xPKGARecent', 'PKSVPRecent']

filename = "daily_stats.csv"
        
with open(filename, 'w') as csvfile:
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile)
                
    # writing the fields 
    csvwriter.writerow(fields)
                
    # writing the data rows 
    csvwriter.writerows(dailyStats)
"""
fields = ['date', 'team', 'xESGF', 'xESGA', 'saveP', 'xPPGF', 'xPKGA', 'PKSVP']

filename = "daily_stats.csv"

with open(filename, 'w') as csvfile:
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile) 
        
    # writing the fields 
    csvwriter.writerow(fields) 
        
    # writing the data rows 
    csvwriter.writerows(dailyStats)
"""
driver.quit()

