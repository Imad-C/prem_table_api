# Premier League Table API

## Description

A Flask API to transfer data of the premier league table from 1992 - present. 
This was also a useful project to help me learn about Flask and API's.

## Installation

As this Flask app is not currently hosted anywhere, the data must first be 
collected locally, and then the app must be run on a local server before any
api calls can be made.

First, ensure you are within the project directory.

Then, install the required packages:
```bash
pip install -e .
```

Collect the data by running:
```bash
python -m data.wiki_scraping
```

Finally, run the api locally:
```bash
flask run
```

## Usage

You can then call the api. There are 5 endpoints: 
- "/teams"
- "/teams/\<team name>"
- "/seasons"
- "/seasons/\<season name>"
- "/query?\<query filter>"

Examples below:

With cURL:
```bash
curl http://localhost:5000/teams/Chelsea
```

With python:
```python
import requests

# A simple example:
season_02_03 = requests.get("http://localhost:5000/seasons/2002-03").json()

# A more complicated exmaple:
query = (
    "team=Arsenal&team=Aston Villa&"
    "season=2014-15&season=2015-16"
    )
custom_query = requests.get("http://localhost:5000/query?" + query)

# This data can then be indexed into, eg: 
data = custom_query.json()['data']['Arsenal']['2014-15']
```

You can find further python examples in the prem_table_api/api_examples folder.