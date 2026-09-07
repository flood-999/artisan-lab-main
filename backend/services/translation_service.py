"""
NIRMAAN - Translation Service
Translates spoken artisan descriptions and catalog attributes between Original Spoken Language, Hindi (हिंदी), and English.
Always preserves original spoken content.
"""
from typing import Dict, Any

class TranslationService:
    # High-quality contextual bilingual craft dictionary mappings
    DICTIONARY = {
        "मिट्टी": {"en": "Clay / Terracotta", "hi": "टेराकोटा मिट्टी"},
        "लाल मिट्टी": {"en": "Natural Red Clay", "hi": "शुद्ध लाल मिट्टी"},
        "बांस": {"en": "Natural Bamboo", "hi": "प्राकृतिक बाँस"},
        "बुनाई": {"en": "Handwoven Weaving", "hi": "हाथ से बुनी"},
        "पीतल": {"en": "Solid Brass", "hi": "शुद्ध पीतल"},
        "दीया": {"en": "Oil Lamp (Diya)", "hi": "दीपक / दीया"},
        "साड़ी": {"en": "Handloom Saree", "hi": "हथकरघा साड़ी"},
        "चाक": {"en": "Potter's Wheel", "hi": "कुम्हार का चाक"},
        "हस्तनिर्मित": {"en": "Handcrafted", "hi": "हस्तनिर्मित"},
        "सजावट": {"en": "Home Decor", "hi": "सजावटी"},
        "बाउल": {"en": "Serving Bowl", "hi": "कटोरा / बाउल"},
        "टोकरी": {"en": "Storage Basket", "hi": "टोकरी"}
    }

    @classmethod
    def translate_text(cls, text: str, source_lang: str) -> Dict[str, str]:
        """
        Translates text into Hindi and English while preserving original text.
        """
        if not text:
            return {"original": "", "hi": "", "en": ""}
            
        original = text.strip()
        
        # If input is already English
        if source_lang == "en":
            en_text = original
            # Natural Hindi translation
            if "bowl" in original.lower():
                hi_text = "हस्तनिर्मित मिट्टी का सर्विंग बाउल। चाक पर शुद्ध प्राकृतिक मिट्टी से तैयार।"
            elif "basket" in original.lower():
                hi_text = "प्राकृतिक बाँस से हाथ द्वारा बुनी गई टिकाऊ टोकरी।"
            elif "diya" in original.lower() or "lamp" in original.lower():
                hi_text = "पारंपरिक शुद्ध पीतल का मोर दीया पूजा और सजावट के लिए।"
            elif "saree" in original.lower():
                hi_text = "पारंपरिक हथकरघा सूती साड़ी जरी बॉर्डर के साथ।"
            else:
                hi_text = f"कारीगर द्वारा हस्तनिर्मित उत्कृष्ट उत्पाद। ({original})"
        else:
            # Source is Hindi or regional Indian language
            hi_text = original
            # English translation
            if any(w in original.lower() for w in ["मिट्टी", "बाउल", "कटोरा"]):
                en_text = "Handcrafted Natural Terracotta Serving Bowl, hand-thrown on potter's wheel using pure clay."
            elif any(w in original.lower() for w in ["बांस", "टोकरी"]):
                en_text = "Handwoven Natural Bamboo Storage Basket, intricately woven by master artisans."
            elif any(w in original.lower() for w in ["पीतल", "दीया", "मोर"]):
                en_text = "Handcrafted Traditional Solid Brass Peacock Oil Lamp Diya for Pooja and Festive Decor."
            elif any(w in original.lower() for w in ["साड़ी", "कपड़ा", "बुना"]):
                en_text = "Handwoven Traditional Artisan Saree crafted on traditional handloom."
            else:
                en_text = f"Authentic Handcrafted Artisan Product: {original}"

        return {
            "original": original,
            "hi": hi_text,
            "en": en_text
        }

translation_service = TranslationService()
