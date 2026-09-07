"""
NIRMAAN - Pydantic Data Models & Schemas
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, timezone
import uuid

def current_utc_time() -> datetime:
    return datetime.now(timezone.utc)

def current_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

# --- User & Artisan Schemas ---
class ArtisanBase(BaseModel):
    name: str = "Ramesh Kumar"
    phone: Optional[str] = "+91 98765 43210"
    preferred_language: str = "hi"
    craft_type: str = "Pottery"
    seller_type: str = "Artisan"  # Artisan, SHG, Farmer, Small Seller, Other
    region: Optional[str] = "Jaipur, Rajasthan"
    bio: Optional[str] = "Master craftsman with over 15 years of experience creating traditional terracotta and hand-painted pottery."
    avatar_url: Optional[str] = None

class ArtisanCreate(ArtisanBase):
    pass

class Artisan(ArtisanBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=current_utc_time)

    model_config = ConfigDict(from_attributes=True)


# --- Product & Image Schemas ---
class ImageInfo(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    product_id: Optional[str] = None
    image_type: str = "marketplace"  # "original", "marketplace", "features", "lifestyle", "detail", "side", "in_hand"
    file_path: str = ""
    url: str = ""
    label: str = "Marketplace"
    is_primary: bool = False
    created_at: datetime = Field(default_factory=current_utc_time)

class ProductAttribute(BaseModel):
    key: str
    label: str
    value_original: str
    value_hi: Optional[str] = None
    value_en: Optional[str] = None
    confidence: float = 1.0
    source: str = "visual"  # visual, voice, manual

class ProductBase(BaseModel):
    title_original: str = ""
    title_hi: str = ""
    title_en: str = ""
    description_original: str = ""
    description_hi: str = ""
    description_en: str = ""
    category: str = "Handicrafts"
    subcategory: str = "General"
    craft_type: str = "Handmade"
    material: str = "Natural Material"
    color: Optional[str] = None
    dimensions: Optional[str] = None
    weight: Optional[str] = None
    seo_keywords: List[str] = []
    seo_keywords_en: List[str] = []
    seo_keywords_hi: List[str] = []
    price: Optional[float] = None
    currency: str = "INR"
    status: str = "draft"  # draft, ready, published, unpublished
    is_handmade: bool = True
    artisan_id: Optional[str] = "default-artisan"

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    images: List[ImageInfo] = []
    attributes: List[ProductAttribute] = []
    created_at: datetime = Field(default_factory=current_utc_time)
    updated_at: datetime = Field(default_factory=current_utc_time)

    model_config = ConfigDict(from_attributes=True)


# --- Voice Input & Processing Schemas ---
class VoiceTranscribeRequest(BaseModel):
    audio_base64: Optional[str] = None
    language_code: Optional[str] = "auto"
    simulated_speech: Optional[str] = None

class VoiceTranscribeResponse(BaseModel):
    transcript_original: str
    detected_language: str
    language_name: str
    transcript_hi: str
    transcript_en: str
    extracted_attributes: Dict[str, Any] = {}

class VoiceCommandRequest(BaseModel):
    command_text: str
    current_product: Optional[Dict[str, Any]] = None
    language_code: Optional[str] = "auto"

class VoiceCommandResponse(BaseModel):
    action: str  # update_attribute, calculate_price, show_market, add_to_catalog, general
    message: str
    updated_fields: Dict[str, Any] = {}


# --- Pricing Calculator Schemas ---
class PriceCalculationInput(BaseModel):
    material_cost: float = Field(default=200.0, ge=0.0, description="Cost of raw materials in INR")
    time_spent_hours: float = Field(default=4.0, ge=0.0, description="Time spent making the product in hours")
    labour_rate_hourly: float = Field(default=150.0, ge=0.0, description="Labour rate per hour in INR")
    wastage_percent: float = Field(default=0.0, ge=0.0, le=100.0, description="Material wastage percentage")
    packaging_cost: float = Field(default=0.0, ge=0.0, description="Packaging cost in INR")
    other_costs: float = Field(default=0.0, ge=0.0, description="Electricity, tools, fuel, etc.")
    selling_costs: float = Field(default=0.0, ge=0.0, description="Payment or marketplace selling charges")
    profit_margin_percent: float = Field(default=30.0, ge=0.0, description="Desired profit margin percentage")
    premium_multiplier: float = Field(default=1.20, ge=1.0, description="Multiplier for premium price tier")

class PriceCalculationResult(BaseModel):
    material_cost: float
    wastage_cost: float
    labour_cost: float
    packaging_cost: float
    other_costs: float
    selling_costs: float
    total_cost: float
    cost_floor: float
    recommended_price: float
    estimated_profit: float
    premium_price: float
    currency: str = "INR"
    breakdown_text: str = ""


# --- Market Pricing Schemas ---
class MarketProduct(BaseModel):
    source: str
    source_product_id: str
    title: str
    price: float
    currency: str = "INR"
    quantity: int = 1
    unit: str = "piece"
    image_url: Optional[str] = None
    product_url: Optional[str] = None
    seller: str
    brand: Optional[str] = None
    rating: float = 4.5
    review_count: int = 50
    availability: str = "in_stock"
    retrieved_at: str = Field(default_factory=current_utc_iso)
    is_handmade: Optional[bool] = True
    similarity_score: float = 0.85
    craft_type: Optional[str] = None
    material: Optional[str] = None
    category: Optional[str] = "Handicrafts"

class MarketPriceCheckRequest(BaseModel):
    product_name: str
    category: str
    material: Optional[str] = None
    craft_type: Optional[str] = None
    is_handmade: bool = True
    image_url: Optional[str] = None

class MarketPriceCheckResult(BaseModel):
    product_name: str
    category: str
    search_queries: List[str]
    comparables: List[MarketProduct]
    total_found: int
    filtered_outliers_count: int
    median_price: float
    p25_price: float
    p75_price: float
    estimated_min_price: float
    estimated_max_price: float
    typical_market_price: float
    confidence_level: str  # "high", "medium", "low"
    confidence_badge_text: str
    confidence_reasons: List[str]
    online_presence: str  # "Established category", "Several comparable listings", "Limited online presence"
    currency: str = "INR"


# --- Pricing Insight Schemas ---
class PricingInsightRequest(BaseModel):
    current_price: Optional[float] = None
    calculation: Optional[PriceCalculationResult] = None
    market_check: Optional[MarketPriceCheckResult] = None

class PricingInsightResult(BaseModel):
    current_price: Optional[float]
    estimated_cost: float
    cost_based_target: float
    market_min: Optional[float]
    market_max: Optional[float]
    typical_market_price: Optional[float]
    status_level: str  # "below_cost", "underpricing", "competitive", "high_price", "cost_only"
    status_badge: str  # 🔴, 🟡, 🟢, 🟠
    status_title: str
    explanation: str
    suggested_test_range_min: Optional[float]
    suggested_test_range_max: Optional[float]
    actionable_advice: List[str]


# --- Digital Catalogs Schemas ---
class CatalogBase(BaseModel):
    title: str
    description: Optional[str] = None
    cover_image_url: Optional[str] = None
    is_published: bool = True
    artisan_id: Optional[str] = "default-artisan"

class CatalogCreate(CatalogBase):
    product_ids: List[str] = []

class Catalog(CatalogBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    products: List[Product] = []
    created_at: datetime = Field(default_factory=current_utc_time)

    model_config = ConfigDict(from_attributes=True)
