"""
NIRMAAN - Catalog Service
Manages digital collections, collection sharing, and exporting.
"""
from typing import List, Optional
from ..models.schemas import Catalog, CatalogCreate
from ..database.db import db

class CatalogService:
    @staticmethod
    def get_all_catalogs(artisan_id: Optional[str] = None) -> List[Catalog]:
        return db.get_catalogs(artisan_id=artisan_id)

    @staticmethod
    def create_catalog(create_data: CatalogCreate) -> Catalog:
        new_catalog = Catalog(
            title=create_data.title,
            description=create_data.description,
            cover_image_url=create_data.cover_image_url,
            is_published=create_data.is_published,
            artisan_id=create_data.artisan_id
        )
        return db.save_catalog(new_catalog, product_ids=create_data.product_ids)

catalog_service = CatalogService()
