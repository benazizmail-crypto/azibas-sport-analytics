from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from azibas.engine import analyze_event

app=FastAPI(title="AZIBAS SPORT ANALYTICS API",version="2.1.0",
 description="API locale de simulation. Les résultats sont limités aux modèles effectivement implémentés.")

class Event(BaseModel):
    sport:str
    event:str
    home_rate:float=Field(gt=0)
    away_rate:float=Field(gt=0)
    corners_mean:Optional[float]=None
    cards_mean:Optional[float]=None
    odds_home:Optional[float]=None
    odds_draw:Optional[float]=None
    odds_away:Optional[float]=None
    odds_over25:Optional[float]=None
    odds_under25:Optional[float]=None
    odds_btts:Optional[float]=None
    odds_over95_corners:Optional[float]=None
    odds_over35_cards:Optional[float]=None

@app.get("/health")
def health():
    return {"status":"ok","live_data_connected":False,"version":"2.1.0"}

@app.post("/analyze")
def analyze(event:Event, simulations:int=Field(default=25000,ge=1000,le=1000000)):
    try:
        return {"event":event.event,"results":analyze_event(event.model_dump(),simulations)}
    except Exception as exc:
        raise HTTPException(status_code=400,detail=str(exc))
