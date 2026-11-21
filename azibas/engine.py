import numpy as np
from math import exp, factorial

def poisson_pmf(k, lam):
    return exp(-lam) * lam**k / factorial(k)

def football_probabilities(home_rate, away_rate, max_goals=12):
    """Score model: independent Poisson baseline. Must be calibrated on historical data."""
    hg=max(.01,float(home_rate)); ag=max(.01,float(away_rate))
    hp=np.array([poisson_pmf(k,hg) for k in range(max_goals+1)])
    ap=np.array([poisson_pmf(k,ag) for k in range(max_goals+1)])
    matrix=np.outer(hp,ap)
    # Normalize truncated tail to preserve a valid probability distribution.
    matrix=matrix/matrix.sum()
    home=float(np.tril(matrix,-1).sum()) # row > col
    draw=float(np.trace(matrix))
    away=float(np.triu(matrix,1).sum())
    over25=float(sum(matrix[i,j] for i in range(max_goals+1) for j in range(max_goals+1) if i+j>=3))
    under25=1-over25
    btts=float(sum(matrix[i,j] for i in range(1,max_goals+1) for j in range(1,max_goals+1)))
    return {"home":home,"draw":draw,"away":away,"over25":over25,"under25":under25,"btts":btts}

def simulate_poisson_over(mean, threshold, n=25000, seed=17):
    rng=np.random.default_rng(seed)
    x=rng.poisson(max(.01,float(mean)),int(n))
    return float(np.mean(x>threshold))

def market_value(probability, odds):
    p=float(probability); o=float(odds)
    if not (0 < p <= 1) or o <= 1:
        raise ValueError("Probabilité ou cote invalide.")
    return {"probability":p,"fair_odds":1/p,"value":p*o-1,"ev_per_unit":p*o-1}

def analyze_event(event, simulations=25000):
    results=[]
    if str(event.get("sport","")).lower()!="football":
        return results  # no fake predictions for unsupported sport-specific models
    required=("home_rate","away_rate")
    if any(event.get(k) is None for k in required):
        return results
    probs=football_probabilities(event["home_rate"],event["away_rate"])
    markets=[
      ("Victoire domicile","home","odds_home"),
      ("Match nul","draw","odds_draw"),
      ("Victoire extérieur","away","odds_away"),
      ("Over 2,5 buts","over25","odds_over25"),
      ("Under 2,5 buts","under25","odds_under25"),
      ("BTTS Oui","btts","odds_btts")
    ]
    for label,key,odd_key in markets:
        odds=event.get(odd_key)
        if odds is None or str(odds)=="nan": continue
        try: metrics=market_value(probs[key],float(odds))
        except (ValueError,TypeError): continue
        results.append(_row(event,label,metrics,"Poisson indépendant",simulations))
    for label,mean_key,threshold,odd_key in [
      ("Over 9,5 corners","corners_mean",9,"odds_over95_corners"),
      ("Over 3,5 cartons","cards_mean",3,"odds_over35_cards")
    ]:
        mean=event.get(mean_key); odds=event.get(odd_key)
        if mean is None or odds is None or str(mean)=="nan" or str(odds)=="nan": continue
        p=simulate_poisson_over(float(mean),threshold,simulations,seed=29+threshold)
        results.append(_row(event,label,market_value(p,float(odds)),"Poisson comptage à calibrer",simulations))
    return results

def _row(event,market,metrics,model,n):
    return {"sport":event.get("sport"),"event":event.get("event"),"market":market,
      **metrics,"odds":float(event[{
       "Victoire domicile":"odds_home","Match nul":"odds_draw","Victoire extérieur":"odds_away",
       "Over 2,5 buts":"odds_over25","Under 2,5 buts":"odds_under25","BTTS Oui":"odds_btts",
       "Over 9,5 corners":"odds_over95_corners","Over 3,5 cartons":"odds_over35_cards"}[market]]),
      "model":model,"simulations":int(n),"data_status":event.get("data_status","Non précisé")}
