from flask import abort
from json import loads
import pandas as pd


def load_data() -> pd.DataFrame:
    '''Loads in dataset, usually would connect to a db here
    '''
    return pd.read_csv("data/df_total.csv")


def abort_non_existant(
        user_data: list,
        data_col: list,
        ) -> None:
    '''Aborts api call if data is not found in dataset. Output handled 
    with Flask error handler
    '''
    
    for item in user_data:
        if item not in data_col:
            message = f"Could not find '{item}' in data." 
            abort(400, message)


def get_team_all_seasons(
        data: pd.DataFrame,
        team: str
        ) -> dict:
    '''Gets all season results for a single team.
    '''
    # checking team is valid
    abort_non_existant([team], data['Team'].unique())  
    
    # filter and transpose
    data = data[data["Team"] == team].drop(columns="Team")
    data = data.set_index("Season").T
    
    # to json
    result = data.to_json(orient="columns")
    return loads(result), 200


def get_season_all_teams(
        data: pd.DataFrame,
        season: str
        ) -> dict:
    '''Gets all team results for a single season.
    '''
    # clean input, check season is valid
    season = season.replace('-', '/')
    abort_non_existant([season], data['Season'].unique())  
    
    # filter, and transpose
    data = data[data['Season']==season].drop(columns='Season')
    data = data.set_index("Team").T
    
    # to json
    result = data.to_json(orient="columns")
    return loads(result), 200


def get_filtered(
        data: pd.DataFrame,
        filter_dict: dict
        ) -> dict:
    '''Filters the data based on season and team values. If empty filter
    dict is passed, then defualts to all data.

    Parameters
    ----------
    data : pd.DataFrame
        Total dataset.
    filter_dict : dict
        Filter values for season and team keys, with list values.

    Returns
    -------
    dict
        JSON output of team data for specified filters.

    '''
    response = {}
    
    # filtering for specified seasons (none returns all)
    if 'season' in filter_dict:
        # clean input, check seasons are valid
        filter_dict['season'] =\
            [x.replace('-', '/') for x in filter_dict['season']]
        abort_non_existant(filter_dict['season'], data['Season'].unique())   
        
        # filtering
        data = data[data['Season'].isin(filter_dict['season'])]
    
    # getting team data for those seasons
    if 'team' in filter_dict:
        # checking teams are valid
        abort_non_existant(filter_dict['team'], data['Team'].unique())
        
        # filtering
        data = data[data['Team'].isin(filter_dict['team'])]
        for team in filter_dict['team']:
            response[team], _ = get_team_all_seasons(data, team)
    else: # no teams provided
        for team in data['Team'].unique():
            response[team], _ = get_team_all_seasons(data, team)
            
    return response, 200
