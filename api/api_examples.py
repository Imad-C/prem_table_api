'''
This script contains examples of how the api can be called 
using python's request library.
'''

import requests

url = "http://localhost:5000/"

''' General ''' 
# Hello World
test = requests.get(url)
print(test.text)

''' Teams '''
# All teams
teams = requests.get(url + 'teams')
print(teams.text)
check = teams.json()['data']

# Single team
single_team = requests.get(url + 'teams/Liverpool')
print(single_team.text)
check = single_team.json()['data']

''' Seasons ''' 
# All Seasons
season = requests.get(url + 'seasons')
print(season.text)
check = teams.json()['data']

# Single season
single_season = requests.get(url + 'seasons/2016-17')
print(single_season.text)
check = single_season.json()['data']

''' Custom '''
# Filter with both Teams and Seasons
query = (
    "team=Arsenal&team=Aston Villa&"
    "season=2014-15&season=2015-16"
    )
custom_query = requests.get(url + 'query?' + query)
print(custom_query.text)
check = custom_query.json()['data']
check = custom_query.json()['data']['Arsenal']['2014-15'] # index into json

# Error example
query = (
    "team=Manchester City&team=FakeTeam&" # no team called 'FakeTeam'
    "season=2012-13&season=2013-14"
    )
error_query = requests.get(url + 'query?' + query)
print(error_query.text)
check = error_query.json()['message']
