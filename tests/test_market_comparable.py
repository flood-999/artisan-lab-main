"""
Test suite for IQR Outlier Filtering and Comparable Engine
"""
import pytest
from backend.services.outlier_detection_service import outlier_detection_service
from backend.services.comparable_engine import comparable_engine
from backend.models.schemas import MarketProduct

def test_outlier_filtering_iqr():
    # Prompt specific example: ₹299, ₹349, ₹399, ₹425, ₹449, ₹499, ₹550, ₹4,999
    # ₹4,999 must be identified as an outlier and filtered out
    raw_prices = [299.0, 349.0, 399.0, 425.0, 449.0, 499.0, 550.0, 4999.0]
    filtered, median, p25, p75, est_min, est_max, outliers_count = outlier_detection_service.filter_outliers_iqr(raw_prices)
    
    assert 4999.0 not in filtered
    assert outliers_count == 1
    assert est_min >= 299.0
    assert est_max <= 600.0
    assert 390.0 <= median <= 460.0

def test_handmade_vs_mass_produced_filter():
    target = {
        "title_en": "Handmade Terracotta Bowl",
        "category": "Pottery",
        "material": "Clay",
        "craft_type": "Terracotta",
        "is_handmade": True
    }
    
    handmade_cand = MarketProduct(
        source="Artisan Guild",
        source_product_id="HG-1",
        title="Handcrafted Clay Serving Bowl",
        price=450.0,
        seller="Mitti Kendra",
        is_handmade=True,
        similarity_score=0.90,
        craft_type="Terracotta",
        material="Clay"
    )
    
    mass_produced_cand = MarketProduct(
        source="Plastic Wholesale",
        source_product_id="PW-1",
        title="Plastic Imitation Clay Bowl",
        price=99.0,
        seller="Poly Mart",
        is_handmade=False,
        similarity_score=0.85,
        craft_type="Molded",
        material="Plastic"
    )
    
    score_handmade = comparable_engine.calculate_similarity(target, handmade_cand)
    score_mass = comparable_engine.calculate_similarity(target, mass_produced_cand)
    
    assert score_handmade >= 0.70
    assert score_mass <= 0.25  # Severely penalized
