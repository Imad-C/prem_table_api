'''
This script creates a visualisation based on the api.
Please have the api running on a local server.
'''

import matplotlib.pyplot as plt
import numpy as np
import requests


def _trim_non_pos(dict_: dict) -> dict:
    '''Takes a dictionary and only returns the 'Pos' key.
    '''
    for k in dict_.keys():
        dict_[k] = dict_[k]['Pos']
    
    return dict_


def _fill_blank_season(dict_: dict, all_seasons: list) -> dict:
    '''Ensures there are a total number of seasons within a dict. 
    If a team is relegated, the 'blank' season is filled with 21
    (i.e. out of the league).
    '''
    dict_keys = list(dict_.keys())
    difference = list(set(all_seasons) - set(dict_keys))
    
    for season in difference:
        dict_[season] = 21
    
    return dict_
    

def get_team_dict(team_name: str) -> dict:
    '''Gets the team data from the api, and acts as a wrapper for the
    above processes.
    '''
    team_data = requests.get(
        f"http://localhost:5000/teams/{team_name}"
        ).json()['data']
    
    all_seasons = requests.get("http://localhost:5000/seasons").json()['data']
    
    team_data = _trim_non_pos(team_data)
    team_data = _fill_blank_season(team_data, all_seasons)
    
    return team_data


if __name__ == "__main__":

    TEAMS = ["Manchester City", "Manchester United"] # Update teams here
    
    fig, ax = plt.subplots(figsize=(12, 5))
    
    # Plotting all teams of interest
    for team in TEAMS:
        team_data = get_team_dict(team)
        
        ax.plot(*zip(*sorted(team_data.items())))
        ax.scatter(*zip(*sorted(team_data.items())), label=team)
        
    # Adding 'relegation zone' 
    all_seasons = requests.get("http://localhost:5000/seasons").json()['data']
    relegation_zone = [21] * len(all_seasons)
    ax.scatter(all_seasons, relegation_zone, color="black", label="Relegated")
    
    # Styling and formatting plot
    ax.invert_yaxis()
    ax.legend(
        loc="upper left",
        ncol=len(TEAMS) + 1,
        bbox_to_anchor=(0, 1.1)
        )
    plt.yticks(np.arange(1, 21, step=1))
    plt.xticks(rotation = 90)
    
    # save and show
    plt.savefig("examples/example_usecase.png", bbox_inches="tight")
    plt.show()
