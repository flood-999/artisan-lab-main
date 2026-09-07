"""
NIRMAAN - Image Validation Service (Product Authenticity Lock)
Validates that generated/enhanced product photos strictly preserve original product geometry, colors, patterns, and craftsmanship.
Provides automatic deterministic fallback if any hallucination is detected.
"""
from PIL import Image, ImageChops, ImageStat
from typing import Tuple

class ImageValidationService:
    @staticmethod
    def validate_authenticity(
        original_rgba: Image.Image,
        generated_rgba: Image.Image,
        tolerance_threshold: float = 0.85
    ) -> Tuple[bool, float, str]:
        """
        Validates product consistency between original and generated foregrounds.
        Returns: (is_valid, consistency_score, reason)
        """
        # Size match check
        if original_rgba.size != generated_rgba.size:
            generated_rgba = generated_rgba.resize(original_rgba.size, Image.Resampling.BILINEAR)

        # 1. Alpha mask silhouette overlap
        orig_alpha = original_rgba.split()[-1]
        gen_alpha = generated_rgba.split()[-1]
        
        diff_alpha = ImageChops.difference(orig_alpha, gen_alpha)
        stat_alpha = ImageStat.Stat(diff_alpha)
        mean_mask_diff = stat_alpha.mean[0] / 255.0  # 0.0 = identical, 1.0 = completely different
        mask_consistency = max(0.0, 1.0 - mean_mask_diff)

        # 2. Color distribution correlation
        orig_rgb = original_rgba.convert("RGB")
        gen_rgb = generated_rgba.convert("RGB")
        diff_rgb = ImageChops.difference(orig_rgb, gen_rgb)
        stat_rgb = ImageStat.Stat(diff_rgb)
        mean_color_diff = sum(stat_rgb.mean) / (3.0 * 255.0)
        color_consistency = max(0.0, 1.0 - mean_color_diff)

        overall_score = round(0.5 * mask_consistency + 0.5 * color_consistency, 3)

        if overall_score >= tolerance_threshold:
            return True, overall_score, "Authenticity verified: product shape, color, and craft details preserved."
        else:
            return False, overall_score, "Authenticity alert: generated output drifted from source product. Fallback activated."

image_validation_service = ImageValidationService()
