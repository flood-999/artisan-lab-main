"""
NIRMAAN - Background Generation Service
Intelligently creates craft-specific studio backdrops and contextual lifestyle environments.
Renders realistic soft contact shadows beneath products.
"""
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageFont, ImageChops
import math
import os
import textwrap

_FONT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "fonts")


def _load_font(name: str, size: int):
    """Loads a bundled TTF so text rendering works the same on every OS
    (doesn't depend on fonts happening to be installed on the host)."""
    try:
        return ImageFont.truetype(os.path.join(_FONT_DIR, name), size)
    except Exception:
        return ImageFont.load_default()

class BackgroundGenerationService:
    THEMES = {
        "pottery": {
            "studio_top": (248, 245, 240),
            "studio_bottom": (230, 222, 212),
            "pedestal": (218, 208, 195),
            "lifestyle_top": (238, 226, 210),
            "lifestyle_bottom": (196, 172, 148),
            "accent": (184, 92, 56)  # Terracotta accent
        },
        "textiles": {
            "studio_top": (250, 249, 246),
            "studio_bottom": (235, 232, 228),
            "pedestal": (224, 220, 215),
            "lifestyle_top": (242, 238, 232),
            "lifestyle_bottom": (210, 202, 192),
            "accent": (140, 110, 80)
        },
        "bamboo": {
            "studio_top": (248, 247, 242),
            "studio_bottom": (232, 230, 220),
            "pedestal": (215, 212, 198),
            "lifestyle_top": (236, 238, 224),
            "lifestyle_bottom": (195, 202, 180),
            "accent": (85, 107, 47)  # Organic leaf green
        },
        "metal": {
            "studio_top": (245, 244, 240),
            "studio_bottom": (225, 222, 215),
            "pedestal": (205, 200, 190),
            "lifestyle_top": (42, 38, 34),
            "lifestyle_bottom": (24, 20, 18),
            "accent": (212, 175, 55)  # Brass gold glow
        },
        "jewellery": {
            "studio_top": (252, 252, 252),
            "studio_bottom": (238, 238, 240),
            "pedestal": (225, 225, 228),
            "lifestyle_top": (36, 32, 38),
            "lifestyle_bottom": (18, 16, 22),
            "accent": (220, 180, 70)
        },
        "woodcraft": {
            "studio_top": (248, 245, 238),
            "studio_bottom": (230, 224, 212),
            "pedestal": (212, 204, 190),
            "lifestyle_top": (235, 220, 200),
            "lifestyle_bottom": (180, 155, 125),
            "accent": (120, 70, 35)
        },
        "default": {
            "studio_top": (250, 248, 245),
            "studio_bottom": (232, 228, 222),
            "pedestal": (218, 214, 206),
            "lifestyle_top": (240, 236, 230),
            "lifestyle_bottom": (205, 198, 188),
            "accent": (160, 140, 120)
        }
    }

    @classmethod
    def _get_theme_for_category(cls, category: str, craft_type: str = "") -> dict:
        text = f"{category} {craft_type}".lower()
        if any(w in text for w in ["pottery", "terracotta", "clay", "mitti"]):
            return cls.THEMES["pottery"]
        elif any(w in text for w in ["textile", "saree", "handloom", "cloth", "fabric", "chanderi", "cotton"]):
            return cls.THEMES["textiles"]
        elif any(w in text for w in ["bamboo", "cane", "jute", "grass", "basket"]):
            return cls.THEMES["bamboo"]
        elif any(w in text for w in ["metal", "brass", "diya", "bronze", "copper", "dhokra"]):
            return cls.THEMES["metal"]
        elif any(w in text for w in ["jewel", "necklace", "earring", "bangle", "silver", "gold"]):
            return cls.THEMES["jewellery"]
        elif any(w in text for w in ["wood", "carving", "wooden", "timber"]):
            return cls.THEMES["woodcraft"]
        return cls.THEMES["default"]

    @classmethod
    def create_marketplace_image(
        cls,
        foreground_rgba: Image.Image,
        category: str = "Handicrafts",
        craft_type: str = ""
    ) -> Image.Image:
        """
        Creates professional studio marketplace photo with clean gradient, subtle studio floor pedestal,
        and natural contact drop shadow.
        """
        theme = cls._get_theme_for_category(category, craft_type)
        width, height = foreground_rgba.size
        
        # 1. Create clean studio gradient background
        bg = Image.new("RGB", (width, height), theme["studio_top"])
        draw = ImageDraw.Draw(bg)
        
        r1, g1, b1 = theme["studio_top"]
        r2, g2, b2 = theme["studio_bottom"]
        for y in range(height):
            ratio = y / float(height)
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))

        # 2. Add subtle studio floor perspective line in lower 25%
        floor_y = int(height * 0.78)
        pr, pg, pb = theme["pedestal"]
        draw.rectangle([(0, floor_y), (width, height)], fill=(pr, pg, pb))
        
        # Smooth the horizon line
        bg = bg.filter(ImageFilter.GaussianBlur(radius=1.5))

        # 3. Create realistic soft contact drop shadow under the product
        shadow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        
        # Shadow ellipse placed under product bottom
        cx = width // 2
        cy = int(height * 0.80)
        rx = int(width * 0.36)
        ry = int(height * 0.08)
        
        shadow_draw.ellipse(
            [(cx - rx, cy - ry), (cx + rx, cy + ry)],
            fill=(20, 20, 25, 110)
        )
        shadow_blurred = shadow.filter(ImageFilter.GaussianBlur(radius=18.0))
        
        # 4. Composite: Background + Shadow + Authentic Product Foreground
        result = bg.convert("RGBA")
        result.alpha_composite(shadow_blurred)
        result.alpha_composite(foreground_rgba)
        
        return result.convert("RGB")

    @classmethod
    def create_professional_studio_image(
        cls,
        foreground_rgba: Image.Image,
    ) -> Image.Image:
        """
        Local (non-AI) fallback for the "Professional Studio" black-
        background look: deep black gradient backdrop, a soft mirrored
        reflection of the product beneath it, and a subtle radial glow
        behind the product for a premium/jewellery-style shine.
        """
        width, height = foreground_rgba.size

        # 1. Near-black gradient background (slightly lighter at the
        #    center for a soft studio glow, darker at the edges).
        bg = Image.new("RGB", (width, height), (8, 8, 10))
        draw = ImageDraw.Draw(bg)
        for y in range(height):
            ratio = y / float(height)
            shade = int(14 + 10 * (1 - abs(ratio - 0.35) * 1.5))
            shade = max(4, min(shade, 26))
            draw.line([(0, y), (width, y)], fill=(shade, shade, shade + 2))

        # 2. Soft radial highlight glow behind the product (the "shine").
        glow = Image.new("L", (width, height), 0)
        glow_draw = ImageDraw.Draw(glow)
        cx, cy = width // 2, int(height * 0.42)
        gr = int(width * 0.45)
        glow_draw.ellipse([(cx - gr, cy - gr), (cx + gr, cy + gr)], fill=90)
        glow = glow.filter(ImageFilter.GaussianBlur(radius=gr * 0.5))
        glow_rgb = Image.merge("RGB", (glow, glow, glow.point(lambda p: min(255, int(p * 1.05)))))
        bg = Image.blend(bg, glow_rgb, alpha=0.35)

        result = bg.convert("RGBA")

        # 3. Mirrored floor reflection of the product itself, faded out
        #    with a vertical gradient so it reads as a glossy reflection.
        reflection = foreground_rgba.transpose(Image.FLIP_TOP_BOTTOM).copy()
        alpha = reflection.split()[3]
        fade = Image.new("L", reflection.size, 0)
        fade_draw = ImageDraw.Draw(fade)
        fh = reflection.size[1]
        for y in range(fh):
            fade_val = int(140 * (1 - (y / float(fh))))
            fade_draw.line([(0, y), (reflection.size[0], y)], fill=max(0, fade_val))
        reflection.putalpha(ImageChops.multiply(alpha, fade))
        reflection = reflection.filter(ImageFilter.GaussianBlur(radius=2.5))

        reflect_offset_y = int(height * 0.62)
        result.alpha_composite(reflection, dest=(0, reflect_offset_y))

        # 4. Soft contact shadow, then the authentic product on top.
        shadow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        cx = width // 2
        cy = int(height * 0.80)
        rx = int(width * 0.34)
        ry = int(height * 0.06)
        shadow_draw.ellipse([(cx - rx, cy - ry), (cx + rx, cy + ry)], fill=(0, 0, 0, 160))
        shadow = shadow.filter(ImageFilter.GaussianBlur(radius=16.0))
        result.alpha_composite(shadow)
        result.alpha_composite(foreground_rgba)

        return result.convert("RGB")

    @classmethod
    def create_lifestyle_image(
        cls,
        foreground_rgba: Image.Image,
        category: str = "Handicrafts",
        craft_type: str = ""
    ) -> Image.Image:
        """
        Creates contextual atmospheric lifestyle photo showing the authentic product in a premium warm setting.
        """
        theme = cls._get_theme_for_category(category, craft_type)
        width, height = foreground_rgba.size
        
        # 1. Atmospheric ambient background
        bg = Image.new("RGB", (width, height), theme["lifestyle_top"])
        draw = ImageDraw.Draw(bg)
        
        r1, g1, b1 = theme["lifestyle_top"]
        r2, g2, b2 = theme["lifestyle_bottom"]
        for y in range(height):
            ratio = y / float(height)
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))

        # 2. Warm ambient sunlight ray / vignette overlay
        accent = theme["accent"]
        overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        
        # Soft warm sun highlight in top corner
        overlay_draw.ellipse(
            [(-int(width*0.2), -int(height*0.2)), (int(width*0.7), int(height*0.6))],
            fill=(accent[0], accent[1], accent[2], 45)
        )
        overlay_blurred = overlay.filter(ImageFilter.GaussianBlur(radius=35.0))

        # 3. Floor shadow
        shadow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        cx = width // 2
        cy = int(height * 0.81)
        rx = int(width * 0.40)
        ry = int(height * 0.09)
        shadow_draw.ellipse(
            [(cx - rx, cy - ry), (cx + rx, cy + ry)],
            fill=(15, 12, 10, 130)
        )
        shadow_blurred = shadow.filter(ImageFilter.GaussianBlur(radius=22.0))

        # 4. Composite
        result = bg.convert("RGBA")
        result.alpha_composite(overlay_blurred)
        result.alpha_composite(shadow_blurred)
        result.alpha_composite(foreground_rgba)
        
        return result.convert("RGB")

    @classmethod
    def create_styled_backdrop(
        cls,
        foreground_rgba: Image.Image,
        style_preset: str = "clean_studio"
    ) -> Image.Image:
        """
        Renders a specific studio environment:
        - clean_studio: Minimal clean white/neutral backdrop with floor shadow
        - warm_wood: Rustic wooden tabletop with warm directional lighting
        - earthy_haat: Raw terracotta clay tones and organic artisan ambience
        - festive_amber: Warm evening festive glow for brass/puja items
        - organic_green: Fresh bamboo and botanical greens
        """
        style = style_preset.lower()
        if "wood" in style:
            return cls.create_lifestyle_image(foreground_rgba, category="woodcraft")
        elif "earth" in style or "clay" in style or "haat" in style:
            return cls.create_lifestyle_image(foreground_rgba, category="pottery")
        elif "festive" in style or "amber" in style or "brass" in style:
            return cls.create_lifestyle_image(foreground_rgba, category="metal")
        elif "green" in style or "nature" in style or "bamboo" in style:
            return cls.create_lifestyle_image(foreground_rgba, category="bamboo")
        else:
            return cls.create_marketplace_image(foreground_rgba, category="default")

    @classmethod
    def create_feature_highlight_image(
        cls,
        top_image: Image.Image,
        features: list,
        category: str = "Handicrafts",
        craft_type: str = "",
        title: str = ""
    ) -> Image.Image:
        """
        Creates a market-brand-style "feature highlight" card: the product
        up top, and a polished bullet-point panel below listing the real
        features the artisan actually described in their voice recording
        (falls back to attribute-based bullets if none were extracted).
        Square 1080x1080 canvas to match the app's image viewer.

        `top_image` can be EITHER a transparent RGBA cutout (a fresh studio
        backdrop + soft contact shadow is generated behind it), OR an
        already-finished RGB photo such as the Marketplace image (it's
        simply fitted into the top zone as-is). Features are usually only
        known after the voice step, i.e. after the Marketplace image
        already exists, so the RGB path is what's normally used.
        """
        theme = cls._get_theme_for_category(category, craft_type)
        C = 1080
        product_zone_h = int(C * 0.56)
        panel_top = product_zone_h

        canvas = Image.new("RGB", (C, C), (255, 255, 255))

        if top_image.mode == "RGBA":
            # 1a. Studio-style top zone built from scratch around a transparent cutout
            top_bg = Image.new("RGB", (C, product_zone_h), theme["studio_top"])
            draw = ImageDraw.Draw(top_bg)
            r1, g1, b1 = theme["studio_top"]
            r2, g2, b2 = theme["studio_bottom"]
            for y in range(product_zone_h):
                ratio = y / float(product_zone_h)
                r = int(r1 + (r2 - r1) * ratio)
                g = int(g1 + (g2 - g1) * ratio)
                b = int(b1 + (b2 - b1) * ratio)
                draw.line([(0, y), (C, y)], fill=(r, g, b))
            canvas.paste(top_bg, (0, 0))

            prod = top_image.copy()
            max_w, max_h = int(C * 0.72), int(product_zone_h * 0.82)
            scale = min(max_w / prod.width, max_h / prod.height)
            prod = prod.resize(
                (max(1, int(prod.width * scale)), max(1, int(prod.height * scale))),
                Image.Resampling.LANCZOS,
            )
            px = (C - prod.width) // 2
            py = int(product_zone_h * 0.06) + (max_h - prod.height) // 2

            shadow = Image.new("RGBA", (C, C), (0, 0, 0, 0))
            shadow_draw = ImageDraw.Draw(shadow)
            cx = C // 2
            cy = py + prod.height - 6
            rx, ry = int(prod.width * 0.38), int(C * 0.025)
            shadow_draw.ellipse([(cx - rx, cy - ry), (cx + rx, cy + ry)], fill=(20, 20, 25, 100))
            shadow = shadow.filter(ImageFilter.GaussianBlur(radius=14))

            canvas = canvas.convert("RGBA")
            canvas.alpha_composite(shadow)
            canvas.alpha_composite(prod, (px, py))
            canvas = canvas.convert("RGB")
        else:
            # 1b. Already-finished RGB photo (e.g. the Marketplace image) —
            #     just fit it into the top zone, no re-compositing needed.
            top_bg = Image.new("RGB", (C, product_zone_h), theme["studio_top"])
            img = top_image.convert("RGB")
            scale = min(C / img.width, product_zone_h / img.height)
            new_w, new_h = max(1, int(img.width * scale)), max(1, int(img.height * scale))
            img_resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
            top_bg.paste(img_resized, ((C - new_w) // 2, (product_zone_h - new_h) // 2))
            canvas.paste(top_bg, (0, 0))

        # 2. Bottom feature panel — clean card with checkmark bullets,
        #    styled like a marketplace "About this item" callout block
        draw = ImageDraw.Draw(canvas)
        draw.rectangle([(0, panel_top), (C, C)], fill=(255, 255, 255))
        accent = theme["accent"]
        draw.rectangle([(0, panel_top), (C, panel_top + 4)], fill=accent)

        heading_font = _load_font("DejaVuSans-Bold.ttf", 34)
        body_font = _load_font("DejaVuSans.ttf", 26)

        pad_x = 56
        y_cursor = panel_top + 30
        if title:
            wrapped_title = textwrap.wrap(title, width=34)[:2]
            for line in wrapped_title:
                draw.text((pad_x, y_cursor), line, font=heading_font, fill=(30, 26, 20))
                y_cursor += 42
            y_cursor += 8

        draw.text((pad_x, y_cursor), "Why you'll love it", font=heading_font, fill=accent)
        y_cursor += 52

        clean_features = [f.strip() for f in (features or []) if f and f.strip()]
        if not clean_features:
            clean_features = [
                f"100% authentic {craft_type or 'handmade'} craftsmanship",
                f"Made from genuine {category.lower() if category else 'natural material'}",
                "Every piece is unique — small natural variations are part of the charm",
                "Carefully packaged for safe delivery",
            ]
        clean_features = clean_features[:5]

        available_h = C - 24 - y_cursor
        row_h = max(38, available_h // max(1, len(clean_features)))

        for feature in clean_features:
            bullet_cy = y_cursor + 16
            draw.ellipse([(pad_x, bullet_cy - 12), (pad_x + 24, bullet_cy + 12)], fill=accent)
            draw.line([(pad_x + 6, bullet_cy), (pad_x + 11, bullet_cy + 6), (pad_x + 18, bullet_cy - 7)],
                      fill=(255, 255, 255), width=3)

            wrapped = textwrap.wrap(feature, width=52)[:2]
            line_y = y_cursor
            for line in wrapped:
                draw.text((pad_x + 40, line_y), line, font=body_font, fill=(50, 44, 36))
                line_y += 32
            y_cursor += row_h

        return canvas

background_generation_service = BackgroundGenerationService()
