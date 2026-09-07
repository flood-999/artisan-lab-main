"""
NIRMAAN - Cost Pricing Service
Deterministic offline price calculation based on artisan raw materials, labour hours, rates, wastage, packaging, and margins.
NEVER uses AI for arithmetic.
"""
from ..models.schemas import PriceCalculationInput, PriceCalculationResult

class CostPricingService:
    @staticmethod
    def calculate(input_data: PriceCalculationInput) -> PriceCalculationResult:
        # 1. Wastage Cost = Material Cost * Wastage % / 100
        wastage_cost = round(input_data.material_cost * (input_data.wastage_percent / 100.0), 2)
        
        # 2. Labour Cost = Hours * Labour Rate
        labour_cost = round(input_data.time_spent_hours * input_data.labour_rate_hourly, 2)
        
        # 3. Total Cost (Cost Floor) = Material + Wastage + Labour + Packaging + Other + Selling Costs
        total_cost = round(
            input_data.material_cost +
            wastage_cost +
            labour_cost +
            input_data.packaging_cost +
            input_data.other_costs +
            input_data.selling_costs,
            2
        )
        
        # Cost Floor: Minimum amount needed to recover estimated costs
        cost_floor = total_cost
        
        # 4. Profit = Total Cost * Profit Margin % / 100
        profit_amount = round(total_cost * (input_data.profit_margin_percent / 100.0), 2)
        
        # 5. Recommended Price = Total Cost + Profit
        recommended_price = round(total_cost + profit_amount, 2)
        
        # 6. Premium Price = Recommended Price * Multiplier (Default 1.20)
        premium_price = round(recommended_price * input_data.premium_multiplier, 2)
        
        breakdown_text = (
            f"Material: ₹{input_data.material_cost:.0f} | "
            f"Wastage ({input_data.wastage_percent:.0f}%): ₹{wastage_cost:.0f} | "
            f"Labour ({input_data.time_spent_hours}h @ ₹{input_data.labour_rate_hourly:.0f}/h): ₹{labour_cost:.0f} | "
            f"Packaging: ₹{input_data.packaging_cost:.0f} | "
            f"Other: ₹{input_data.other_costs:.0f} | "
            f"Selling Fees: ₹{input_data.selling_costs:.0f} | "
            f"Total Cost: ₹{total_cost:.0f} | "
            f"Profit ({input_data.profit_margin_percent:.0f}%): ₹{profit_amount:.0f}"
        )
        
        return PriceCalculationResult(
            material_cost=input_data.material_cost,
            wastage_cost=wastage_cost,
            labour_cost=labour_cost,
            packaging_cost=input_data.packaging_cost,
            other_costs=input_data.other_costs,
            selling_costs=input_data.selling_costs,
            total_cost=total_cost,
            cost_floor=cost_floor,
            recommended_price=recommended_price,
            estimated_profit=profit_amount,
            premium_price=premium_price,
            currency="INR",
            breakdown_text=breakdown_text
        )

cost_pricing_service = CostPricingService()
