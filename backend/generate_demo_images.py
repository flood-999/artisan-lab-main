"""
Generate demo images for seed products
"""
import os
from PIL import Image, ImageDraw, ImageFont

STATIC_IMG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend", "images")
os.makedirs(STATIC_IMG_DIR, exist_ok=True)

def create_craft_image(filename: str, title: str, bg_color: tuple, fg_color: tuple, accent_color: tuple):
    img = Image.new("RGB", (600, 600), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Soft background gradient & pedestal
    for y in range(600):
        ratio = y / 600.0
        r = int(bg_color[0] * (1.0 - ratio*0.2))
        g = int(bg_color[1] * (1.0 - ratio*0.2))
        b = int(bg_color[2] * (1.0 - ratio*0.2))
        draw.line([(0, y), (600, y)], fill=(r, g, b))
        
    # Pedestal floor
    draw.rectangle([(0, 480), (600, 600)], fill=(int(bg_color[0]*0.85), int(bg_color[1]*0.85), int(bg_color[2]*0.85)))
    
    # Shadow
    draw.ellipse([(140, 470), (460, 520)], fill=(30, 25, 20))
    
    # Main Product Shape (Artisanal Silhouette)
    draw.ellipse([(170, 220), (430, 480)], fill=fg_color, outline=accent_color, width=4)
    # Inner craft texture rings
    draw.ellipse([(200, 250), (400, 450)], fill=None, outline=accent_color, width=2)
    draw.ellipse([(230, 280), (370, 420)], fill=None, outline=accent_color, width=2)
    
    # Text Banner
    draw.rectangle([(50, 50), (550, 110)], fill=(35, 30, 25))
    draw.text((80, 70), title, fill=(255, 250, 240))
    
    path = os.path.join(STATIC_IMG_DIR, filename)
    img.save(path, "JPEG", quality=90)
    print(f"Generated {path}")

# Terracotta Bowl
create_craft_image("terracotta_marketplace.jpg", "Terracotta Bowl - Studio", (245, 240, 235), (196, 92, 54), (140, 60, 30))
create_craft_image("terracotta_original.jpg", "Terracotta Bowl - Original Photo", (210, 205, 195), (196, 92, 54), (140, 60, 30))
create_craft_image("terracotta_lifestyle.jpg", "Terracotta Bowl - Lifestyle", (230, 215, 195), (196, 92, 54), (140, 60, 30))

# Bamboo Basket
create_craft_image("bamboo_marketplace.jpg", "Bamboo Basket - Studio", (248, 246, 240), (198, 164, 98), (140, 110, 60))
create_craft_image("bamboo_original.jpg", "Bamboo Basket - Original Photo", (220, 215, 200), (198, 164, 98), (140, 110, 60))
create_craft_image("bamboo_lifestyle.jpg", "Bamboo Basket - Lifestyle", (235, 238, 220), (198, 164, 98), (140, 110, 60))

# Brass Diya
create_craft_image("diya_marketplace.jpg", "Brass Peacock Diya - Studio", (245, 242, 238), (218, 175, 55), (160, 120, 30))
create_craft_image("diya_original.jpg", "Brass Peacock Diya - Original Photo", (215, 210, 200), (218, 175, 55), (160, 120, 30))
create_craft_image("diya_lifestyle.jpg", "Brass Peacock Diya - Lifestyle", (38, 34, 30), (218, 175, 55), (160, 120, 30))

# Artisan Avatar
avatar = Image.new("RGB", (200, 200), (196, 92, 54))
avatar_draw = ImageDraw.Draw(avatar)
avatar_draw.ellipse([(30, 30), (170, 170)], fill=(250, 240, 230))
avatar_draw.ellipse([(70, 50), (130, 110)], fill=(196, 92, 54))
avatar_draw.ellipse([(45, 120), (155, 200)], fill=(196, 92, 54))
avatar.save(os.path.join(STATIC_IMG_DIR, "artisan_avatar.png"), "PNG")
print("Generated artisan avatar")
