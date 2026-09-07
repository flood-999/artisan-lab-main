"""
NIRMAAN - Exhaustive Test Suite Covering Every Platform Feature
Tests all 11 core feature areas:
1. System Health & Root
2. Artisan Profile & Multi-Craft Onboarding
3. Product Vision, Segmentation, Backgrounds & Authenticity Lock
4. Multilingual Speech, Transcription & Voice Commands
5. AI Factuality Verification & Grounded Storytelling Catalog Generation
6. Deterministic Cost Pricing Engine & Mathematical Formulas
7. Market Comparable Intelligence, IQR Outlier Detection & Multi-Craft Search
8. Pricing Insight & Loss Prevention Dashboard
9. Product Lifecycle & CRUD Management
10. Digital Catalogs & Curated Collections
11. Marketplace Feed, Search & Category Filtering
"""
import io
import pytest
from PIL import Image
from fastapi.testclient import TestClient
from backend.main import app
from backend.database.db import db
from backend.models.schemas import (
    PriceCalculationInput, MarketPriceCheckRequest, PricingInsightRequest,
    ArtisanBase, Product, CatalogCreate
)
from backend.services import (
    cost_pricing_service,
    market_data_service,
    pricing_insight_service,
    product_vision_service,
    speech_service,
    translation_service,
    catalog_extraction_service,
    voice_command_service,
    catalog_service
)
from backend.services.outlier_detection_service import outlier_detection_service
from backend.services.image_validation_service import image_validation_service

client = TestClient(app)

# Helper to create a test image
def create_test_image_bytes(color=(200, 90, 50), width=300, height=300):
    img = Image.new("RGB", (width, height), color=color)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


# ==========================================
# 1. SYSTEM HEALTH & ROOT
# ==========================================
class TestSystemHealth:
    def test_root_endpoint_serves_frontend(self):
        response = client.get("/")
        assert response.status_code == 200

    def test_health_check_status(self):
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["app"] == "NIRMAAN"
        assert data["database"] == "connected"


# ==========================================
# 2. ARTISAN PROFILE & MULTI-CRAFT ONBOARDING
# ==========================================
class TestArtisanProfile:
    def test_get_default_artisan_profile(self):
        response = client.get("/api/artisan")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "artisan-ramesh"
        assert "Ramesh" in data["name"]
        assert "craft_type" in data
        assert "preferred_language" in data

    def test_update_artisan_profile_multi_craft(self):
        update_data = {
            "name": "Sita Devi & Ramesh",
            "phone": "+91 98765 43210",
            "preferred_language": "hi",
            "craft_type": "Pottery & Terracotta, Bamboo & Cane Craft, Brass & Metal Craft",
            "seller_type": "SHG",
            "region": "Varanasi, Uttar Pradesh",
            "bio": "Artisan SHG creating sustainable pottery, cane baskets, and brass lamps."
        }
        response = client.put("/api/artisan", json=update_data)
        assert response.status_code == 200
        updated = response.json()
        assert updated["name"] == "Sita Devi & Ramesh"
        assert updated["seller_type"] == "SHG"
        assert "Bamboo & Cane Craft" in updated["craft_type"]
        assert "Brass & Metal Craft" in updated["craft_type"]


# ==========================================
# 3. PRODUCT VISION & AUTHENTICITY LOCK
# ==========================================
class TestProductVisionPipeline:
    def test_upload_and_process_photo(self):
        img_bytes = create_test_image_bytes(color=(190, 80, 40))
        response = client.post(
            "/api/products/upload-photo",
            files={"file": ("test_pottery.jpg", img_bytes, "image/jpeg")},
            data={"category": "Pottery", "craft_type": "Terracotta"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "visual_traits" in data
        assert "category" in data["visual_traits"]
        assert len(data["images"]) >= 1

    def test_generate_studio_style_presets(self):
        for style in ["clean_studio", "warm_heritage", "rustic_clay", "silk_fabric", "minimal_wood"]:
            response = client.post(
                "/api/products/generate-style",
                json={
                    "image_url": "/static/images/terracotta_marketplace.jpg",
                    "style": style
                }
            )
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "image" in data
            assert data["image"]["url"].startswith("/uploads/marketplace/")

    def test_authenticity_lock_verification(self):
        img1 = Image.new("RGBA", (200, 200), (200, 100, 50, 255))
        img2 = Image.new("RGBA", (200, 200), (205, 105, 55, 255)) # slightly enhanced
        is_authentic, score, msg = image_validation_service.validate_authenticity(img1, img2, tolerance_threshold=0.85)
        assert is_authentic is True
        assert score >= 0.85

        # Severely altered image (tampered shape & inverted colors)
        img3 = Image.new("RGBA", (200, 200), (10, 240, 200, 255))
        is_authentic_fail, score_fail, _ = image_validation_service.validate_authenticity(img1, img3, tolerance_threshold=0.85)
        assert is_authentic_fail is False
        assert score_fail < 0.85


# ==========================================
# 4. MULTILINGUAL SPEECH & VOICE COMMANDS
# ==========================================
class TestSpeechAndVoiceCommands:
    @pytest.mark.parametrize("lang_code, sample_text", [
        ("hi", "यह प्राकृतिक बांस से बुनी फल रखने की टोकरी है"),
        ("mr", "हा अस्सल मातीचा हस्तनिर्मित सर्व्हिंग बाऊल आहे"),
        ("bn", "এটি খাঁটি হাতে তৈরি বাঁশের ফলের ঝুড়ি"),
        ("gu", "આ કુદરતી માટીમાંથી બનાવેલ સુંદર કટોરો છે"),
        ("ta", "இது பாரம்பரிய கைவினை பித்தளை விளக்கு"),
        ("te", "ఇది సంప్రదాయ చేతితో తయారు చేసిన మట్టి పాత్ర"),
        ("kn", "ಇದು ನೈಸರ್ಗಿಕ ಮಣ್ಣಿನಿಂದ ಕೈಯಿಂದ ಮಾಡಿದ ಬಟ್ಟಲು"),
        ("pa", "ਇਹ ਹੱਥੀਂ ਤਿਆਰ ਕੀਤੀ ਪਿੱਤਲ ਦੀ ਦੀਵਾ ਹੈ"),
        ("ml", "ഇത് പരമ്പരാഗത കൈകൊണ്ട് ഉണ്ടാക്കിയ മൺപാത്രം ആണ്"),
        ("en", "This is a handmade brass peacock oil lamp made by traditional casting")
    ])
    def test_multilingual_voice_transcription(self, lang_code, sample_text):
        response = client.post(
            "/api/voice/transcribe",
            json={"simulated_speech": sample_text}
        )
        assert response.status_code == 200
        res = response.json()
        assert res["detected_language"] == lang_code
        assert res["transcript_original"] == sample_text
        assert len(res["transcript_en"]) > 0
        assert len(res["transcript_hi"]) > 0

    def test_voice_command_set_price(self):
        req = {"command_text": "What is the recommended price for this craft"}
        response = client.post("/api/voice/command", json=req)
        assert response.status_code == 200
        res = response.json()
        assert res["action"] == "calculate_price"

    def test_voice_command_publish_product(self):
        req = {"command_text": "Publish my product to the marketplace"}
        response = client.post("/api/voice/command", json=req)
        assert response.status_code == 200
        res = response.json()
        assert res["action"] == "publish_product"

    def test_voice_command_help(self):
        req = {"command_text": "Help me use NIRMAAN"}
        response = client.post("/api/voice/command", json=req)
        assert response.status_code == 200
        res = response.json()
        assert res["action"] == "help"


# ==========================================
# 5. AI DESCRIPTION VERIFICATION & CATALOG SYNTHESIS
# ==========================================
class TestAICatalogVerificationAndSynthesis:
    def test_extract_and_verify_catalog_description(self):
        payload = {
            "spoken_text": "मैं 4 घंटे लगाकर शुद्ध पीतल से पारंपरिक मोर वाला दीया ढलाई करके बनाता हूँ।",
            "detected_language": "hi",
            "visual_traits": {
                "category": "Metal craft",
                "craft_type": "Brass Casting",
                "material": "Solid Brass",
                "color": "Golden Brass"
            }
        }
        response = client.post("/api/voice/catalog", json=payload)
        assert response.status_code == 200
        data = response.json()
        
        # Check extraction
        assert data["category"] == "Metal craft"
        assert "brass" in data["title_en"].lower() or "lamp" in data["title_en"].lower() or "diya" in data["title_en"].lower()
        assert "पीतल" in data["title_hi"] or "दीया" in data["title_hi"]
        # Check AI Verification Checklist
        # Check AI Verification Checklist
        assert "ai_verification" in data
        assert data["ai_verification"]["is_verified"] is True
        assert "Casting" in data["ai_verification"]["verified_technique"]
        assert data["ai_verification"]["verified_material"] == "Solid Brass"
        assert len(data["ai_verification"]["verification_checklist"]) >= 3

        # Check Grounded Storytelling Descriptions
        assert "Artisan Story" in data["description_en"]
        assert "Features & Care" in data["description_en"]
        assert "कारीगर" in data["description_hi"]
        assert "विशेषता" in data["description_hi"]

        # Check Keywords
        assert len(data["seo_keywords"]) >= 3


# ==========================================
# 6. DETERMINISTIC COST PRICING ENGINE
# ==========================================
class TestCostPricingEngine:
    def test_cost_calculation_mathematics(self):
        input_data = PriceCalculationInput(
            material_cost=300.0,
            time_spent_hours=5.0,
            labour_rate_hourly=200.0,  # Labour = 1000
            wastage_percent=10.0,      # Material wastage = 30
            packaging_cost=50.0,
            other_costs=20.0,
            selling_costs=0.0,
            profit_margin_percent=25.0, # Profit = 1400 * 0.25 = 350
            premium_multiplier=1.20
        )
        res = cost_pricing_service.calculate(input_data)
        
        expected_total_cost = 300 + 1000 + 30 + 50 + 20 # 1400.0
        assert res.total_cost == expected_total_cost
        assert res.cost_floor == expected_total_cost
        assert res.recommended_price == 1750.0
        assert res.premium_price == 2100.0
        assert "Total Cost" in res.breakdown_text

    def test_zero_time_cost_safety(self):
        input_data = PriceCalculationInput(
            material_cost=150.0,
            time_spent_hours=0.0,
            labour_rate_hourly=0.0,
            wastage_percent=0.0,
            packaging_cost=0.0,
            other_costs=0.0,
            selling_costs=0.0,
            profit_margin_percent=20.0,
            premium_multiplier=1.15
        )
        res = cost_pricing_service.calculate(input_data)
        assert res.total_cost == 150.0
        assert res.recommended_price == 180.0


# ==========================================
# 7. MARKET COMPARABLE & IQR OUTLIER DETECTION
# ==========================================
class TestMarketComparableEngine:
    def test_iqr_outlier_filtering(self):
        # 10 reasonable prices + 1 extreme low + 1 extreme high outlier
        prices = [350.0, 380.0, 400.0, 420.0, 390.0, 410.0, 450.0, 370.0, 430.0, 395.0, 20.0, 5000.0]
        filtered, median, p25, p75, est_min, est_max, outliers_count = outlier_detection_service.filter_outliers_iqr(prices)
        
        assert outliers_count == 2
        assert 20.0 not in filtered
        assert 5000.0 not in filtered
        assert 370.0 <= median <= 420.0
        assert est_min >= 300.0
        assert est_max <= 500.0

    @pytest.mark.parametrize("category, craft, material, name", [
        ("Pottery", "Terracotta", "Clay", "Terracotta Serving Bowl"),
        ("Bamboo craft", "Bamboo Weaving", "Bamboo", "Bamboo Storage Basket"),
        ("Metal craft", "Brass Casting", "Brass", "Brass Peacock Diya"),
        ("Textiles", "Handloom Weaving", "Cotton", "Handloom Cotton Saree"),
        ("Woodcraft", "Wood Carving", "Sheesham Wood", "Carved Wooden Tray"),
        ("Jewellery", "Terracotta Jewellery", "Clay", "Handcrafted Terracotta Necklace"),
        ("Paintings", "Folk Painting", "Handmade Paper", "Madhubani Painting Canvas"),
        ("Leather & Jute", "Jute Braiding", "Natural Jute", "Handcrafted Jute Tote Bag")
    ])
    def test_market_check_across_all_craft_categories(self, category, craft, material, name):
        req = {
            "product_name": name,
            "category": category,
            "material": material,
            "craft_type": craft,
            "is_handmade": True
        }
        response = client.post("/api/pricing/market-check", json=req)
        assert response.status_code == 200
        res = response.json()
        assert res["total_found"] >= 1
        assert res["estimated_min_price"] > 0
        assert res["typical_market_price"] >= res["estimated_min_price"]
        assert len(res["comparables"]) >= 1
        assert res["comparables"][0]["is_handmade"] is True


# ==========================================
# 8. PRICING INSIGHT & LOSS PREVENTION DASHBOARD
# ==========================================
class TestPricingInsightDashboard:
    def test_below_cost_loss_warning(self):
        req = {
            "current_price": 400.0,
            "calculation": {
                "material_cost": 200.0,
                "wastage_cost": 0.0,
                "labour_cost": 400.0,
                "packaging_cost": 0.0,
                "other_costs": 0.0,
                "selling_costs": 0.0,
                "total_cost": 600.0,
                "cost_floor": 600.0,
                "recommended_price": 800.0,
                "estimated_profit": 200.0,
                "premium_price": 960.0
            }
        }
        response = client.post("/api/pricing/insight", json=req)
        assert response.status_code == 200
        res = response.json()
        assert res["status_level"] == "below_cost"
        assert "🔴" in res["status_badge"]
        assert "may not cover your costs" in res["status_title"]
        assert len(res["actionable_advice"]) >= 1

    def test_underpriced_warning(self):
        req = {
            "current_price": 500.0,
            "calculation": {
                "material_cost": 150.0,
                "wastage_cost": 0.0,
                "labour_cost": 150.0,
                "packaging_cost": 0.0,
                "other_costs": 0.0,
                "selling_costs": 0.0,
                "total_cost": 300.0,
                "cost_floor": 300.0,
                "recommended_price": 750.0,
                "estimated_profit": 450.0,
                "premium_price": 900.0
            },
            "market_check": {
                "product_name": "Test Craft",
                "category": "Pottery",
                "search_queries": [],
                "comparables": [],
                "total_found": 4,
                "filtered_outliers_count": 0,
                "median_price": 800.0,
                "p25_price": 650.0,
                "p75_price": 950.0,
                "estimated_min_price": 650.0,
                "estimated_max_price": 950.0,
                "typical_market_price": 800.0,
                "confidence_level": "high",
                "confidence_badge_text": "🟢 High",
                "confidence_reasons": [],
                "online_presence": "Active",
                "currency": "INR"
            }
        }
        response = client.post("/api/pricing/insight", json=req)
        assert response.status_code == 200
        res = response.json()
        assert res["status_level"] == "underpricing"
        assert "🟡" in res["status_badge"]

    def test_competitive_pricing(self):
        req = {
            "current_price": 750.0,
            "calculation": {
                "material_cost": 200.0,
                "wastage_cost": 0.0,
                "labour_cost": 300.0,
                "packaging_cost": 0.0,
                "other_costs": 0.0,
                "selling_costs": 0.0,
                "total_cost": 500.0,
                "cost_floor": 500.0,
                "recommended_price": 700.0,
                "estimated_profit": 200.0,
                "premium_price": 840.0
            },
            "market_check": {
                "product_name": "Test Craft",
                "category": "Pottery",
                "search_queries": [],
                "comparables": [],
                "total_found": 4,
                "filtered_outliers_count": 0,
                "median_price": 750.0,
                "p25_price": 650.0,
                "p75_price": 900.0,
                "estimated_min_price": 650.0,
                "estimated_max_price": 900.0,
                "typical_market_price": 750.0,
                "confidence_level": "high",
                "confidence_badge_text": "🟢 High",
                "confidence_reasons": [],
                "online_presence": "Active",
                "currency": "INR"
            }
        }
        response = client.post("/api/pricing/insight", json=req)
        assert response.status_code == 200
        res = response.json()
        assert res["status_level"] == "competitive"
        assert "🟢" in res["status_badge"]

    def test_overpriced_warning(self):
        req = {
            "current_price": 1500.0,
            "calculation": {
                "material_cost": 200.0,
                "wastage_cost": 0.0,
                "labour_cost": 300.0,
                "packaging_cost": 0.0,
                "other_costs": 0.0,
                "selling_costs": 0.0,
                "total_cost": 500.0,
                "cost_floor": 500.0,
                "recommended_price": 700.0,
                "estimated_profit": 200.0,
                "premium_price": 840.0
            },
            "market_check": {
                "product_name": "Test Craft",
                "category": "Pottery",
                "search_queries": [],
                "comparables": [],
                "total_found": 4,
                "filtered_outliers_count": 0,
                "median_price": 750.0,
                "p25_price": 600.0,
                "p75_price": 900.0,
                "estimated_min_price": 600.0,
                "estimated_max_price": 900.0,
                "typical_market_price": 750.0,
                "confidence_level": "high",
                "confidence_badge_text": "🟢 High",
                "confidence_reasons": [],
                "online_presence": "Active",
                "currency": "INR"
            }
        }
        response = client.post("/api/pricing/insight", json=req)
        assert response.status_code == 200
        res = response.json()
        assert res["status_level"] == "high_price"
        assert "🟠" in res["status_badge"]


# ==========================================
# 9. PRODUCT CRUD & PUBLICATION LIFECYCLE
# ==========================================
class TestProductLifecycleCRUD:
    def test_create_and_publish_new_product(self):
        prod_id = f"test-prod-{id(self)}"
        new_prod = {
            "id": prod_id,
            "artisan_id": "artisan-ramesh",
            "title_original": "हाथ से बनी पीतल की घंटी",
            "title_hi": "हस्तनिर्मित पारंपरिक पीतल घंटी",
            "title_en": "Handcrafted Traditional Brass Pooja Bell",
            "description_original": "शुद्ध पीतल से ढलाई करके बनाई गई पूजा घंटी।",
            "description_hi": "पारंपरिक ढलाई कला द्वारा शुद्ध पीतल से निर्मित।",
            "description_en": "Handcrafted pure brass pooja bell with resonant sound.",
            "category": "Metal craft",
            "subcategory": "Pooja & Bells",
            "craft_type": "Brass Casting",
            "material": "Solid Brass",
            "color": "Golden",
            "dimensions": "Height: 5 inches",
            "weight": "350g",
            "seo_keywords": ["brass bell", "pooja bell", "handcrafted brass"],
            "price": 499.0,
            "currency": "INR",
            "status": "draft",
            "is_handmade": True,
            "images": [
                {"id": "img-t1", "image_type": "marketplace", "file_path": "/static/images/diya_marketplace.jpg", "url": "/static/images/diya_marketplace.jpg", "label": "Marketplace", "is_primary": True}
            ],
            "attributes": []
        }
        
        # 1. Save as Draft
        save_resp = client.post("/api/products/save", json=new_prod)
        assert save_resp.status_code == 200
        saved = save_resp.json()
        assert saved["id"] == prod_id
        assert saved["status"] == "draft"

        # 2. Get Detail
        get_resp = client.get(f"/api/products/{prod_id}")
        assert get_resp.status_code == 200
        assert get_resp.json()["title_en"] == "Handcrafted Traditional Brass Pooja Bell"

        # 3. Publish
        pub_resp = client.post(f"/api/products/{prod_id}/publish")
        assert pub_resp.status_code == 200
        published = pub_resp.json()
        assert published["status"] == "published"


# ==========================================
# 10. DIGITAL CATALOGS & GROUPED COLLECTIONS
# ==========================================
class TestDigitalCatalogs:
    def test_list_and_create_catalog(self):
        # List Catalogs
        list_resp = client.get("/api/catalogs")
        assert list_resp.status_code == 200
        catalogs = list_resp.json()
        assert len(catalogs) >= 1

        # Create New Collection
        cat_payload = {
            "title": "Masterpiece Brass Collection ✨",
            "description": "Exquisite hand-cast brass home decor items and lamps.",
            "cover_image_url": "/static/images/diya_marketplace.jpg",
            "product_ids": ["prod-brass-diya"],
            "is_published": True
        }
        create_resp = client.post("/api/catalogs", json=cat_payload)
        assert create_resp.status_code == 200
        created = create_resp.json()
        assert created["title"] == "Masterpiece Brass Collection ✨"
        assert len(created["products"]) >= 1


# ==========================================
# 11. MARKETPLACE FEED, SEARCH & CATEGORY FILTERING
# ==========================================
class TestMarketplaceFeed:
    def test_marketplace_all_feed(self):
        response = client.get("/api/marketplace/feed")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1
        assert len(data["products"]) >= 1

    def test_marketplace_category_filter(self):
        response = client.get("/api/marketplace/feed?category=Pottery")
        assert response.status_code == 200
        data = response.json()
        for p in data["products"]:
            assert "pottery" in p["category"].lower() or "terracotta" in p["craft_type"].lower()

    def test_marketplace_keyword_search(self):
        response = client.get("/api/marketplace/feed?query=diya")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1
        assert any("diya" in p["title_en"].lower() or "diya" in p["title_hi"].lower() for p in data["products"])
