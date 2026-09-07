"""
Test suite for Deterministic Cost Pricing Service
"""
import pytest
from backend.models.schemas import PriceCalculationInput
from backend.services.cost_pricing_service import cost_pricing_service

def test_basic_cost_calculation():
    inp = PriceCalculationInput(
        material_cost=200.0,
        time_spent_hours=4.0,
        labour_rate_hourly=150.0,
        wastage_percent=0.0,
        packaging_cost=0.0,
        other_costs=0.0,
        selling_costs=0.0,
        profit_margin_percent=30.0,
        premium_multiplier=1.20
    )
    result = cost_pricing_service.calculate(inp)
    
    # Labour = 4 * 150 = 600
    assert result.labour_cost == 600.0
    assert result.wastage_cost == 0.0
    # Total Cost = 200 + 600 = 800
    assert result.total_cost == 800.0
    assert result.cost_floor == 800.0
    # Profit = 800 * 0.30 = 240
    assert result.estimated_profit == 240.0
    # Recommended Price = 800 + 240 = 1040
    assert result.recommended_price == 1040.0
    # Premium Price = 1040 * 1.20 = 1248
    assert result.premium_price == 1248.0

def test_full_cost_calculation_with_wastage_and_packaging():
    inp = PriceCalculationInput(
        material_cost=500.0,
        time_spent_hours=3.5,
        labour_rate_hourly=200.0,
        wastage_percent=10.0,
        packaging_cost=50.0,
        other_costs=30.0,
        selling_costs=20.0,
        profit_margin_percent=25.0,
        premium_multiplier=1.25
    )
    result = cost_pricing_service.calculate(inp)
    
    # Wastage = 500 * 0.10 = 50
    assert result.wastage_cost == 50.0
    # Labour = 3.5 * 200 = 700
    assert result.labour_cost == 700.0
    # Total Cost = 500 + 50 + 700 + 50 + 30 + 20 = 1350
    assert result.total_cost == 1350.0
    assert result.cost_floor == 1350.0
    # Profit = 1350 * 0.25 = 337.5
    assert result.estimated_profit == 337.5
    # Recommended Price = 1350 + 337.5 = 1687.5
    assert result.recommended_price == 1687.5
    # Premium Price = 1687.5 * 1.25 = 2109.38
    assert result.premium_price == 2109.38
