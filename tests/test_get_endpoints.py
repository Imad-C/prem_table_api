from api import app


arsenal_2001_02 = { # This historical data should remain constant
    'D': 9, 'GA': 36, 'GD': '+43', 'GF': 79, 'L': 3, 'Pld': 38,
    'Pos': 1, 'Pts': '87', 'W': 26, 'Qualification or relegation': (
        'Qualification for the Champions League first group stage')
    }

    
def test_home():
    with app.test_client() as c:
        response = c.get("/")
        assert response.status_code == 200
        assert response.text == "Hello, world!"
    

def test_handle_exception():
    with app.test_client() as c:
        response = c.get("/teams/FakeTeam")
        assert response.status_code == 400
        assert response.json["message"] == "Could not find 'FakeTeam' in data." 


def test_single_team():
    with app.test_client() as c:
        response = c.get("/teams/Arsenal")
        assert response.status_code == 200
        assert response.json["data"]["2001/02"] == arsenal_2001_02
        

def test_single_season():
    with app.test_client() as c:
        response = c.get("/seasons/2001-02")
        assert response.status_code == 200
        assert response.json["data"]["Arsenal"] == arsenal_2001_02
        

def test_make_query():
    with app.test_client() as c:
        response = c.get("query?team=Arsenal&season=2001-02")
        assert response.status_code == 200
        assert response.json["data"]["Arsenal"]["2001/02"] == arsenal_2001_02