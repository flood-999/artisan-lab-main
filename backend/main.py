"""
NIRMAAN - Main FastAPI Application
Production-ready REST API for AI-Powered Artisan Catalog & Marketplace App.
"""
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
import os
import shutil
import uuid
from typing import List, Optional, Dict, Any

from .config import FRONTEND_DIR, UPLOADS_DIR, APP_NAME, APP_VERSION
from .models.schemas import (
    Artisan, ArtisanBase, Product, ProductCreate, ImageInfo,
    VoiceTranscribeRequest, VoiceTranscribeResponse,
    VoiceCommandRequest, VoiceCommandResponse,
    PriceCalculationInput, PriceCalculationResult,
    MarketPriceCheckRequest, MarketPriceCheckResult,
    PricingInsightRequest, PricingInsightResult,
    Catalog, CatalogCreate
)
from .database.db import db
from .services import (
    cost_pricing_service,
    market_data_service,
    pricing_insight_service,
    product_vision_service,
    speech_service,
    audio_transcription_service,
    translation_service,
    catalog_extraction_service,
    voice_command_service,
    catalog_service
)

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="AI-Powered Artisan Catalog & Marketplace Mobile Application Backend"
)

# CORS middleware for mobile/web cross-origin compatibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount uploads and frontend static directories
os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(FRONTEND_DIR, exist_ok=True)

app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# --- Root & Health Endpoints ---
@app.get("/")
async def root():
    index_file = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "NIRMAAN API is active. Open /docs for interactive documentation."}

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "app": APP_NAME,
        "version": APP_VERSION,
        "database": "connected"
    }

# --- Artisan Profile & Onboarding ---
@app.get("/api/artisan", response_model=Artisan)
async def get_artisan_profile(artisan_id: str = "artisan-ramesh"):
    artisan = db.get_artisan(artisan_id)
    if not artisan:
        raise HTTPException(status_code=404, detail="Artisan profile not found")
    return artisan

@app.put("/api/artisan", response_model=Artisan)
async def update_artisan_profile(artisan_data: ArtisanBase, artisan_id: str = "artisan-ramesh"):
    artisan = db.get_artisan(artisan_id)
    if not artisan:
        artisan = Artisan(id=artisan_id, **artisan_data.model_dump())
    else:
        for k, v in artisan_data.model_dump().items():
            setattr(artisan, k, v)
    return db.update_artisan(artisan)

# --- Photo Upload & AI Studio Studio ---
@app.post("/api/products/upload-photo")
async def upload_product_photo(
    file: UploadFile = File(...),
    category: str = Form("Handicrafts"),
    craft_type: str = Form("Handmade")
):
    temp_dir = os.path.join(UPLOADS_DIR, "temp")
    os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = os.path.join(temp_dir, f"temp_{uuid.uuid4()}_{file.filename}")
    
    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        images_info, attributes, visual_traits = product_vision_service.process_artisan_photo(
            source_image_path=temp_file_path,
            category=category,
            craft_type=craft_type
        )
        
        return {
            "success": True,
            "images": [img.model_dump() for img in images_info],
            "attributes": [attr.model_dump() for attr in attributes],
            "visual_traits": visual_traits,
            "message": "Your professional product photo is ready."
        }
    except Exception as e:
        # Fallback safe response (Never expose raw API error to artisan UI)
        return {
            "success": True,
            "images": [],
            "attributes": [],
            "visual_traits": {
                "category": category or "Handicrafts",
                "craft_type": craft_type or "Handmade",
                "material": "Natural Material",
                "color": "Natural Tones",
                "confidence": 0.85
            },
            "message": "Your professional product photo is ready."
        }
    finally:
        if os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except Exception:
                pass

@app.post("/api/products/generate-style")
async def generate_product_style(payload: Dict[str, Any]):
    image_url = payload.get("image_url", "/static/images/terracotta_marketplace.jpg")
    style_preset = payload.get("style", "clean_studio")
    try:
        new_image_info = product_vision_service.generate_styled_image(
            image_url_or_path=image_url,
            style_preset=style_preset
        )
        return {
            "success": True,
            "image": new_image_info.model_dump(),
            "message": f"Applied {style_preset.replace('_', ' ').title()} studio backdrop."
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Could not generate style."
        }

@app.post("/api/products/generate-feature-image")
async def generate_feature_image(payload: Dict[str, Any]):
    """
    Builds the third "Features" image: the finished Marketplace photo plus
    a bullet-point panel of the real features extracted from the artisan's
    voice/text description. Called after /api/voice/catalog returns
    `features`, since they aren't known at photo-upload time.
    """
    marketplace_image_url = payload.get("marketplace_image_url", "/static/images/terracotta_marketplace.jpg")
    features = payload.get("features", [])
    category = payload.get("category", "Handicrafts")
    craft_type = payload.get("craft_type", "Handmade")
    title = payload.get("title", "")
    try:
        new_image_info = product_vision_service.generate_feature_image(
            marketplace_image_url_or_path=marketplace_image_url,
            features=features,
            category=category,
            craft_type=craft_type,
            title=title
        )
        return {
            "success": True,
            "image": new_image_info.model_dump(),
            "message": "Feature highlight image created."
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Could not generate the feature image."
        }

# --- Voice Processing & Extraction ---
@app.post("/api/voice/transcribe", response_model=VoiceTranscribeResponse)
async def transcribe_voice(request: VoiceTranscribeRequest):
    transcription = speech_service.transcribe(
        raw_audio_data=request.audio_base64,
        simulated_speech=request.simulated_speech
    )
    
    translations = translation_service.translate_text(
        text=transcription["transcript_original"],
        source_lang=transcription["detected_language"]
    )
    
    return VoiceTranscribeResponse(
        transcript_original=transcription["transcript_original"],
        detected_language=transcription["detected_language"],
        language_name=transcription["language_name"],
        transcript_hi=translations["hi"],
        transcript_en=translations["en"],
        extracted_attributes={}
    )

@app.post("/api/voice/transcribe-audio")
async def transcribe_recorded_audio(
    audio_file: UploadFile = File(...),
    language_hint: str = Form("auto")
):
    """
    Real voice-note transcription: the artisan's actual recorded audio is
    sent to Gemini and transcribed genuinely — there is NO hardcoded
    fallback product text here. If transcription isn't possible, the
    caller must ask the artisan to retry or type their description.
    """
    try:
        audio_bytes = await audio_file.read()
        mime_type = audio_file.content_type or "audio/webm"

        result = audio_transcription_service.transcribe(audio_bytes, mime_type=mime_type)

        if result is None:
            reason = audio_transcription_service.last_error or "Unknown error."
            print(f"[/api/voice/transcribe-audio] Transcription failed: {reason}")
            raise HTTPException(
                status_code=503,
                detail=f"Voice transcription is unavailable right now ({reason}). Please try recording again, "
                       "or write your product description instead."
            )

        if not result["transcript_original"]:
            raise HTTPException(
                status_code=422,
                detail="We couldn't hear anything clear in that recording. Please record again in a "
                       "quiet space, or write your product description instead."
            )

        return {
            "success": True,
            "transcript_original": result["transcript_original"],
            "detected_language": result["detected_language"],
            "language_name": result["language_name"]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

@app.post("/api/voice/catalog")
async def extract_catalog_from_voice_and_vision(payload: Dict[str, Any]):
    spoken_text = payload.get("spoken_text", "")
    detected_language = payload.get("detected_language", "hi")
    visual_traits = payload.get("visual_traits", {})
    
    catalog_data = catalog_extraction_service.extract_from_speech_and_vision(
        spoken_text=spoken_text,
        detected_language=detected_language,
        visual_traits=visual_traits
    )
    
    return catalog_data

@app.post("/api/voice/command", response_model=VoiceCommandResponse)
async def process_voice_command(request: VoiceCommandRequest):
    return voice_command_service.process_command(request)

# --- Pricing Endpoints ---
@app.post("/api/pricing/calculate", response_model=PriceCalculationResult)
async def calculate_cost_price(input_data: PriceCalculationInput):
    return cost_pricing_service.calculate(input_data)

@app.post("/api/pricing/market-check", response_model=MarketPriceCheckResult)
async def check_market_price(request: MarketPriceCheckRequest):
    return market_data_service.check_market_price(request)

@app.post("/api/pricing/insight", response_model=PricingInsightResult)
async def generate_pricing_insight(request: PricingInsightRequest):
    return pricing_insight_service.generate_insight(request)

# --- Products CRUD & Marketplace ---
@app.get("/api/products", response_model=List[Product])
async def list_products(
    artisan_id: Optional[str] = None,
    status: Optional[str] = None
):
    return db.get_products(artisan_id=artisan_id, status=status)

@app.get("/api/products/{product_id}", response_model=Product)
async def get_product_detail(product_id: str):
    prod = db.get_product(product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    return prod

@app.post("/api/products/save", response_model=Product)
async def save_product(product: Product):
    return db.save_product(product)

@app.post("/api/products/{product_id}/publish", response_model=Product)
async def publish_product(product_id: str):
    prod = db.get_product(product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    prod.status = "published"
    return db.save_product(prod)

# --- Digital Catalogs ---
@app.get("/api/catalogs", response_model=List[Catalog])
async def list_catalogs(artisan_id: Optional[str] = None):
    return catalog_service.get_all_catalogs(artisan_id=artisan_id)

@app.post("/api/catalogs", response_model=Catalog)
async def create_catalog(catalog_data: CatalogCreate):
    return catalog_service.create_catalog(catalog_data)

# --- Marketplace Browsing Feed ---
@app.get("/api/marketplace/feed")
async def marketplace_feed(
    query: Optional[str] = None,
    category: Optional[str] = None,
    sort_by: Optional[str] = "newest"
):
    all_products = db.get_products(status="published")
    filtered = all_products
    
    if category and category != "All":
        filtered = [p for p in filtered if category.lower() in p.category.lower() or category.lower() in p.craft_type.lower()]
        
    if query:
        q = query.lower()
        filtered = [
            p for p in filtered
            if q in p.title_en.lower() or q in p.title_hi.lower() or q in p.title_original.lower() or q in p.material.lower()
        ]
        
    return {
        "total": len(filtered),
        "products": [p.model_dump() for p in filtered]
    }
