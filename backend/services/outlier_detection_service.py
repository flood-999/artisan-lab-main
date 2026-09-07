"""
NIRMAAN - Outlier Detection Service
Calculates Median, P25, P75, and Interquartile Range (IQR) to filter out market price distortions.
"""
from typing import List, Tuple
import math

class OutlierDetectionService:
    @staticmethod
    def _percentile(sorted_data: List[float], percentile: float) -> float:
        if not sorted_data:
            return 0.0
        k = (len(sorted_data) - 1) * percentile
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            return sorted_data[int(k)]
        d0 = sorted_data[int(f)] * (c - k)
        d1 = sorted_data[int(c)] * (k - f)
        return round(d0 + d1, 2)

    @classmethod
    def filter_outliers_iqr(cls, prices: List[float], k_factor: float = 1.5) -> Tuple[List[float], float, float, float, float, float, int]:
        """
        Takes raw prices list, returns:
        (filtered_prices, median, p25, p75, estimated_min, estimated_max, filtered_outliers_count)
        """
        if not prices:
            return [], 0.0, 0.0, 0.0, 0.0, 0.0, 0
            
        sorted_prices = sorted(prices)
        n = len(sorted_prices)
        
        if n == 1:
            p = sorted_prices[0]
            return sorted_prices, p, p, p, p, p, 0
            
        p25 = cls._percentile(sorted_prices, 0.25)
        median = cls._percentile(sorted_prices, 0.50)
        p75 = cls._percentile(sorted_prices, 0.75)
        iqr = p75 - p25
        
        # Upper & Lower bounds
        lower_bound = max(0.0, p25 - (k_factor * iqr))
        upper_bound = p75 + (k_factor * iqr)
        
        filtered = [p for p in sorted_prices if lower_bound <= p <= upper_bound]
        
        # If filtering is too aggressive and leaves fewer than 2 items, preserve original
        if len(filtered) < 2 and len(sorted_prices) >= 2:
            filtered = sorted_prices
            
        outliers_count = len(sorted_prices) - len(filtered)
        
        # Recalculate statistics on filtered data
        final_sorted = sorted(filtered)
        final_p25 = cls._percentile(final_sorted, 0.25)
        final_median = cls._percentile(final_sorted, 0.50)
        final_p75 = cls._percentile(final_sorted, 0.75)
        
        # Estimated realistic market range
        estimated_min = final_p25
        estimated_max = final_p75
        
        return final_sorted, final_median, final_p25, final_p75, estimated_min, estimated_max, outliers_count

outlier_detection_service = OutlierDetectionService()
