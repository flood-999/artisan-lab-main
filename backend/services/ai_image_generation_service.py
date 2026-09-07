"""
NIRMAAN - AI Image Generation & Transformation Service
Uses Google Gemini Interactions API (`google-genai` SDK) with `gemini-3.1-flash-image` (Nano Banana 2)
to transform raw smartphone photos into professional e-commerce studio catalog images.
Includes robust offline fallback.
"""
import os
import io
import base64
import logging
from typing import Optional, Union
from PIL import Image

from ..config import GEMINI_API_KEY, GEMINI_IMAGE_MODEL

logger = logging.getLogger("nirmaan.ai_image")

class AIImageGenerationService:
    def __init__(self):
        self._client = None

    @property
    def model_name(self) -> str:
        return os.getenv("GEMINI_IMAGE_MODEL", GEMINI_IMAGE_MODEL or "gemini-3.1-flash-image").strip()

    def _get_api_key(self) -> str:
        return (os.getenv("GEMINI_API_KEY", "").strip() or 
                os.getenv("GOOGLE_API_KEY", "").strip() or 
                GEMINI_API_KEY).strip()

    def is_available(self) -> bool:
        """Returns True if a valid Gemini API key is configured."""
        key = self._get_api_key()
        return bool(key and len(key) > 5)

    def _get_client(self):
        if not self.is_available():
            return None
        if self._client is None:
            try:
                from google import genai
                key = self._get_api_key()
                self._client = genai.Client(api_key=key)
            except Exception as e:
                logger.warning(f"Could not initialize Google GenAI client: {e}")
                return None
        return self._client

    def generate_marketplace_image(
        self,
        source_image: Union[str, Image.Image],
        category: str = "Handicrafts",
        craft_type: str = "Handmade"
    ) -> Optional[Image.Image]:
        """
        Transforms raw smartphone photo into a commercial studio marketplace catalog image.
        Returns PIL Image if successful, or None on fallback.
        """
        client = self._get_client()
        if not client:
            return None

        prompt = (
            f"Commercial e-commerce studio catalog photograph of this authentic handcrafted {craft_type} ({category}). "
            "Transform this raw smartphone photo into a pristine, high-end online marketplace catalog image. "
            "Preserve the authentic handcrafted product exactly as shown: keep its genuine shape, texture, material, color, and artisanal craft details. "
            "Place the product centered on a smooth, elegant studio pedestal with soft studio lighting, subtle realistic contact shadow, and clean off-white studio background. "
            "Eliminate cluttered background, bedsheets, flooring, and hands. Output a high-resolution commercial product shot."
        )

        return self._execute_image_transformation(client, source_image, prompt)

    def generate_lifestyle_image(
        self,
        source_image: Union[str, Image.Image],
        category: str = "Handicrafts",
        craft_type: str = "Handmade"
    ) -> Optional[Image.Image]:
        """
        Transforms raw smartphone photo into an atmospheric interior lifestyle photo.
        Returns PIL Image if successful, or None on fallback.
        """
        client = self._get_client()
        if not client:
            return None

        prompt = (
            f"Architectural interior lifestyle photograph featuring this handcrafted {craft_type} ({category}). "
            "The exact same handcrafted piece is placed in a warm, aesthetically styled modern Indian living or dining room. "
            "Natural morning sunlight streaming from a side window, resting on a textured wooden table or rustic shelf with warm ambient decor, "
            "gentle depth of field with soft blurred background. Keep the product authentic and true to its handmade craft."
        )

        return self._execute_image_transformation(client, source_image, prompt)

    def generate_styled_backdrop(
        self,
        source_image: Union[str, Image.Image],
        style_preset: str = "clean_studio",
        category: str = "Handicrafts",
        craft_type: str = "Handmade"
    ) -> Optional[Image.Image]:
        """
        Re-renders product with a specific studio backdrop aesthetic preset.
        """
        client = self._get_client()
        if not client:
            return None

        style_prompts = {
            "clean_studio": "on a minimalist white studio pedestal with clean softbox lighting and subtle contact shadow.",
            "warm_heritage": "on a warm terracotta and brass heritage pedestal with soft warm golden illumination.",
            "rustic_clay": "on a natural textured sandstone and organic earthy clay surface with warm rustic sunlight.",
            "silk_fabric": "on luxurious draped silk fabric with gentle folds, elegant shadows, and premium ambient glow.",
            "minimal_wood": "on a smooth seasoned teak wood table with soft morning natural light and warm earthy depth."
        }

        backdrop_desc = style_prompts.get(style_preset, style_prompts["clean_studio"])
        prompt = (
            f"Professional studio photograph of this authentic handcrafted {craft_type} ({category}) {backdrop_desc} "
            "Preserve the authentic handmade product geometry, color, and texture exactly. High commercial quality."
        )

        return self._execute_image_transformation(client, source_image, prompt)

    def generate_professional_studio_image(
        self,
        source_image: Union[str, Image.Image],
        category: str = "Handicrafts",
        craft_type: str = "Handmade"
    ) -> Optional[Image.Image]:
        """
        Premium "Professional Studio" variant: a dramatic black-background
        commercial shot with glossy floor reflection and rim/shine
        lighting — the look used for premium jewellery/electronics-style
        product photography, as distinct from the plain white marketplace
        shot.
        """
        client = self._get_client()
        if not client:
            return None

        prompt = (
            f"Premium high-end commercial product photograph of this authentic handcrafted {craft_type} ({category}). "
            "Preserve the authentic handcrafted product exactly as shown: keep its genuine shape, texture, material, color, and artisanal craft details — do not alter the product itself. "
            "Place the product centered on a deep black studio background with a glossy black reflective floor showing a subtle mirror reflection of the product beneath it. "
            "Use dramatic professional studio lighting with soft rim light and gentle highlight shine along the product's edges, like a premium jewellery or luxury-goods advertisement. "
            "Eliminate cluttered background, bedsheets, flooring, and hands. Output a high-resolution, dramatic, premium commercial product shot."
        )

        return self._execute_image_transformation(client, source_image, prompt)

    def _execute_image_transformation(
        self,
        client,
        source_image: Union[str, Image.Image],
        prompt: str
    ) -> Optional[Image.Image]:
        """
        Executes image editing via the real `google-genai` SDK content-generation
        API (`client.models.generate_content`). The model returns one or more
        response parts; an image-capable model returns an `inline_data` part
        containing the generated image bytes.

        (A previous version of this method called `client.interactions.create`,
        which is not a real method on the google-genai client — every call
        silently raised an exception and fell back to the local Pillow studio,
        which is why AI backgrounds never actually appeared. This is the fix.)
        """
        print("\n" + "="*50)
        print("AI IMAGE SERVICE CALLED: YES")
        print(f"GEMINI_IMAGE_MODEL: {self.model_name}")
        print("GEMINI REQUEST STARTED")
        try:
            # 1. Normalize input to a PIL Image (the SDK accepts PIL images directly)
            if isinstance(source_image, str):
                pil_image = Image.open(source_image).convert("RGB")
            else:
                pil_image = source_image.convert("RGB")

            # 2. Call Gemini's content-generation API with text + image input
            response = client.models.generate_content(
                model=self.model_name,
                contents=[prompt, pil_image],
            )

            print("GEMINI REQUEST SUCCEEDED: YES")

            # 3. Extract the generated image from the response parts
            candidates = getattr(response, "candidates", None) or []
            for candidate in candidates:
                content = getattr(candidate, "content", None)
                parts = getattr(content, "parts", None) or []
                for part in parts:
                    inline_data = getattr(part, "inline_data", None)
                    if inline_data and getattr(inline_data, "data", None):
                        raw = inline_data.data
                        decoded_bytes = base64.b64decode(raw) if isinstance(raw, str) else raw
                        print(f"GENERATED IMAGE BYTES: YES ({len(decoded_bytes)} bytes)")
                        print("="*50 + "\n")
                        return Image.open(io.BytesIO(decoded_bytes)).convert("RGB")

            print("GENERATED IMAGE BYTES: NO (No inline image data in response)")
            print("="*50 + "\n")
            return None

        except Exception as e:
            print("GEMINI REQUEST SUCCEEDED: NO")
            print(f"EXACT ERROR ({type(e).__name__}): {e}")
            import traceback
            traceback.print_exc()
            print("="*50 + "\n")
            return None


ai_image_generation_service = AIImageGenerationService()
