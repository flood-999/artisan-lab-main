"""
Test suite for NIRMAAN REST API Endpoints
"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["app"] == "NIRMAAN"

def test_artisan_profile():
    response = client.get("/api/artisan")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert data["preferred_language"] in ["hi", "en", "mr", "bn", "gu", "ta", "te", "kn", "pa", "ml"]

def test_products_list_and_seed_data():
    response = client.get("/api/products")
    assert response.status_code == 200
    products = response.json()
    assert len(products) >= 3
    # Check terracotta bowl is present
    titles = [p["title_en"] for p in products]
    assert any("Terracotta" in t for t in titles)

def test_pricing_calculate_api():
    payload = {
        "material_cost": 200.0,
        "time_spent_hours": 4.0,
        "labour_rate_hourly": 150.0,
        "wastage_percent": 0.0,
        "packaging_cost": 0.0,
        "other_costs": 0.0,
        "selling_costs": 0.0,
        "profit_margin_percent": 30.0,
        "premium_multiplier": 1.20
    }
    response = client.post("/api/pricing/calculate", json=payload)
    assert response.status_code == 200
    res = response.json()
    assert res["total_cost"] == 800.0
    assert res["recommended_price"] == 1040.0
    assert res["premium_price"] == 1248.0

def test_market_price_check_api():
    payload = {
        "product_name": "Terracotta Serving Bowl",
        "category": "Pottery",
        "material": "Natural Clay",
        "craft_type": "Terracotta",
        "is_handmade": True
    }
    response = client.post("/api/pricing/market-check", json=payload)
    assert response.status_code == 200
    res = response.json()
    assert res["total_found"] > 0
    assert res["estimated_min_price"] > 0
    assert res["typical_market_price"] > 0
    assert res["confidence_level"] in ["high", "medium", "low"]

def test_voice_transcribe_and_catalog_api():
    payload = {
        "simulated_speech": "यह प्राकृतिक बांस से बुनी हुई फल रखने की टोकरी है।"
    }
    response = client.post("/api/voice/transcribe", json=payload)
    assert response.status_code == 200
    res = response.json()
    assert "बांस" in res["transcript_original"]
    assert res["detected_language"] == "hi"

    # Test catalog extraction
    cat_payload = {
        "spoken_text": res["transcript_original"],
        "detected_language": res["detected_language"],
        "visual_traits": {"category": "Bamboo craft", "craft_type": "Bamboo Weaving"}
    }
    cat_resp = client.post("/api/voice/catalog", json=cat_payload)
    assert cat_resp.status_code == 200
    cat_data = cat_resp.json()
    assert cat_data["category"] == "Bamboo craft"
    assert "bamboo" in cat_data["title_en"].lower()
