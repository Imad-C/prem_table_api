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
