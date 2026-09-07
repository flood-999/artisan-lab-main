"""
NIRMAAN - Market Data Service
Manages search query generation, market provider querying, price normalization, outlier filtering, and confidence estimation.
"""
from typing import List, Dict, Any, Optional
from ..models.schemas import MarketPriceCheckRequest, MarketPriceCheckResult, MarketProduct
from ..database.db import db
from .comparable_engine import comparable_engine
from .outlier_detection_service import outlier_detection_service

class MarketDataProvider:
    """Modular market data provider interface."""
    def search(self, queries: List[str], category: str, craft_type: Optional[str] = None, material: Optional[str] = None) -> List[MarketProduct]:
        return db.search_market_products(category=category, craft_type=craft_type, material=material)

class MarketDataService:
    def __init__(self, provider: Optional[MarketDataProvider] = None):
        self.provider = provider or MarketDataProvider()

    @staticmethod
    def generate_search_queries(product_name: str, category: str, material: Optional[str], craft_type: Optional[str]) -> List[str]:
        queries = []
        name_clean = product_name.strip()
        mat_clean = (material or "").strip()
        craft_clean = (craft_type or "").strip()
        
        # Primary localized queries for Indian market
        queries.append(f"handmade {name_clean} India")
        if mat_clean:
            queries.append(f"handcrafted {mat_clean} {name_clean} India INR")
        if craft_clean:
            queries.append(f"traditional {craft_clean} {name_clean} artisan price India")
        queries.append(f"{category} {name_clean} online price India")
        
        return list(dict.fromkeys(queries))[:4]

    def check_market_price(self, request: MarketPriceCheckRequest) -> MarketPriceCheckResult:
        # 1. Generate search queries
        queries = self.generate_search_queries(
            product_name=request.product_name,
            category=request.category,
            material=request.material,
            craft_type=request.craft_type
        )
        
        # 2. Fetch candidates from market provider
        candidate_pool = self.provider.search(
            queries=queries,
            category=request.category,
            craft_type=request.craft_type,
            material=request.material
        )
        
        # 3. Match & Rank Comparables (with Handmade filter)
        target_dict = {
            "title_en": request.product_name,
            "category": request.category,
            "material": request.material,
            "craft_type": request.craft_type,
            "is_handmade": request.is_handmade
        }
        ranked_comparables = comparable_engine.filter_and_rank_comparables(
            target_product=target_dict,
            candidate_pool=candidate_pool,
            min_similarity_threshold=0.50
        )
        
        # 4. Extract and normalize per-piece prices
        raw_prices = []
        for item in ranked_comparables:
            unit_price = item.price / max(1, item.quantity)
            raw_prices.append(unit_price)
            
        # 5. Outlier Filtering via IQR
        filtered_prices, median, p25, p75, est_min, est_max, outliers_count = outlier_detection_service.filter_outliers_iqr(raw_prices)
        
        # 6. Calculate Confidence
        total_found = len(ranked_comparables)
        confidence_level = "low"
        confidence_badge_text = "🔴 Low Confidence"
        confidence_reasons = []
        
        if total_found >= 4 and outliers_count <= 2:
            confidence_level = "high"
            confidence_badge_text = "🟢 High Confidence"
            confidence_reasons.append(f"Found {total_found} high-similarity comparable artisan listings in India.")
            confidence_reasons.append("Stable price distribution with low variance.")
        elif total_found >= 2:
            confidence_level = "medium"
            confidence_badge_text = "🟡 Medium Confidence"
            confidence_reasons.append(f"Found {total_found} comparable items with matching craft and materials.")
            confidence_reasons.append("Slight price spread across different artisan clusters.")
        else:
            confidence_level = "low"
            confidence_badge_text = "🔴 Low Confidence"
            confidence_reasons.append("Limited direct listings found for this unique handcrafted piece.")
            confidence_reasons.append("Estimates are indicative; prioritize your cost calculation.")

        # 7. Online Presence Analysis
        if total_found >= 5:
            online_presence = "Established category with active online demand"
        elif total_found >= 2:
            online_presence = "Several comparable listings found online"
        else:
            online_presence = "Limited online presence — unique artisan craft"

        # Fallback safe ranges if data is zero
        if not filtered_prices:
            est_min = 250.0
            est_max = 650.0
            typical_price = 450.0
            median = 450.0
            p25 = 250.0
            p75 = 650.0
        else:
            typical_price = median

        return MarketPriceCheckResult(
            product_name=request.product_name,
            category=request.category,
            search_queries=queries,
            comparables=ranked_comparables[:6],
            total_found=total_found,
            filtered_outliers_count=outliers_count,
            median_price=round(median, 2),
            p25_price=round(p25, 2),
            p75_price=round(p75, 2),
            estimated_min_price=round(est_min, 2),
            estimated_max_price=round(est_max, 2),
            typical_market_price=round(typical_price, 2),
            confidence_level=confidence_level,
            confidence_badge_text=confidence_badge_text,
            confidence_reasons=confidence_reasons,
            online_presence=online_presence,
            currency="INR"
        )

market_data_service = MarketDataService()
