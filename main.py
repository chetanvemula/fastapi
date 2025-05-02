
from fastapi import FastAPI
import requests

app = FastAPI()
POLYGON_API_KEY = "GLqBwSTlMJLaaSV4mf7SI9_n0VCUin33"

def get_polygon_quote(symbol):
    url = f"https://api.polygon.io/v2/last/nbbo/{symbol}?apiKey={POLYGON_API_KEY}"
    r = requests.get(url)
    return r.json()

def get_vix_value():
    url = f"https://api.polygon.io/v2/aggs/ticker/VIX/prev?apiKey={POLYGON_API_KEY}"
    r = requests.get(url)
    return r.json()['results'][0]['c']

@app.get("/realtime-signal")
def get_strategy():
    nq_data = get_polygon_quote("C:NDX")
    vix = get_vix_value()

    # Mock ADD and TICK values
    add = 1200
    tick = 850

    nq_price = nq_data['results']['ask']['p']

    if vix < 16 and add > 1000 and tick > 800:
        return {
            "strategy": "Bull Put Spread",
            "entry": f"Sell Put {int(nq_price - 300)}, Buy Put {int(nq_price - 350)}",
            "exit": "Target 25% profit",
            "reason": f"NDX: {nq_price}, VIX: {vix}, ADD: {add}, TICK: {tick}"
        }
    elif vix > 20 and add < -1000 and tick < -800:
        return {
            "strategy": "Bear Call Spread",
            "entry": f"Sell Call {int(nq_price + 300)}, Buy Call {int(nq_price + 350)}",
            "exit": "Target 25% profit",
            "reason": f"NDX: {nq_price}, VIX: {vix}, ADD: {add}, TICK: {tick}"
        }
    elif 16 <= vix <= 22 and -500 <= add <= 500:
        return {
            "strategy": "Iron Condor",
            "entry": f"Sell Put {int(nq_price - 300)}, Buy Put {int(nq_price - 350)}, Sell Call {int(nq_price + 300)}, Buy Call {int(nq_price + 350)}",
            "exit": "Target 25% profit",
            "reason": f"NDX: {nq_price}, VIX: {vix}, ADD: {add}, TICK: {tick}"
        }
    else:
        return {
            "strategy": "Iron Butterfly",
            "entry": f"Sell Put & Call at {int(nq_price)}, Buy wings at {int(nq_price - 300)} and {int(nq_price + 300)}",
            "exit": "Target 25% profit",
            "reason": f"NDX: {nq_price}, VIX: {vix}, ADD: {add}, TICK: {tick}"
        }
