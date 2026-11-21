from azibas.engine import football_probabilities, market_value, analyze_event

def test_football_probabilities_sum_to_one():
    p=football_probabilities(1.5,1.0)
    assert abs(p["home"]+p["draw"]+p["away"]-1)<1e-8
    assert 0 <= p["btts"] <= 1

def test_value_calculation():
    x=market_value(.60,2.0)
    assert round(x["value"],8)==.2
    assert round(x["fair_odds"],8)==1.66666667

def test_no_fake_nonfootball_prediction():
    assert analyze_event({"sport":"Tennis","event":"A-B","home_rate":1.2,"away_rate":1.0})==[]

def test_football_omits_markets_without_odds():
    r=analyze_event({"sport":"Football","event":"A-B","home_rate":1.4,"away_rate":1.0})
    assert r==[]
