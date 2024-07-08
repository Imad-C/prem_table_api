from flask import Flask, jsonify, request

import prem_table_api.api_helpers as helpers

app = Flask(__name__)
data = helpers.load_data()


@app.get("/")
def home():
    return "Hello, world!"


@app.get("/teams")
def teams():
    response_data = [name for name in data['Team'].unique()]
    return jsonify({
        "success": True,
        "data": response_data
        }), 200


@app.get("/teams/<string:team_name>")
def single_team(team_name):
    response_data, status = helpers.get_team_all_seasons(data, team_name)
    return jsonify({
        "success": True,
        "team": team_name,
        "data": response_data
        }), status


@app.get("/seasons")
def seasons():
    response_data = [season for season in data['Season'].unique()]
    return jsonify({
        "success": True,
        "data": response_data
        }), 200


@app.get("/seasons/<string:season>")
def single_season(season):
    response_data, status = helpers.get_season_all_teams(data, season)
    return jsonify({
        "success": True,
        "season": season,
        "data": response_data
        }), status


@app.get("/query")
def make_query():
    query_filters = request.args.to_dict(flat=False)
    teams = query_filters['team'] if 'team' in query_filters else ['All']
    seasons = query_filters['season'] if 'season' in query_filters else ['All']
    response_data, status = helpers.get_filtered(data, query_filters) 
    
    return jsonify({
        "success": True,
        "team": teams,
        "season": seasons,
        "data": response_data
        }), status


@app.errorhandler(400)
def handle_exception(e):
    return jsonify({
        "success": False,
        "status": e.code,
        'message': e.description
        }), 400
