"""
NIRMAAN - Image Enhancement Service
Provides balanced, non-destructive exposure, contrast, sharpness, and white-balance enhancements for product clarity.
Strictly preserves authentic colors and details without over-processing.
"""
from PIL import Image, ImageEnhance, ImageOps

class ImageEnhancementService:
    @staticmethod
    def enhance_product(image: Image.Image) -> Image.Image:
        """
        Enhances product image clarity, contrast, and color vibrancy while strictly preserving authenticity.
        """
        img = image.copy()
        
        # 1. Subtle sharpness boost (brings out craft texture, weaving, clay grain)
        enhancer_sharpness = ImageEnhance.Sharpness(img)
        img = enhancer_sharpness.enhance(1.25)
        
        # 2. Balanced contrast boost
        enhancer_contrast = ImageEnhance.Contrast(img)
        img = enhancer_contrast.enhance(1.10)
        
        # 3. Controlled brightness / exposure compensation
        enhancer_brightness = ImageEnhance.Brightness(img)
        img = enhancer_brightness.enhance(1.05)
        
        # 4. Color richness (gentle saturation calibration)
        enhancer_color = ImageEnhance.Color(img)
        img = enhancer_color.enhance(1.08)
        
        return img

image_enhancement_service = ImageEnhancementService()
