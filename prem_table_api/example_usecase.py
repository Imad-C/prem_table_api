'''
This script creates a visualisation based on the api.
Please have the api running on a local server.
'''

import requests

TEAM = "Manchester City" # edit to look at a different team 

single_team = requests.get("http://localhost:5000/teams/Liverpool")