"""
Test suite for Prioritized 5-Level Pricing Insight Logic
"""
import pytest
from backend.models.schemas import (
    PricingInsightRequest, PriceCalculationResult, MarketPriceCheckResult
)
from backend.services.pricing_insight_service import pricing_insight_service

def test_below_cost_warning_priority():
    # Cost = 500, Price = 400 (Direct loss)
    calc = PriceCalculationResult(
        material_cost=200.0,
        wastage_cost=0.0,
        labour_cost=300.0,
        packaging_cost=0.0,
        other_costs=0.0,
        selling_costs=0.0,
        total_cost=500.0,
        cost_floor=500.0,
        recommended_price=650.0,
        estimated_profit=150.0,
        premium_price=780.0
    )
    req = PricingInsightRequest(current_price=400.0, calculation=calc)
    insight = pricing_insight_service.generate_insight(req)
    
    assert insight.status_level == "below_cost"
    assert insight.status_badge == "🔴"
    assert "may not cover your costs" in insight.status_title

def test_underpricing_detection():
    # Cost = 840, Target = 1099, Market = 999 - 1399, Current = 900
    calc = PriceCalculationResult(
        material_cost=300.0,
        wastage_cost=0.0,
        labour_cost=540.0,
        packaging_cost=0.0,
        other_costs=0.0,
        selling_costs=0.0,
        total_cost=840.0,
        cost_floor=840.0,
        recommended_price=1099.0,
        estimated_profit=259.0,
        premium_price=1318.8
    )
    market = MarketPriceCheckResult(
        product_name="Terracotta Item",
        category="Pottery",
        search_queries=[],
        comparables=[],
        total_found=5,
        filtered_outliers_count=0,
        median_price=1150.0,
        p25_price=999.0,
        p75_price=1399.0,
        estimated_min_price=999.0,
        estimated_max_price=1399.0,
        typical_market_price=1150.0,
        confidence_level="high",
        confidence_badge_text="🟢 High Confidence",
        confidence_reasons=[],
        online_presence="Established"
    )
    req = PricingInsightRequest(current_price=900.0, calculation=calc, market_check=market)
    insight = pricing_insight_service.generate_insight(req)
    
    assert insight.status_level == "underpricing"
    assert insight.status_badge == "🟡"
    assert "underpricing" in insight.status_title.lower()

def test_competitive_pricing():
    calc = PriceCalculationResult(
        material_cost=200.0,
        wastage_cost=0.0,
        labour_cost=200.0,
        packaging_cost=0.0,
        other_costs=0.0,
        selling_costs=0.0,
        total_cost=400.0,
        cost_floor=400.0,
        recommended_price=550.0,
        estimated_profit=150.0,
        premium_price=660.0
    )
    market = MarketPriceCheckResult(
        product_name="Item",
        category="General",
        search_queries=[],
        comparables=[],
        total_found=4,
        filtered_outliers_count=0,
        median_price=550.0,
        p25_price=450.0,
        p75_price=650.0,
        estimated_min_price=450.0,
        estimated_max_price=650.0,
        typical_market_price=550.0,
        confidence_level="high",
        confidence_badge_text="🟢 High Confidence",
        confidence_reasons=[],
        online_presence="Established"
    )
    req = PricingInsightRequest(current_price=550.0, calculation=calc, market_check=market)
    insight = pricing_insight_service.generate_insight(req)
    
    assert insight.status_level == "competitive"
    assert insight.status_badge == "🟢"
    assert "competitive" in insight.status_title.lower()
