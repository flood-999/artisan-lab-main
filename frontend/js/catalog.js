/**
 * NIRMAAN - Catalog Viewer & Multilingual Editor
 * Manages photo switching, multilingual tabs, and voice-command editing.
 */
import { ApiClient } from "./api.js";

export const CatalogManager = {
  activeProduct: null,
  activeImageTab: "original", // marketplace, original, features
  activeLangTab: "original",    // original, hi, en

  setProduct(product) {
    this.activeProduct = product;
  },

  getCurrentImage() {
    if (!this.activeProduct || !this.activeProduct.images || this.activeProduct.images.length === 0) {
      return "/static/images/terracotta_marketplace.jpg";
    }
    const matched = this.activeProduct.images.find(img => img.image_type === this.activeImageTab);
    return matched ? matched.url : this.activeProduct.images[0].url;
  },

  getLocalizedContent(lang = "original") {
    if (!this.activeProduct) return { title: "", description: "", keywords: [] };
    if (lang === "hi") {
      return {
        title: this.activeProduct.title_hi || this.activeProduct.title_original,
        description: this.activeProduct.description_hi || this.activeProduct.description_original,
        keywords: this.activeProduct.seo_keywords_hi && this.activeProduct.seo_keywords_hi.length
          ? this.activeProduct.seo_keywords_hi
          : (this.activeProduct.seo_keywords || [])
      };
    } else if (lang === "en") {
      return {
        title: this.activeProduct.title_en || this.activeProduct.title_original,
        description: this.activeProduct.description_en || this.activeProduct.description_original,
        keywords: this.activeProduct.seo_keywords_en && this.activeProduct.seo_keywords_en.length
          ? this.activeProduct.seo_keywords_en
          : (this.activeProduct.seo_keywords || [])
      };
    }
    return {
      title: this.activeProduct.title_original || this.activeProduct.title_hi || "हस्तनिर्मित उत्पाद",
      description: this.activeProduct.description_original || this.activeProduct.description_hi || "",
      keywords: this.activeProduct.seo_keywords_en && this.activeProduct.seo_keywords_en.length
        ? this.activeProduct.seo_keywords_en
        : (this.activeProduct.seo_keywords || [])
    };
  },

  async executeVoiceCommand(commandText) {
    if (!commandText) return null;
    const res = await ApiClient.processVoiceCommand(commandText, this.activeProduct);
    if (res && res.updated_fields && this.activeProduct) {
      Object.assign(this.activeProduct, res.updated_fields);
    }
    return res;
  }
};
