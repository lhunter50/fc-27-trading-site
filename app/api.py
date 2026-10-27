from fastapi import FastAPI, Query

from app.analysis import scan_market
from app.scanner import find_investment_opportunities, get_scanner_summary


app = FastAPI(
     title="FIFA Trading Bot API",
     description="API for analyzing FIFA player prices and identifying investment opportunities.",
     version="1.0.0",
)

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.get("/api/players")
def get_players(
    category: str | None = None,
    min_price: int = Query(default=1000, ge=0),
    max_price: int = Query(default=100000, ge=0),
):
    players = scan_market(min_observations=1)

    if category:
        players = [player for player in players if player["category"] == category]

    filtered_players = [
        player for player in players
        if min_price <= player["current_price"] <= max_price
    ]

    return {
        "count": len(filtered_players),
        "players": filtered_players
    }

@app.get("/api/opportunities")
def get_opportunities(
    min_roi: float = 0,
    limit: int = Query(default=20, ge=1, le=100)
):
    opportunities = find_investment_opportunities()

    opportunities = [
        player for player in opportunities
        if player["roi"] >= min_roi
    ]

    return {
        "count": len(opportunities),
        "opportunities": opportunities[:limit]
    }

@app.get("/api/scanner/summary")
def scanner_summary():
    return get_scanner_summary()