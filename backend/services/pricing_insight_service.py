"""
NIRMAAN - Pricing Insight Service
Combines artisan production costs, cost-based target, and market intelligence to produce prioritized, actionable insights.
Strictly never makes false certainties.
"""
from typing import Optional, List
from ..models.schemas import PricingInsightRequest, PricingInsightResult, PriceCalculationResult, MarketPriceCheckResult

class PricingInsightService:
    @staticmethod
    def generate_insight(request: PricingInsightRequest) -> PricingInsightResult:
        calc: Optional[PriceCalculationResult] = request.calculation
        market: Optional[MarketPriceCheckResult] = request.market_check
        
        # Determine current price & cost values
        current_price = request.current_price
        if current_price is None and calc:
            current_price = calc.recommended_price
            
        estimated_cost = calc.total_cost if calc else 350.0
        cost_target = calc.recommended_price if calc else 500.0
        
        market_min = market.estimated_min_price if market else None
        market_max = market.estimated_max_price if market else None
        typical_market = market.typical_market_price if market else None
        
        advice: List[str] = []
        suggested_min = None
        suggested_max = None
        
        # --- PRIORITY 1: Below-Cost Warning (🔴) ---
        if current_price is not None and current_price < estimated_cost:
            status_level = "below_cost"
            status_badge = "🔴"
            status_title = "Your price may not cover your costs"
            explanation = (
                f"Your current price of ₹{current_price:.0f} is lower than your estimated production cost "
                f"of ₹{estimated_cost:.0f}. Selling at this price may result in a financial loss on your labour and materials."
            )
            suggested_min = cost_target
            suggested_max = round(cost_target * 1.15, 2)
            advice.append(f"Increase your price to at least ₹{cost_target:.0f} to cover costs and earn fair wages.")
            advice.append("Check if material wastage or time spent can be optimized without reducing quality.")

        # --- PRIORITY 2: Underpricing Detection (🟡) ---
        elif (
            current_price is not None and
            market_min is not None and
            (current_price < cost_target or current_price < market_min)
        ):
            status_level = "underpricing"
            status_badge = "🟡"
            status_title = "You may be underpricing your product"
            explanation = (
                f"Your current price of ₹{current_price:.0f} is below your recommended target (₹{cost_target:.0f}) "
                f"and below the typical market range (₹{market_min:.0f} — ₹{market_max:.0f}). Buyers often associate very low prices with lower craft authenticity."
            )
            suggested_min = max(cost_target, market_min)
            suggested_max = round(suggested_min * 1.15, 2)
            advice.append(f"Consider testing a price between ₹{suggested_min:.0f} — ₹{suggested_max:.0f}.")
            advice.append("Emphasize your authentic handmade process and premium natural materials in your catalog.")

        # --- PRIORITY 3: Competitive Price (🟢) ---
        elif (
            current_price is not None and
            current_price >= estimated_cost and
            (market_max is None or current_price <= market_max * 1.10)
        ):
            status_level = "competitive"
            status_badge = "🟢"
            status_title = "Your price looks competitive"
            explanation = (
                f"Your price of ₹{current_price:.0f} is well within the current market range "
                f"and comfortably covers your production costs of ₹{estimated_cost:.0f} with a healthy artisan profit."
            )
            suggested_min = current_price
            suggested_max = round(current_price * 1.10, 2)
            advice.append("Your pricing strikes a great balance between fair artisan earnings and buyer appeal.")
            advice.append("You can offer festival bundle discounts (e.g. buy 2 for 5% off) without hurting profit.")

        # --- PRIORITY 4: High-Price Positioning (🟠) ---
        elif (
            current_price is not None and
            market_max is not None and
            current_price > market_max * 1.10
        ):
            status_level = "high_price"
            status_badge = "🟠"
            status_title = "Your price may be higher than comparable products"
            explanation = (
                f"Your price of ₹{current_price:.0f} is higher than the typical market range of ₹{market_min:.0f} — ₹{market_max:.0f}. "
                f"Higher pricing is completely viable if your piece has intricate detailing, master craftsmanship, or rare heritage techniques."
            )
            suggested_min = market_min
            suggested_max = current_price
            advice.append("Include high-resolution close-up photos showing the intricate craft and master details.")
            advice.append("Highlight your artisan story and the hours of dedicated handwork invested.")

        # --- PRIORITY 5: Insufficient Market Data / Cost-Only ---
        else:
            status_level = "cost_only"
            status_badge = "💡"
            status_title = "Cost-based pricing guidance"
            explanation = (
                f"Based on your estimated production cost of ₹{estimated_cost:.0f}, your target price of ₹{cost_target:.0f} "
                f"ensures you earn fair wages for your hours of skilled craftwork."
            )
            suggested_min = cost_target
            suggested_max = round(cost_target * 1.20, 2)
            advice.append(f"Recommended price: ₹{cost_target:.0f} (recovers material + labour + profit).")
            advice.append(f"Premium tier: ₹{cost_target * 1.20:.0f} for custom or gift-boxed orders.")

        return PricingInsightResult(
            current_price=current_price,
            estimated_cost=estimated_cost,
            cost_based_target=cost_target,
            market_min=market_min,
            market_max=market_max,
            typical_market_price=typical_market,
            status_level=status_level,
            status_badge=status_badge,
            status_title=status_title,
            explanation=explanation,
            suggested_test_range_min=suggested_min,
            suggested_test_range_max=suggested_max,
            actionable_advice=advice
        )

pricing_insight_service = PricingInsightService()
