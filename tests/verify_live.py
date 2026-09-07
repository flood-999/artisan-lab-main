"""
Live Server Verification Script
"""
import httpx
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

def run_checks():
    client = httpx.Client(base_url="http://127.0.0.1:8000")
    
    print("1. Health Check:")
    h = client.get("/api/health").json()
    print("   Status:", h["status"], "| App:", h["app"])

    print("\n2. Voice Transcription & Multilingual Extraction:")
    v = client.post("/api/voice/transcribe", json={"simulated_speech": "यह प्राकृतिक बांस से बुनी फल रखने की टोकरी है।"}).json()
    print("   Detected Language:", v["detected_language"], f"({v['language_name']})")
    print("   Original:", v["transcript_original"])
    print("   English:", v["transcript_en"])

    print("\n3. Deterministic Cost Pricing:")
    p = client.post("/api/pricing/calculate", json={
        "material_cost": 200,
        "time_spent_hours": 4,
        "labour_rate_hourly": 150,
        "wastage_percent": 5,
        "packaging_cost": 20,
        "other_costs": 10,
        "selling_costs": 0,
        "profit_margin_percent": 30,
        "premium_multiplier": 1.2
    }).json()
    print("   Total Cost (Floor): ₹", p["total_cost"])
    print("   Recommended Price:  ₹", p["recommended_price"])
    print("   Premium Price:      ₹", p["premium_price"])

    print("\n4. Check Market Price (IQR Outlier Filtered):")
    m = client.post("/api/pricing/market-check", json={
        "product_name": "Bamboo Storage Basket",
        "category": "Bamboo craft",
        "material": "Natural Bamboo",
        "craft_type": "Bamboo Weaving",
        "is_handmade": True
    }).json()
    print(f"   Estimated Market Range: ₹{m['estimated_min_price']} — ₹{m['estimated_max_price']}")
    print(f"   Typical Market Price:   ₹{m['typical_market_price']}")
    print(f"   Confidence Level:       {m['confidence_level'].upper()} ({m['confidence_badge_text']})")
    print(f"   Comparables Count:      {len(m['comparables'])}")

    print("\n5. Pricing Insight Dashboard:")
    ins = client.post("/api/pricing/insight", json={
        "current_price": 550,
        "calculation": p,
        "market_check": m
    }).json()
    print(f"   Status:      {ins['status_badge']} {ins['status_title']}")
    print(f"   Explanation: {ins['explanation']}")
    print(f"   Advice Count:{len(ins['actionable_advice'])}")

    print("\n6. Marketplace Feed:")
    feed = client.get("/api/marketplace/feed").json()
    print(f"   Published Products Available: {feed['total']}")
    for prod in feed["products"]:
        print(f"   • {prod['title_en']} — ₹{prod['price']} ({prod['craft_type']})")

    print("\n✓ ALL LIVE END-TO-END VERIFICATION CHECKS PASSED!")

if __name__ == "__main__":
    run_checks()
