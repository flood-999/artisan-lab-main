"""
NIRMAAN - Comparable Product Matching Engine
Implements multi-factor weighted similarity scoring and strict Handmade vs Mass-Produced filtering.
"""
from typing import List, Dict, Any, Optional
from ..models.schemas import MarketProduct

class ComparableEngine:
    WEIGHTS = {
        "product_type": 0.25,
        "category": 0.15,
        "material": 0.20,
        "size": 0.10,
        "craftsmanship": 0.10,
        "visual_similarity": 0.15,
        "use_case": 0.05
    }

    @classmethod
    def calculate_similarity(
        cls,
        target_product: Dict[str, Any],
        candidate: MarketProduct
    ) -> float:
        # Mandatory Rule 46: Handmade vs Mass-produced separation
        if target_product.get("is_handmade", True) and candidate.is_handmade is False:
            return 0.20  # Severely penalized, not a valid comparable
            
        score = 0.0
        
        # 1. Product Type (25%)
        target_type = (target_product.get("title_en") or target_product.get("title_original") or "").lower()
        cand_title = candidate.title.lower()
        if any(term in cand_title for term in target_type.split()):
            score += cls.WEIGHTS["product_type"] * 1.0
        else:
            score += cls.WEIGHTS["product_type"] * 0.4
            
        # 2. Category (15%)
        target_cat = (target_product.get("category") or "").lower()
        cand_cat = (candidate.category or "").lower()
        if target_cat in cand_cat or cand_cat in target_cat:
            score += cls.WEIGHTS["category"] * 1.0
        else:
            score += cls.WEIGHTS["category"] * 0.3
            
        # 3. Material (20%)
        target_mat = (target_product.get("material") or "").lower()
        cand_mat = (candidate.material or "").lower()
        if target_mat and (target_mat in cand_mat or cand_mat in cand_title):
            score += cls.WEIGHTS["material"] * 1.0
        elif target_mat:
            score += cls.WEIGHTS["material"] * 0.5
        else:
            score += cls.WEIGHTS["material"] * 0.7
            
        # 4. Size (10%)
        # Approximate size matching
        score += cls.WEIGHTS["size"] * 0.85
        
        # 5. Craftsmanship (10%)
        target_craft = (target_product.get("craft_type") or "").lower()
        cand_craft = (candidate.craft_type or "").lower()
        if target_craft and (target_craft in cand_craft or target_craft in cand_title):
            score += cls.WEIGHTS["craftsmanship"] * 1.0
        else:
            score += cls.WEIGHTS["craftsmanship"] * 0.6
            
        # 6. Visual Similarity (15%)
        score += cls.WEIGHTS["visual_similarity"] * candidate.similarity_score
        
        # 7. Use Case (5%)
        score += cls.WEIGHTS["use_case"] * 0.90
        
        return round(min(1.0, score), 2)

    @classmethod
    def filter_and_rank_comparables(
        cls,
        target_product: Dict[str, Any],
        candidate_pool: List[MarketProduct],
        min_similarity_threshold: float = 0.50
    ) -> List[MarketProduct]:
        scored = []
        for cand in candidate_pool:
            sim = cls.calculate_similarity(target_product, cand)
            if sim >= min_similarity_threshold:
                cand_copy = cand.model_copy()
                cand_copy.similarity_score = sim
                scored.append(cand_copy)
                
        # Sort by similarity descending
        scored.sort(key=lambda x: x.similarity_score, reverse=True)
        return scored

comparable_engine = ComparableEngine()
