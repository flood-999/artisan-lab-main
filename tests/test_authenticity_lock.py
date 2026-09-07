"""
Test suite for Product Authenticity Lock
"""
import pytest
from PIL import Image, ImageDraw
from backend.services.image_validation_service import image_validation_service

def test_authenticity_passes_for_identical_and_enhanced():
    img1 = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
    d1 = ImageDraw.Draw(img1)
    d1.ellipse([(50, 50), (150, 150)], fill=(180, 80, 40, 255))
    
    # Enhanced with slightly sharper/brighter pixels
    img2 = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
    d2 = ImageDraw.Draw(img2)
    d2.ellipse([(50, 50), (150, 150)], fill=(190, 85, 45, 255))
    
    is_valid, score, reason = image_validation_service.validate_authenticity(img1, img2)
    assert is_valid is True
    assert score >= 0.85

def test_authenticity_fails_and_triggers_fallback_on_severe_alteration():
    img1 = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
    d1 = ImageDraw.Draw(img1)
    d1.ellipse([(50, 50), (150, 150)], fill=(180, 80, 40, 255)) # Brown round pot
    
    # Severely altered shape & color (e.g. green square hallucination)
    img2 = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
    d2 = ImageDraw.Draw(img2)
    d2.rectangle([(10, 10), (190, 190)], fill=(20, 180, 40, 255))
    
    is_valid, score, reason = image_validation_service.validate_authenticity(img1, img2)
    assert is_valid is False
    assert "Fallback activated" in reason
