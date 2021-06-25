import requests
import json

res = requests.get("https://statsapi.web.nhl.com/api/v1/teams")
teamList = res.json()['teams']

teamIDs = {}

for team in teamList:
    if (team['name'] != 'Seattle Kraken'):
        teamIDs[team['name']] = team['id']

print(teamIDs)
