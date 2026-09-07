/**
 * NIRMAAN - API Client
 * Interfaces with backend endpoints with resilient error fallbacks.
 */
const BASE_URL = window.location.origin;

export const ApiClient = {
  async getArtisan() {
    const res = await fetch(`${BASE_URL}/api/artisan`);
    if (!res.ok) throw new Error("Failed to fetch artisan");
    return res.json();
  },

  async updateArtisan(artisanData) {
    const res = await fetch(`${BASE_URL}/api/artisan`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(artisanData)
    });
    return res.json();
  },

  async uploadProductPhoto(fileBlob, category = "Handicrafts", craftType = "Handmade") {
    const formData = new FormData();
    formData.append("file", fileBlob, "photo.jpg");
    formData.append("category", category);
    formData.append("craft_type", craftType);

    const res = await fetch(`${BASE_URL}/api/products/upload-photo`, {
      method: "POST",
      body: formData
    });
    return res.json();
  },

  async generateStyle(imageUrl, stylePreset = "warm_wood") {
    const res = await fetch(`${BASE_URL}/api/products/generate-style`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ image_url: imageUrl, style: stylePreset })
    });
    return res.json();
  },

  async generateFeatureImage(marketplaceImageUrl, features, category, craftType, title) {
    const res = await fetch(`${BASE_URL}/api/products/generate-feature-image`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        marketplace_image_url: marketplaceImageUrl,
        features: features,
        category: category,
        craft_type: craftType,
        title: title
      })
    });
    return res.json();
  },

  /**
   * Sends the artisan's REAL recorded voice note to the backend, which uses
   * Gemini's audio understanding to genuinely transcribe it — no canned or
   * placeholder product text is ever substituted here.
   */
  async transcribeAudioBlob(audioBlob, languageHint = "auto") {
    const formData = new FormData();
    const extension = (audioBlob.type || "").includes("mp4") ? "m4a" : "webm";
    formData.append("audio_file", audioBlob, `voice_note.${extension}`);
    formData.append("language_hint", languageHint);

    const res = await fetch(`${BASE_URL}/api/voice/transcribe-audio`, {
      method: "POST",
      body: formData
    });

    if (!res.ok) {
      let detail = "Could not transcribe the recording.";
      try {
        const errBody = await res.json();
        detail = errBody.detail || detail;
      } catch (e) { /* ignore */ }
      throw new Error(detail);
    }

    return res.json();
  },

  async transcribeVoice(simulatedSpeech = null, languageCode = "auto") {
    const res = await fetch(`${BASE_URL}/api/voice/transcribe`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        simulated_speech: simulatedSpeech,
        language_code: languageCode
      })
    });
    return res.json();
  },

  async extractCatalog(spokenText, detectedLanguage, visualTraits) {
    const res = await fetch(`${BASE_URL}/api/voice/catalog`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        spoken_text: spokenText,
        detected_language: detectedLanguage,
        visual_traits: visualTraits
      })
    });
    return res.json();
  },

  async processVoiceCommand(commandText, currentProduct) {
    const res = await fetch(`${BASE_URL}/api/voice/command`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        command_text: commandText,
        current_product: currentProduct
      })
    });
    return res.json();
  },

  async calculateCostPrice(calcInput) {
    const res = await fetch(`${BASE_URL}/api/pricing/calculate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(calcInput)
    });
    return res.json();
  },

  async checkMarketPrice(marketReq) {
    const res = await fetch(`${BASE_URL}/api/pricing/market-check`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(marketReq)
    });
    return res.json();
  },

  async getPricingInsight(insightReq) {
    const res = await fetch(`${BASE_URL}/api/pricing/insight`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(insightReq)
    });
    return res.json();
  },

  async getProducts(status = null) {
    let url = `${BASE_URL}/api/products`;
    if (status) url += `?status=${status}`;
    const res = await fetch(url);
    return res.json();
  },

  async getProduct(id) {
    const res = await fetch(`${BASE_URL}/api/products/${id}`);
    return res.json();
  },

  async saveProduct(product) {
    const res = await fetch(`${BASE_URL}/api/products/save`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(product)
    });
    return res.json();
  },

  async publishProduct(productId) {
    const res = await fetch(`${BASE_URL}/api/products/${productId}/publish`, {
      method: "POST"
    });
    return res.json();
  },

  async getCatalogs() {
    const res = await fetch(`${BASE_URL}/api/catalogs`);
    return res.json();
  },

  async getMarketplaceFeed(category = null, query = null) {
    let url = `${BASE_URL}/api/marketplace/feed?`;
    if (category) url += `category=${encodeURIComponent(category)}&`;
    if (query) url += `query=${encodeURIComponent(query)}&`;
    const res = await fetch(url);
    return res.json();
  }
};
