"""
NIRMAAN - AI Catalog Generation Service
Writes a genuinely product-specific title, description, SEO keywords, and
feature bullets from the artisan's OWN spoken description + detected visual
traits, using Gemini text generation. This replaces fully-templated,
category-bucketed text (which produced identical keywords/description for
every product in the same category) with real per-product generation.

If Gemini isn't configured or the call fails for any reason, `generate()`
returns None and the caller (catalog_extraction_service) falls back to a
transcript-driven local heuristic — still varies per input, just without AI.
"""
import os
import re
import json
from typing import Dict, Any, Optional

from ..config import GEMINI_API_KEY, GEMINI_TEXT_MODEL

REQUIRED_KEYS = ["title_en", "title_hi", "description_en", "description_hi", "seo_keywords_en", "seo_keywords_hi", "features"]


class AICatalogGenerationService:
    def __init__(self):
        self._client = None

    def _get_api_key(self) -> str:
        return (os.getenv("GEMINI_API_KEY", "").strip() or
                os.getenv("GOOGLE_API_KEY", "").strip() or
                GEMINI_API_KEY).strip()

    def is_available(self) -> bool:
        key = self._get_api_key()
        return bool(key and len(key) > 5)

    def _get_client(self):
        if not self.is_available():
            return None
        if self._client is None:
            try:
                from google import genai
                self._client = genai.Client(api_key=self._get_api_key())
            except Exception as e:
                print(f"[AICatalogGenerationService] Could not initialize Google GenAI client: {e}")
                return None
        return self._client

    @staticmethod
    def _strip_code_fence(text: str) -> str:
        text = text.strip()
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
        return text.strip()

    def generate(
        self,
        spoken_text: str,
        detected_language: str,
        category: str,
        craft_type: str,
        material: str,
        color: str,
    ) -> Optional[Dict[str, Any]]:
        client = self._get_client()
        if not client:
            return None
        if not spoken_text or not spoken_text.strip():
            return None

        prompt = f"""You are writing a real e-commerce marketplace listing for ONE specific
handmade product for an artisan marketplace app. Write content that is
SPECIFIC to this exact product, not generic boilerplate.

Artisan's own spoken description (ground truth — use only what is said or
directly implied by it, never invent certifications, awards, purity claims,
or facts not present here): "{spoken_text.strip()}"

Detected visual category: {category}
Detected craft technique: {craft_type}
Detected material: {material}
Detected dominant color: {color}

Write:
- title_en: a compelling, specific product title in English (under 12 words)
- title_hi: the same title translated naturally into Hindi
- description_en: a 2-4 sentence product description in English that weaves
  in real details from the artisan's description
- description_hi: the same description naturally written in Hindi (not a
  literal word-for-word translation, natural Hindi phrasing)
- seo_keywords_en: 6-10 realistic ENGLISH buyer search phrases a shopper
  would actually type on Amazon, Etsy, Flipkart, or ONDC to find this exact
  product (lowercase, no hashtags, no Hindi/Devanagari words — these are
  pasted directly into English-language marketplace listings, so they must
  be genuinely in English, not transliterated)
- seo_keywords_hi: 6-10 realistic Hindi buyer search phrases (Devanagari
  script) a shopper would type on a Hindi-language marketplace/ONDC seller
  app to find this exact product — these must be separate from and not a
  direct translation list of seo_keywords_en, written the way Hindi buyers
  actually search
- features: 3-5 short bullet-point features/selling-points, each a short
  phrase (not a full sentence), drawn from what the artisan actually said
  or from the detected material/technique — never fabricated claims

Return STRICT JSON only, with exactly these keys and nothing else, no
markdown code fences, no commentary:
{{"title_en": "...", "title_hi": "...", "description_en": "...", "description_hi": "...", "seo_keywords_en": ["...", "..."], "seo_keywords_hi": ["...", "..."], "features": ["...", "..."]}}
"""

        try:
            model = os.getenv("GEMINI_TEXT_MODEL", GEMINI_TEXT_MODEL or "gemini-3.6-flash").strip()
            response = client.models.generate_content(model=model, contents=[prompt])
            raw_text = getattr(response, "text", None)
            if not raw_text:
                print("[AICatalogGenerationService] Empty response text from Gemini")
                return None

            cleaned = self._strip_code_fence(raw_text)
            data = json.loads(cleaned)

            if not all(k in data for k in REQUIRED_KEYS):
                print(f"[AICatalogGenerationService] Response missing required keys: {data.keys()}")
                return None
            if (not isinstance(data.get("seo_keywords_en"), list) or
                    not isinstance(data.get("seo_keywords_hi"), list) or
                    not isinstance(data.get("features"), list)):
                return None

            return data

        except json.JSONDecodeError as e:
            print(f"[AICatalogGenerationService] Could not parse JSON from Gemini response: {e}")
            return None
        except Exception as e:
            print(f"[AICatalogGenerationService] Generation failed: {type(e).__name__}: {e}")
            return None


ai_catalog_generation_service = AICatalogGenerationService()
