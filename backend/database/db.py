"""
NIRMAAN - Database & Repository Layer
Provides in-memory & SQLite persistence with default artisan profile, sample Indian craft products, and benchmark market datasets.
"""
import sqlite3
import json
import os
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from ..models.schemas import (
    Artisan, Product, ImageInfo, ProductAttribute, Catalog,
    MarketProduct, PriceCalculationResult, MarketPriceCheckResult, PricingInsightResult
)

DB_PATH = os.path.join(os.path.dirname(__file__), "nirmaan.db")

def now_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def now_utc() -> datetime:
    return datetime.now(timezone.utc)

class Database:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_db()
        self._seed_initial_data()

    def _get_conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS artisans (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    phone TEXT,
                    preferred_language TEXT,
                    craft_type TEXT,
                    seller_type TEXT,
                    region TEXT,
                    bio TEXT,
                    avatar_url TEXT,
                    created_at TEXT
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id TEXT PRIMARY KEY,
                    artisan_id TEXT,
                    title_original TEXT,
                    title_hi TEXT,
                    title_en TEXT,
                    description_original TEXT,
                    description_hi TEXT,
                    description_en TEXT,
                    category TEXT,
                    subcategory TEXT,
                    craft_type TEXT,
                    material TEXT,
                    color TEXT,
                    dimensions TEXT,
                    weight TEXT,
                    seo_keywords TEXT,
                    seo_keywords_en TEXT,
                    seo_keywords_hi TEXT,
                    price REAL,
                    currency TEXT,
                    status TEXT,
                    is_handmade INTEGER,
                    images_json TEXT,
                    attributes_json TEXT,
                    created_at TEXT,
                    updated_at TEXT
                )
            """)
            # Lightweight migration: add new columns to a pre-existing DB file
            # without wiping the artisan's saved products.
            cur.execute("PRAGMA table_info(products)")
            existing_cols = {row[1] for row in cur.fetchall()}
            if "seo_keywords_en" not in existing_cols:
                cur.execute("ALTER TABLE products ADD COLUMN seo_keywords_en TEXT")
            if "seo_keywords_hi" not in existing_cols:
                cur.execute("ALTER TABLE products ADD COLUMN seo_keywords_hi TEXT")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS catalogs (
                    id TEXT PRIMARY KEY,
                    artisan_id TEXT,
                    title TEXT NOT NULL,
                    description TEXT,
                    cover_image_url TEXT,
                    is_published INTEGER,
                    product_ids_json TEXT,
                    created_at TEXT
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS market_products (
                    id TEXT PRIMARY KEY,
                    source TEXT,
                    source_product_id TEXT,
                    title TEXT NOT NULL,
                    price REAL NOT NULL,
                    currency TEXT,
                    quantity INTEGER,
                    unit TEXT,
                    image_url TEXT,
                    product_url TEXT,
                    seller TEXT,
                    brand TEXT,
                    rating REAL,
                    review_count INTEGER,
                    availability TEXT,
                    retrieved_at TEXT,
                    is_handmade INTEGER,
                    similarity_score REAL,
                    craft_type TEXT,
                    material TEXT,
                    category TEXT
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS price_calculations (
                    id TEXT PRIMARY KEY,
                    product_id TEXT,
                    data_json TEXT,
                    created_at TEXT
                )
            """)
            conn.commit()

    def _seed_initial_data(self):
        with self._get_conn() as conn:
            cur = conn.cursor()
            
            # 1. Seed Default Artisan
            cur.execute("SELECT COUNT(*) FROM artisans")
            if cur.fetchone()[0] == 0:
                artisan = Artisan(
                    id="artisan-ramesh",
                    name="Rameshwaram Handicrafts (Ramesh Kumar)",
                    phone="+91 98290 12345",
                    preferred_language="hi",
                    craft_type="Terracotta & Pottery",
                    seller_type="Artisan",
                    region="Khurja, Uttar Pradesh",
                    bio="3rd generation master potter specializing in hand-thrown terracotta, natural clay kitchenware, and traditional painted earthen lamps.",
                    avatar_url="/static/images/artisan_avatar.png"
                )
                cur.execute("""
                    INSERT INTO artisans (id, name, phone, preferred_language, craft_type, seller_type, region, bio, avatar_url, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    artisan.id, artisan.name, artisan.phone, artisan.preferred_language,
                    artisan.craft_type, artisan.seller_type, artisan.region, artisan.bio,
                    artisan.avatar_url, artisan.created_at.isoformat()
                ))

            # 2. Seed Initial Products
            cur.execute("SELECT COUNT(*) FROM products")
            if cur.fetchone()[0] == 0:
                sample_products = [
                    {
                        "id": "prod-terracotta-bowl",
                        "artisan_id": "artisan-ramesh",
                        "title_original": "मिट्टी का हस्तनिर्मित बाउल",
                        "title_hi": "हस्तनिर्मित प्राकृतिक टेराकोटा बाउल",
                        "title_en": "Handcrafted Natural Terracotta Serving Bowl",
                        "description_original": "प्राकृतिक शुद्ध लाल मिट्टी से बना हुआ सर्विंग बाउल।",
                        "description_hi": "पारंपरिक कुम्हार कला से शुद्ध जैविक लाल मिट्टी द्वारा चाक पर निर्मित। भोजन परोसने और सजावट के लिए आदर्श।",
                        "description_en": "Hand-thrown on traditional potter's wheel using 100% natural clay. Ideal for serving, curd setting, and rustic home decor.",
                        "category": "Pottery",
                        "subcategory": "Tableware & Bowls",
                        "craft_type": "Terracotta",
                        "material": "Natural Red Clay",
                        "color": "Earthy Terracotta Red",
                        "dimensions": "Diameter: 7 inches, Height: 3.5 inches",
                        "weight": "450g",
                        "seo_keywords": json.dumps(["terracotta bowl", "handmade clay pot", "indian pottery", "eco-friendly tableware", "khurja pottery"]),
                        "seo_keywords_en": json.dumps(["terracotta bowl", "handmade clay pot", "indian pottery", "eco-friendly tableware", "khurja pottery"]),
                        "seo_keywords_hi": json.dumps(["मिट्टी का बर्तन", "हस्तनिर्मित मिट्टी का बाउल", "टेराकोटा कटोरा", "देसी मिट्टी के बर्तन", "पारंपरिक मिट्टी के बर्तन"]),
                        "price": 399.0,
                        "currency": "INR",
                        "status": "published",
                        "is_handmade": 1,
                        "images_json": json.dumps([
                            {"id": "img-1", "image_type": "marketplace", "file_path": "/static/images/terracotta_marketplace.jpg", "url": "/static/images/terracotta_marketplace.jpg", "label": "Marketplace", "is_primary": True},
                            {"id": "img-2", "image_type": "original", "file_path": "/static/images/terracotta_original.jpg", "url": "/static/images/terracotta_original.jpg", "label": "Original", "is_primary": False},
                            {"id": "img-3", "image_type": "lifestyle", "file_path": "/static/images/terracotta_lifestyle.jpg", "url": "/static/images/terracotta_lifestyle.jpg", "label": "Lifestyle", "is_primary": False}
                        ]),
                        "attributes_json": json.dumps([
                            {"key": "craft", "label": "Craft Technique", "value_original": "चाक पर बना", "value_hi": "हाथ से चाक पर घुमाया गया", "value_en": "Wheel-thrown Handcrafted", "confidence": 0.98, "source": "visual"},
                            {"key": "material", "label": "Material", "value_original": "लाल मिट्टी", "value_hi": "शुद्ध टेराकोटा मिट्टी", "value_en": "Pure Terracotta Clay", "confidence": 0.99, "source": "voice"}
                        ]),
                        "created_at": now_utc_iso(),
                        "updated_at": now_utc_iso()
                    },
                    {
                        "id": "prod-bamboo-basket",
                        "artisan_id": "artisan-ramesh",
                        "title_original": "बांस की हाथ से बुनी टोकरी",
                        "title_hi": "प्राकृतिक हस्तनिर्मित बाँस की टोकरी",
                        "title_en": "Handwoven Natural Bamboo Storage Basket",
                        "description_original": "मजबूत प्राकृतिक बांस की पट्टियों से हाथ से बुनी गई टोकरी। फल रखने और सामान रखने के लिए।",
                        "description_hi": "कारीगरों द्वारा प्राकृतिक बाँस की पतली खपच्चियों से हाथ से बुनी टोकरी। रसोई व फलों के लिए टिकाऊ।",
                        "description_en": "Durable and lightweight storage basket handwoven from seasoned natural bamboo cane. Perfect for fresh fruits and kitchen organization.",
                        "category": "Bamboo craft",
                        "subcategory": "Storage & Baskets",
                        "craft_type": "Bamboo Weaving",
                        "material": "Seasoned Bamboo Cane",
                        "color": "Natural Bamboo Gold",
                        "dimensions": "10 x 10 x 4.5 inches",
                        "weight": "280g",
                        "seo_keywords": json.dumps(["bamboo basket", "handwoven basket", "cane storage", "northeast bamboo craft", "natural fruit basket"]),
                        "seo_keywords_en": json.dumps(["bamboo basket", "handwoven basket", "cane storage", "northeast bamboo craft", "natural fruit basket"]),
                        "seo_keywords_hi": json.dumps(["बांस की टोकरी", "हाथ से बुनी टोकरी", "बांस की हस्तनिर्मित टोकरी", "फल रखने की टोकरी", "प्राकृतिक बांस उत्पाद"]),
                        "price": 549.0,
                        "currency": "INR",
                        "status": "published",
                        "is_handmade": 1,
                        "images_json": json.dumps([
                            {"id": "img-4", "image_type": "marketplace", "file_path": "/static/images/bamboo_marketplace.jpg", "url": "/static/images/bamboo_marketplace.jpg", "label": "Marketplace", "is_primary": True},
                            {"id": "img-5", "image_type": "original", "file_path": "/static/images/bamboo_original.jpg", "url": "/static/images/bamboo_original.jpg", "label": "Original", "is_primary": False},
                            {"id": "img-6", "image_type": "lifestyle", "file_path": "/static/images/bamboo_lifestyle.jpg", "url": "/static/images/bamboo_lifestyle.jpg", "label": "Lifestyle", "is_primary": False}
                        ]),
                        "attributes_json": json.dumps([
                            {"key": "material", "label": "Material", "value_original": "प्राकृतिक बांस", "value_hi": "प्राकृतिक बांस", "value_en": "Natural Cane Bamboo", "confidence": 0.99, "source": "voice"}
                        ]),
                        "created_at": now_utc_iso(),
                        "updated_at": now_utc_iso()
                    },
                    {
                        "id": "prod-brass-diya",
                        "artisan_id": "artisan-ramesh",
                        "title_original": "पीतल का मोर दीया",
                        "title_hi": "हस्तनिर्मित पारंपरिक पीतल का मोर दीया",
                        "title_en": "Handcrafted Traditional Brass Peacock Oil Lamp Diya",
                        "description_original": "शुद्ध पीतल से ढलाई करके नक्काशी किया गया मोर दीया। पूजा और त्योहारों के लिए।",
                        "description_hi": "पारंपरिक धातु कारीगरी से निर्मित ठोस पीतल का मोर दीया। पूजा कक्ष और दीपावली उत्सव के लिए शुभ।",
                        "description_en": "Traditional sand-cast solid brass oil lamp featuring detailed peacock engraving and antique golden finish.",
                        "category": "Metal craft",
                        "subcategory": "Religious & Puja Decor",
                        "craft_type": "Brass Dhokra / Sand Casting",
                        "material": "Solid Brass",
                        "color": "Antique Gold",
                        "dimensions": "Height: 6 inches, Base: 3 inches",
                        "weight": "420g",
                        "seo_keywords": json.dumps(["brass diya", "peacock oil lamp", "puja lamp", "traditional brass craft", "diwali diya"]),
                        "seo_keywords_en": json.dumps(["brass diya", "peacock oil lamp", "puja lamp", "traditional brass craft", "diwali diya"]),
                        "seo_keywords_hi": json.dumps(["पीतल का दीया", "मोर दीया", "पूजा का दीया", "पारंपरिक पीतल शिल्प", "दिवाली दीया"]),
                        "price": 799.0,
                        "currency": "INR",
                        "status": "published",
                        "is_handmade": 1,
                        "images_json": json.dumps([
                            {"id": "img-7", "image_type": "marketplace", "file_path": "/static/images/diya_marketplace.jpg", "url": "/static/images/diya_marketplace.jpg", "label": "Marketplace", "is_primary": True},
                            {"id": "img-8", "image_type": "original", "file_path": "/static/images/diya_original.jpg", "url": "/static/images/diya_original.jpg", "label": "Original", "is_primary": False},
                            {"id": "img-9", "image_type": "lifestyle", "file_path": "/static/images/diya_lifestyle.jpg", "url": "/static/images/diya_lifestyle.jpg", "label": "Lifestyle", "is_primary": False}
                        ]),
                        "attributes_json": json.dumps([]),
                        "created_at": now_utc_iso(),
                        "updated_at": now_utc_iso()
                    }
                ]
                for p in sample_products:
                    cur.execute("""
                        INSERT INTO products (
                            id, artisan_id, title_original, title_hi, title_en,
                            description_original, description_hi, description_en,
                            category, subcategory, craft_type, material, color,
                            dimensions, weight, seo_keywords, seo_keywords_en, seo_keywords_hi,
                            price, currency,
                            status, is_handmade, images_json, attributes_json,
                            created_at, updated_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        p["id"], p["artisan_id"], p["title_original"], p["title_hi"], p["title_en"],
                        p["description_original"], p["description_hi"], p["description_en"],
                        p["category"], p["subcategory"], p["craft_type"], p["material"], p["color"],
                        p["dimensions"], p["weight"], p["seo_keywords"], p["seo_keywords_en"], p["seo_keywords_hi"],
                        p["price"], p["currency"],
                        p["status"], p["is_handmade"], p["images_json"], p["attributes_json"],
                        p["created_at"], p["updated_at"]
                    ))

            # 3. Seed Catalogs
            cur.execute("SELECT COUNT(*) FROM catalogs")
            if cur.fetchone()[0] == 0:
                catalogs_data = [
                    {
                        "id": "cat-diwali-special",
                        "artisan_id": "artisan-ramesh",
                        "title": "Diwali Festival & Decor Collection 🪔",
                        "description": "Handcrafted brass lamps, terracotta diyas, and festive decor made for celebration.",
                        "cover_image_url": "/static/images/diya_marketplace.jpg",
                        "is_published": 1,
                        "product_ids_json": json.dumps(["prod-brass-diya", "prod-terracotta-bowl"])
                    },
                    {
                        "id": "cat-natural-living",
                        "artisan_id": "artisan-ramesh",
                        "title": "Natural Earth & Living Collection 🌿",
                        "description": "Sustainable terracotta kitchenware and handwoven bamboo utility items.",
                        "cover_image_url": "/static/images/bamboo_marketplace.jpg",
                        "is_published": 1,
                        "product_ids_json": json.dumps(["prod-terracotta-bowl", "prod-bamboo-basket"])
                    }
                ]
                for c in catalogs_data:
                    cur.execute("""
                        INSERT INTO catalogs (id, artisan_id, title, description, cover_image_url, is_published, product_ids_json, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        c["id"], c["artisan_id"], c["title"], c["description"], c["cover_image_url"],
                        c["is_published"], c["product_ids_json"], now_utc_iso()
                    ))

            # 4. Seed Market Benchmark Products for Intelligence Engine
            cur.execute("SELECT COUNT(*) FROM market_products")
            if cur.fetchone()[0] == 0:
                benchmark_market_items = [
                    # Pottery / Terracotta
                    ("mp-1", "FabIndia", "FAB-101", "Handmade Terracotta Serving Bowl 7 Inch", 399.0, "INR", 1, "piece", "FabIndia Crafts", 4.4, 85, 1, 0.95, "Terracotta", "Clay", "Pottery"),
                    ("mp-2", "Jaypore", "JAY-202", "Earth Clay Hand Thrown Kitchen Bowl", 450.0, "INR", 1, "piece", "Jaypore Artisan Guild", 4.6, 120, 1, 0.92, "Terracotta", "Clay", "Pottery"),
                    ("mp-3", "Amazon Karigar", "AK-303", "Khurja Handcrafted Red Clay Bowl", 349.0, "INR", 1, "piece", "Rural Crafts Producer Co", 4.2, 210, 1, 0.90, "Terracotta", "Clay", "Pottery"),
                    ("mp-4", "Etsy India", "ETSY-404", "Traditional Clay Curd Setting Bowl", 420.0, "INR", 1, "piece", "Mitti Kala Kendra", 4.8, 64, 1, 0.89, "Terracotta", "Clay", "Pottery"),
                    ("mp-5", "Local Market Feed", "LOC-505", "Unglazed Terracotta Bowl Medium", 280.0, "INR", 1, "piece", "Gramin Haat", 4.0, 30, 1, 0.88, "Terracotta", "Clay", "Pottery"),
                    ("mp-6", "Etsy Global Boutique", "ETSY-EXP", "Luxury Antique Finish Terracotta Relic", 4999.0, "INR", 1, "piece", "Heritage Global", 4.9, 12, 1, 0.60, "Terracotta", "Clay", "Pottery"), # Outlier!
                    
                    # Bamboo Craft
                    ("mp-7", "Okhai", "OK-101", "Handwoven Cane Bamboo Storage Basket 10 Inch", 550.0, "INR", 1, "piece", "Assam Cane Artisans SHG", 4.5, 95, 1, 0.94, "Bamboo Weaving", "Bamboo", "Bamboo craft"),
                    ("mp-8", "Tribes India", "TI-202", "North-East Natural Bamboo Fruit Basket", 490.0, "INR", 1, "piece", "TRIFED Tribal Producer", 4.6, 140, 1, 0.93, "Bamboo Weaving", "Bamboo", "Bamboo craft"),
                    ("mp-9", "Jaypore", "JAY-303", "Artisanal Handwoven Bamboo Basket", 650.0, "INR", 1, "piece", "Manipur Craft Cluster", 4.7, 72, 1, 0.91, "Bamboo Weaving", "Bamboo", "Bamboo craft"),
                    ("mp-10", "Amazon Karigar", "AK-404", "Eco-friendly Cane Bamboo Utility Basket", 520.0, "INR", 1, "piece", "Rural Cane Guild", 4.3, 180, 1, 0.90, "Bamboo Weaving", "Bamboo", "Bamboo craft"),
                    ("mp-11", "Plastic Co Wholesale", "PLAS-01", "Plastic Imitation Bamboo Look Basket 4-Pack", 199.0, "INR", 1, "piece", "Industrial Poly Mart", 3.2, 400, 0, 0.40, "Mass Molded", "Plastic", "Bamboo craft"), # Mass-produced!
                    
                    # Brass Diya / Metal Craft
                    ("mp-12", "Poompuhar", "POOM-101", "Solid Brass Peacock Diya Handcrafted 6 Inch", 850.0, "INR", 1, "piece", "Tamil Nadu Handicrafts Corp", 4.7, 110, 1, 0.96, "Sand Casting", "Brass", "Metal craft"),
                    ("mp-13", "Craftsvilla", "CV-202", "Traditional Brass Oil Lamp Mayur Diya", 750.0, "INR", 1, "piece", "Moradabad Brass Works", 4.4, 230, 1, 0.94, "Sand Casting", "Brass", "Metal craft"),
                    ("mp-14", "Jaypore", "JAY-404", "Cast Brass Antique Peacock Lamp", 920.0, "INR", 1, "piece", "Swarna Craft Heritage", 4.8, 65, 1, 0.91, "Sand Casting", "Brass", "Metal craft"),
                    ("mp-15", "Amazon Karigar", "AK-505", "Handmade Brass Diya with Engraved Stand", 799.0, "INR", 1, "piece", "Artisan Brass Cluster", 4.5, 340, 1, 0.93, "Sand Casting", "Brass", "Metal craft"),
                    ("mp-16", "Direct Import Co", "IMP-99", "Sheet Metal Machine Stamped Diya Set", 250.0, "INR", 1, "piece", "Factory Metal Corp", 3.5, 500, 0, 0.45, "Machine Stamped", "Alloy", "Metal craft"), # Mass produced!
                    
                    # Handloom & Textiles
                    ("mp-17", "FabIndia", "FAB-TEX-1", "Handloom Cotton Saree with Zari Border", 1850.0, "INR", 1, "piece", "Chanderi Weavers Co-op", 4.6, 310, 1, 0.95, "Handloom Weaving", "Pure Cotton", "Textiles"),
                    ("mp-18", "Jaypore", "JAY-TEX-2", "Handwoven Chanderi Saree with Zari", 2200.0, "INR", 1, "piece", "Madhya Pradesh Weavers", 4.8, 95, 1, 0.93, "Handloom Weaving", "Cotton Silk", "Textiles"),
                    ("mp-19", "Tribes India", "TI-TEX-3", "Traditional Handloom Saree Natural Dye", 1650.0, "INR", 1, "piece", "Tribal Weavers Society", 4.5, 140, 1, 0.90, "Handloom Weaving", "Organic Cotton", "Textiles"),

                    # Woodcraft
                    ("mp-20", "FabIndia", "FAB-WD-1", "Hand Carved Sheesham Wood Serving Tray", 890.0, "INR", 1, "piece", "Saharanpur Wood Artisans", 4.6, 115, 1, 0.94, "Wood Carving", "Sheesham Wood", "Woodcraft"),
                    ("mp-21", "Jaypore", "JAY-WD-2", "Artisanal Wooden Spice Box with Brass Inlay", 1150.0, "INR", 1, "piece", "Rajasthan Wood Guild", 4.7, 88, 1, 0.92, "Wood Carving", "Teak Wood", "Woodcraft"),
                    ("mp-22", "Amazon Karigar", "AK-WD-3", "Handmade Natural Wood Kitchen Bowl", 650.0, "INR", 1, "piece", "Rural Wood Cluster", 4.3, 140, 1, 0.90, "Wood Carving", "Mango Wood", "Woodcraft"),

                    # Handmade Jewellery
                    ("mp-23", "Jaypore", "JAY-JWL-1", "Handcrafted Terracotta Necklace with Jhumkas", 550.0, "INR", 1, "piece", "Bengal Terracotta Artisans", 4.5, 92, 1, 0.94, "Terracotta Jewellery", "Natural Clay", "Jewellery"),
                    ("mp-24", "Okhai", "OK-JWL-2", "Traditional Brass Handcrafted Drop Earrings", 480.0, "INR", 1, "piece", "Tribal Jewellery SHG", 4.6, 130, 1, 0.93, "Filigree & Casting", "Brass", "Jewellery"),
                    ("mp-25", "FabIndia", "FAB-JWL-3", "Handmade Tribal Beaded Artisan Choker", 750.0, "INR", 1, "piece", "Northeast Crafts Co-op", 4.7, 75, 1, 0.91, "Beadwork", "Glass Beads", "Jewellery"),

                    # Paintings & Folk Art
                    ("mp-26", "Craftsvilla", "CV-PNT-1", "Original Madhubani Folk Art Painting Canvas", 1250.0, "INR", 1, "piece", "Mithila Artisans Collective", 4.8, 160, 1, 0.95, "Folk Painting", "Handmade Paper", "Paintings"),
                    ("mp-27", "Tribes India", "TI-PNT-2", "Traditional Warli Tribal Art Hand Painted Canvas", 950.0, "INR", 1, "piece", "Maharashtra Tribal Guild", 4.6, 105, 1, 0.92, "Folk Painting", "Cotton Canvas", "Paintings"),

                    # Leather & Jute
                    ("mp-28", "FabIndia", "FAB-JT-1", "Eco-friendly Handcrafted Jute Tote Bag", 499.0, "INR", 1, "piece", "Kolkata Jute SHG", 4.4, 210, 1, 0.93, "Jute Braiding", "Natural Jute", "Leather & Jute"),
                    ("mp-29", "Jaypore", "JAY-LTH-2", "Handcrafted Genuine Leather Journal Diary", 850.0, "INR", 1, "piece", "Santiniketan Leather Guild", 4.7, 95, 1, 0.91, "Leather Craft", "Vegetable Tanned Leather", "Leather & Jute")
                ]
                for item in benchmark_market_items:
                    cur.execute("""
                        INSERT OR REPLACE INTO market_products (
                            id, source, source_product_id, title, price, currency, quantity, unit,
                            seller, rating, review_count, is_handmade, similarity_score,
                            craft_type, material, category, retrieved_at, availability
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7],
                        item[8], item[9], item[10], item[11], item[12],
                        item[13], item[14], item[15], now_utc_iso(), "in_stock"
                    ))

            conn.commit()

    # --- Artisan Methods ---
    def get_artisan(self, artisan_id: str = "artisan-ramesh") -> Optional[Artisan]:
        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM artisans WHERE id = ?", (artisan_id,))
            row = cur.fetchone()
            if not row:
                cur.execute("SELECT * FROM artisans LIMIT 1")
                row = cur.fetchone()
            if row:
                return Artisan(
                    id=row["id"],
                    name=row["name"],
                    phone=row["phone"],
                    preferred_language=row["preferred_language"],
                    craft_type=row["craft_type"],
                    seller_type=row["seller_type"],
                    region=row["region"],
                    bio=row["bio"],
                    avatar_url=row["avatar_url"],
                    created_at=datetime.fromisoformat(row["created_at"]) if row["created_at"] else now_utc()
                )
        return None

    def update_artisan(self, artisan: Artisan) -> Artisan:
        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                UPDATE artisans SET
                    name = ?, phone = ?, preferred_language = ?,
                    craft_type = ?, seller_type = ?, region = ?,
                    bio = ?, avatar_url = ?
                WHERE id = ?
            """, (
                artisan.name, artisan.phone, artisan.preferred_language,
                artisan.craft_type, artisan.seller_type, artisan.region,
                artisan.bio, artisan.avatar_url, artisan.id
            ))
            conn.commit()
        return artisan

    # --- Product Methods ---
    def get_products(self, artisan_id: Optional[str] = None, status: Optional[str] = None) -> List[Product]:
        with self._get_conn() as conn:
            cur = conn.cursor()
            query = "SELECT * FROM products WHERE 1=1"
            params = []
            if artisan_id:
                query += " AND artisan_id = ?"
                params.append(artisan_id)
            if status:
                query += " AND status = ?"
                params.append(status)
            query += " ORDER BY created_at DESC"
            cur.execute(query, params)
            rows = cur.fetchall()
            products = []
            for r in rows:
                images = [ImageInfo(**img) for img in json.loads(r["images_json"] or "[]")]
                attributes = [ProductAttribute(**attr) for attr in json.loads(r["attributes_json"] or "[]")]
                keywords = json.loads(r["seo_keywords"] or "[]")
                keywords_en = json.loads(r["seo_keywords_en"] or "[]") if r["seo_keywords_en"] else keywords
                keywords_hi = json.loads(r["seo_keywords_hi"] or "[]") if r["seo_keywords_hi"] else []
                products.append(Product(
                    id=r["id"],
                    artisan_id=r["artisan_id"],
                    title_original=r["title_original"] or "",
                    title_hi=r["title_hi"] or "",
                    title_en=r["title_en"] or "",
                    description_original=r["description_original"] or "",
                    description_hi=r["description_hi"] or "",
                    description_en=r["description_en"] or "",
                    category=r["category"] or "Handicrafts",
                    subcategory=r["subcategory"] or "General",
                    craft_type=r["craft_type"] or "Handmade",
                    material=r["material"] or "Natural Material",
                    color=r["color"],
                    dimensions=r["dimensions"],
                    weight=r["weight"],
                    seo_keywords=keywords,
                    seo_keywords_en=keywords_en,
                    seo_keywords_hi=keywords_hi,
                    price=r["price"],
                    currency=r["currency"] or "INR",
                    status=r["status"] or "draft",
                    is_handmade=bool(r["is_handmade"]),
                    images=images,
                    attributes=attributes,
                    created_at=datetime.fromisoformat(r["created_at"]) if r["created_at"] else now_utc(),
                    updated_at=datetime.fromisoformat(r["updated_at"]) if r["updated_at"] else now_utc()
                ))
            return products

    def get_product(self, product_id: str) -> Optional[Product]:
        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM products WHERE id = ?", (product_id,))
            r = cur.fetchone()
            if r:
                images = [ImageInfo(**img) for img in json.loads(r["images_json"] or "[]")]
                attributes = [ProductAttribute(**attr) for attr in json.loads(r["attributes_json"] or "[]")]
                keywords = json.loads(r["seo_keywords"] or "[]")
                keywords_en = json.loads(r["seo_keywords_en"] or "[]") if r["seo_keywords_en"] else keywords
                keywords_hi = json.loads(r["seo_keywords_hi"] or "[]") if r["seo_keywords_hi"] else []
                return Product(
                    id=r["id"],
                    artisan_id=r["artisan_id"],
                    title_original=r["title_original"] or "",
                    title_hi=r["title_hi"] or "",
                    title_en=r["title_en"] or "",
                    description_original=r["description_original"] or "",
                    description_hi=r["description_hi"] or "",
                    description_en=r["description_en"] or "",
                    category=r["category"] or "Handicrafts",
                    subcategory=r["subcategory"] or "General",
                    craft_type=r["craft_type"] or "Handmade",
                    material=r["material"] or "Natural Material",
                    color=r["color"],
                    dimensions=r["dimensions"],
                    weight=r["weight"],
                    seo_keywords=keywords,
                    seo_keywords_en=keywords_en,
                    seo_keywords_hi=keywords_hi,
                    price=r["price"],
                    currency=r["currency"] or "INR",
                    status=r["status"] or "draft",
                    is_handmade=bool(r["is_handmade"]),
                    images=images,
                    attributes=attributes,
                    created_at=datetime.fromisoformat(r["created_at"]) if r["created_at"] else now_utc(),
                    updated_at=datetime.fromisoformat(r["updated_at"]) if r["updated_at"] else now_utc()
                )
        return None

    def save_product(self, product: Product) -> Product:
        with self._get_conn() as conn:
            cur = conn.cursor()
            images_json = json.dumps([img.model_dump(mode="json") for img in product.images])
            attributes_json = json.dumps([attr.model_dump(mode="json") for attr in product.attributes])
            keywords_json = json.dumps(product.seo_keywords)
            keywords_en_json = json.dumps(product.seo_keywords_en or product.seo_keywords)
            keywords_hi_json = json.dumps(product.seo_keywords_hi)
            cur.execute("""
                INSERT OR REPLACE INTO products (
                    id, artisan_id, title_original, title_hi, title_en,
                    description_original, description_hi, description_en,
                    category, subcategory, craft_type, material, color,
                    dimensions, weight, seo_keywords, seo_keywords_en, seo_keywords_hi,
                    price, currency,
                    status, is_handmade, images_json, attributes_json,
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                product.id, product.artisan_id, product.title_original, product.title_hi, product.title_en,
                product.description_original, product.description_hi, product.description_en,
                product.category, product.subcategory, product.craft_type, product.material, product.color,
                product.dimensions, product.weight, keywords_json, keywords_en_json, keywords_hi_json,
                product.price, product.currency,
                product.status, 1 if product.is_handmade else 0, images_json, attributes_json,
                product.created_at.isoformat(), now_utc_iso()
            ))
            conn.commit()
        return product

    # --- Catalog Methods ---
    def get_catalogs(self, artisan_id: Optional[str] = None) -> List[Catalog]:
        with self._get_conn() as conn:
            cur = conn.cursor()
            query = "SELECT * FROM catalogs"
            params = []
            if artisan_id:
                query += " WHERE artisan_id = ?"
                params.append(artisan_id)
            query += " ORDER BY created_at DESC"
            cur.execute(query, params)
            rows = cur.fetchall()
            catalogs = []
            for r in rows:
                prod_ids = json.loads(r["product_ids_json"] or "[]")
                products = []
                for pid in prod_ids:
                    p = self.get_product(pid)
                    if p:
                        products.append(p)
                catalogs.append(Catalog(
                    id=r["id"],
                    artisan_id=r["artisan_id"],
                    title=r["title"],
                    description=r["description"],
                    cover_image_url=r["cover_image_url"],
                    is_published=bool(r["is_published"]),
                    products=products,
                    created_at=datetime.fromisoformat(r["created_at"]) if r["created_at"] else now_utc()
                ))
            return catalogs

    def save_catalog(self, catalog: Catalog, product_ids: List[str]) -> Catalog:
        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT OR REPLACE INTO catalogs (
                    id, artisan_id, title, description, cover_image_url, is_published, product_ids_json, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                catalog.id, catalog.artisan_id, catalog.title, catalog.description, catalog.cover_image_url,
                1 if catalog.is_published else 0, json.dumps(product_ids), catalog.created_at.isoformat()
            ))
            conn.commit()
        return self.get_catalogs(catalog.artisan_id)[0]

    # --- Market Products Queries ---
    def search_market_products(self, category: str, craft_type: Optional[str] = None, material: Optional[str] = None) -> List[MarketProduct]:
        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT * FROM market_products
                WHERE category LIKE ? OR craft_type LIKE ? OR material LIKE ? OR title LIKE ? OR title LIKE ?
                ORDER BY rating DESC, review_count DESC
            """, (f"%{category}%", f"%{craft_type or ''}%", f"%{material or ''}%", f"%{category}%", f"%{craft_type or ''}%"))
            rows = cur.fetchall()
            
            if len(rows) < 3:
                cur.execute("SELECT * FROM market_products ORDER BY similarity_score DESC LIMIT 10")
                rows = cur.fetchall()

            return [
                MarketProduct(
                    source=r["source"],
                    source_product_id=r["source_product_id"],
                    title=r["title"],
                    price=r["price"],
                    currency=r["currency"] or "INR",
                    quantity=r["quantity"] or 1,
                    unit=r["unit"] or "piece",
                    image_url=r["image_url"],
                    product_url=r["product_url"],
                    seller=r["seller"],
                    brand=r["brand"],
                    rating=r["rating"] or 4.5,
                    review_count=r["review_count"] or 50,
                    availability=r["availability"] or "in_stock",
                    retrieved_at=r["retrieved_at"] or now_utc_iso(),
                    is_handmade=bool(r["is_handmade"]),
                    similarity_score=r["similarity_score"] or 0.85,
                    craft_type=r["craft_type"],
                    material=r["material"],
                    category=r["category"] or "Handicrafts"
                ) for r in rows
            ]

db = Database()
