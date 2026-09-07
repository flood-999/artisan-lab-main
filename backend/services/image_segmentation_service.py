"""
NIRMAAN - Image Segmentation Service
Removes the background from artisan product photos.

Primary pipeline: rembg (U^2-Net deep-learning matting) detects the true
subject silhouette, then OpenCV cleans up the alpha mask (denoise, close
small holes, feather edges) and sharpens the product itself so the cutout
looks crisp and marketplace-ready instead of a rough crop.

If rembg / OpenCV / numpy aren't installed (or the model can't load, e.g. no
internet on first run to fetch weights), this automatically falls back to the
original lightweight Pillow-only heuristic so the app keeps working.
"""
from PIL import Image, ImageFilter
import math

try:
    import numpy as np
    import cv2
    from rembg import remove as rembg_remove, new_session as rembg_new_session
    _ADVANCED_AVAILABLE = True
except Exception:
    _ADVANCED_AVAILABLE = False

_REMBG_SESSION = None


class ImageSegmentationService:

    @staticmethod
    def _get_session():
        global _REMBG_SESSION
        if _REMBG_SESSION is None:
            # isnet-general-use gives cleaner edges than u2net for varied
            # product photos (pottery, textiles, metal, bamboo, jewelry, etc.)
            _REMBG_SESSION = rembg_new_session("isnet-general-use")
        return _REMBG_SESSION

    @classmethod
    def segment_product(cls, image: Image.Image) -> Image.Image:
        """
        Extracts the product foreground and returns an RGBA image with a
        clean transparent background, ready for marketplace compositing.
        """
        if _ADVANCED_AVAILABLE:
            try:
                return cls._segment_with_rembg_and_opencv(image)
            except Exception as e:
                print(f"[ImageSegmentationService] rembg/OpenCV pipeline failed, using fallback: {e}")
        return cls._segment_with_heuristic(image)

    @classmethod
    def _segment_with_rembg_and_opencv(cls, image: Image.Image) -> Image.Image:
        img_rgba = image.convert("RGBA")

        # 1. rembg (isnet-general-use) - accurate deep-learning foreground/
        #    background split. alpha_matting is deliberately left OFF here:
        #    it needs the extra `pymatting` package, and if that's missing
        #    rembg raises an error that (previously) silently fell back to
        #    the much weaker heuristic cutout below. Plain rembg + the
        #    OpenCV cleanup/feathering in step 2 is reliable without extra
        #    dependencies. If you do have pymatting installed and want the
        #    softer edges, set alpha_matting=True below.
        session = cls._get_session()
        cutout = rembg_remove(
            img_rgba,
            session=session,
            alpha_matting=False,
        )

        rgba_arr = np.array(cutout)  # H x W x 4
        bgr = cv2.cvtColor(rgba_arr[:, :, :3], cv2.COLOR_RGB2BGR)
        alpha = rgba_arr[:, :, 3]

        # 2. OpenCV mask cleanup - remove speckle noise / stray pixels, close
        #    small holes inside the subject, then feather the edge slightly so
        #    the cutout doesn't look "cut with scissors"
        kernel = np.ones((3, 3), np.uint8)
        alpha = cv2.morphologyEx(alpha, cv2.MORPH_OPEN, kernel, iterations=1)
        alpha = cv2.morphologyEx(alpha, cv2.MORPH_CLOSE, kernel, iterations=2)
        alpha = cv2.GaussianBlur(alpha, (5, 5), 0)

        # 3. Unsharp-mask the product pixels themselves so texture and edges
        #    read as crisp / professional rather than soft or muddy
        blurred = cv2.GaussianBlur(bgr, (0, 0), sigmaX=3)
        sharpened_bgr = cv2.addWeighted(bgr, 1.5, blurred, -0.5, 0)
        sharpened_rgb = cv2.cvtColor(sharpened_bgr, cv2.COLOR_BGR2RGB)

        result_arr = np.dstack([sharpened_rgb, alpha])
        return Image.fromarray(result_arr, mode="RGBA")

    @staticmethod
    def _segment_with_heuristic(image: Image.Image) -> Image.Image:
        """
        Fallback edge-preserving background separation (no ML model required).
        Used only if rembg/OpenCV/numpy are unavailable in the environment.
        """
        img_rgba = image.convert("RGBA")
        width, height = img_rgba.size

        corners = [
            img_rgba.getpixel((5, 5)),
            img_rgba.getpixel((width - 6, 5)),
            img_rgba.getpixel((5, height - 6)),
            img_rgba.getpixel((width - 6, height - 6)),
            img_rgba.getpixel((width // 2, 5)),
            img_rgba.getpixel((5, height // 2)),
            img_rgba.getpixel((width - 6, height // 2)),
        ]
        avg_bg_r = sum(c[0] for c in corners) / len(corners)
        avg_bg_g = sum(c[1] for c in corners) / len(corners)
        avg_bg_b = sum(c[2] for c in corners) / len(corners)

        mask = Image.new("L", (width, height), 0)
        cx, cy = width / 2.0, height / 2.0
        max_dist = math.sqrt(cx * cx + cy * cy)

        src_pixels = img_rgba.load()
        mask_pixels = mask.load()

        for y in range(height):
            for x in range(width):
                r, g, b, a = src_pixels[x, y]
                color_dist = math.sqrt((r - avg_bg_r) ** 2 + (g - avg_bg_g) ** 2 + (b - avg_bg_b) ** 2)
                dist_center = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
                center_factor = max(0.0, 1.0 - (dist_center / (max_dist * 0.95)))

                if color_dist > 28 or center_factor > 0.45:
                    alpha_val = min(255, int((color_dist / 65.0) * 200 + (center_factor * 100)))
                    mask_pixels[x, y] = max(0, min(255, alpha_val))
                else:
                    mask_pixels[x, y] = 0

        smoothed_mask = mask.filter(ImageFilter.GaussianBlur(radius=2.5))

        result = Image.new("RGBA", (width, height))
        for y in range(height):
            for x in range(width):
                r, g, b, _ = src_pixels[x, y]
                alpha = smoothed_mask.getpixel((x, y))
                result.putpixel((x, y), (r, g, b, alpha))

        return result


image_segmentation_service = ImageSegmentationService()
