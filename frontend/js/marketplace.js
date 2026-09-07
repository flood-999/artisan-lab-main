/**
 * NIRMAAN - Marketplace & Sharing Manager
 * Handles marketplace listings, search, category filters, and WhatsApp/Social sharing.
 */
import { ApiClient } from "./api.js";

export const MarketplaceManager = {
  activeCategory: "All",
  searchQuery: "",
  products: [],

  async loadFeed(category = "All", query = "") {
    this.activeCategory = category;
    this.searchQuery = query;
    const catParam = category === "All" ? null : category;
    const data = await ApiClient.getMarketplaceFeed(catParam, query);
    this.products = data.products || [];
    return this.products;
  },

  generateWhatsAppShareUrl(product, artisanName = "Artisan Ramesh") {
    const title = product.title_en || product.title_hi || product.title_original || "Handmade Craft";
    const price = product.price ? `₹${product.price}` : "Price on Request";
    const desc = product.description_en || product.description_hi || "";
    
    const message = `Namaste! 🙏\nCheck out this authentic handmade craft from *${artisanName}* on NIRMAAN:\n\n*${title}*\n💰 Price: ${price}\n🧵 Material: ${product.material || "Natural"}\n✨ Craft: ${product.craft_type || "Handmade"}\n\n${desc}\n\n👉 Discover more on NIRMAAN Marketplace!`;
    
    return `https://api.whatsapp.com/send?text=${encodeURIComponent(message)}`;
  }
};
