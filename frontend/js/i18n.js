/**
 * NIRMAAN - i18n (UI language) manager
 *
 * Only Hindi ("hi") and English ("en") are wired up for now. The strings
 * below cover the app's static chrome (nav, headers, buttons, labels).
 * AI-generated content (product titles/descriptions, prices, etc.) is left
 * as-is since it is generated live in whichever language the artisan spoke.
 */

export const SUPPORTED_UI_LANGUAGES = ["en", "hi"];
const STORAGE_KEY = "nirmaan_ui_language";

export const TRANSLATIONS = {
  en: {
    "app.tagline": "Artisan Catalog Studio",
    "nav.home": "Home",
    "nav.products": "My Products",
    "nav.marketplace": "Marketplace",
    "nav.schemes": "Scheme Sarthi",
    "nav.profile": "Profile",

    "home.greeting": "Welcome back",
    "home.subtitle": "Ready to catalog a new creation?",
    "home.cta.new_product": "+ Create New Product Listing",
    "home.recent.title": "Recently Created",
    "home.quick_tools": "Quick Studio Tools",
    "home.tool_photo_title": "AI Product Photo",
    "home.tool_photo_desc": "Studio background & lighting",
    "home.tool_voice_title": "Speak Your Product",
    "home.tool_voice_desc": "Describe in your language",
    "home.tool_calc_title": "Calculate My Price",
    "home.tool_calc_desc": "Fair wage cost calculator",
    "home.tool_market_title": "Check Market Price",
    "home.tool_market_desc": "Comparable prices in India",

    "create.step1.title": "How would you like to describe it?",
    "create.mode.voice": "🎙️ Speak Product",
    "create.mode.text": "✍️ Write Description",
    "create.step2.title": "Tell us about your product",
    "create.step2.subtitle": "Speak in your own language — English, हिंदी, मराठी, বাংলা, தமிழ், etc.",
    "create.speaking_in": "🎙️ Speaking In:",
    "create.mic.tap": "Tap to Record Your Voice",
    "create.mic.placeholder": "🎙️ Record your voice here — describe your product in your own words.",
    "create.examples.title": "Quick Spoken Examples (Tap to use):",
    "create.next.catalog": "Next: Create Professional Catalog ✨",

    "products.title": "My Products",
    "marketplace.title": "Marketplace",
    "profile.title": "Profile",
    "profile.edit": "✏️ Edit Artisan Profile & Preferences",

    "onboarding.title": "Welcome to NIRMAAN",
    "onboarding.subtitle": "Tell us about yourself so we can configure your studio assistant.",
    "onboarding.name": "Your Name / Business Name:",
    "onboarding.language": "Preferred Language:",
    "onboarding.language.note": "More languages coming soon.",
    "onboarding.craft": "What do you make? (Select multiple)",
    "onboarding.seller_type": "Seller Type:",
    "onboarding.region": "Your Region:",
    "onboarding.save": "Save & Continue",

    "langpicker.title": "Choose your language",
    "langpicker.subtitle": "आप हिंदी या अंग्रेज़ी चुन सकते हैं — More languages coming soon.",
    "langpicker.hi": "हिंदी",
    "langpicker.en": "English",
    "langpicker.continue": "Continue",

    "tabs.marketplace": "Marketplace",
    "tabs.studio_pro": "Professional Studio",
    "tabs.original": "Original",
    "tabs.features": "Features",
    "tabs.calc_price": "💰 Calculate My Price",
    "tabs.market_price": "🌐 Check Market Price",
    "tabs.pricing_insight": "💡 Pricing Insight",
    "tabs.cat_all": "All",
    "tabs.cat_pottery": "Pottery",
    "tabs.cat_bamboo": "Bamboo",
    "tabs.cat_metal": "Metal Craft",
    "tabs.cat_textiles": "Textiles",
    "tabs.cat_jewellery": "Jewellery",
    "tabs.cat_woodcraft": "Woodcraft",

    "auth.welcome": "Welcome to NIRMAAN",
    "auth.subtitle": "Register or log in to start cataloging your craft.",
    "auth.tab_login": "Log In",
    "auth.tab_register": "New Registration",
    "auth.mobile": "Mobile Number",
    "auth.send_otp": "Send OTP",
    "auth.otp": "Enter OTP",
    "auth.otp_hint": "This is a demo — any mobile number works, use OTP 123456.",
    "auth.login_btn": "Log In",
    "auth.full_name": "Full Name",
    "auth.gender": "Gender",
    "auth.gender_male": "Male",
    "auth.gender_female": "Female",
    "auth.gender_other": "Other",
    "auth.craft_type": "Primary Craft",
    "auth.state": "State",
    "auth.district": "District / Town",
    "auth.aadhaar": "Aadhaar / Artisan ID Card No. (Optional)",
    "auth.register_btn": "Complete Registration",

    "schemes.title": "Government Schemes For You",
    "schemes.subtitle": "Support programs from the Government of India for artisans like you.",
    "schemes.continue": "Continue to NIRMAAN",
    "schemes.about": "About",
    "schemes.eligibility": "Eligibility",
    "schemes.close": "Close"
  },
  hi: {
    "app.tagline": "कारीगर कैटलॉग स्टूडियो",
    "nav.home": "होम",
    "nav.products": "मेरे उत्पाद",
    "nav.marketplace": "बाज़ार",
    "nav.schemes": "स्कीम सारथी",
    "nav.profile": "प्रोफ़ाइल",

    "home.greeting": "वापसी पर स्वागत है",
    "home.subtitle": "एक नई रचना को कैटलॉग करने के लिए तैयार हैं?",
    "home.cta.new_product": "+ नया उत्पाद बनाएं",
    "home.recent.title": "हाल ही में बनाए गए",
    "home.quick_tools": "त्वरित स्टूडियो टूल्स",
    "home.tool_photo_title": "एआई प्रोडक्ट फोटो",
    "home.tool_photo_desc": "स्टूडियो बैकग्राउंड व लाइटिंग",
    "home.tool_voice_title": "अपने उत्पाद के बारे में बोलें",
    "home.tool_voice_desc": "अपनी भाषा में बताएं",
    "home.tool_calc_title": "अपनी कीमत तय करें",
    "home.tool_calc_desc": "उचित मज़दूरी लागत कैलकुलेटर",
    "home.tool_market_title": "बाज़ार मूल्य देखें",
    "home.tool_market_desc": "भारत में समान कीमतें",

    "create.step1.title": "आप इसे कैसे बताना चाहेंगे?",
    "create.mode.voice": "🎙️ बोलकर बताएं",
    "create.mode.text": "✍️ लिखकर बताएं",
    "create.step2.title": "अपने उत्पाद के बारे में बताएं",
    "create.step2.subtitle": "अपनी भाषा में बोलें — अंग्रेज़ी, हिंदी, मराठी, বাংলা, தமிழ், आदि।",
    "create.speaking_in": "🎙️ बोल रहे हैं:",
    "create.mic.tap": "अपनी आवाज़ रिकॉर्ड करने के लिए टैप करें",
    "create.mic.placeholder": "🎙️ यहां अपनी आवाज़ रिकॉर्ड करें — अपने उत्पाद के बारे में अपने शब्दों में बताएं।",
    "create.examples.title": "बोलने के उदाहरण (उपयोग करने के लिए टैप करें):",
    "create.next.catalog": "आगे: प्रोफेशनल कैटलॉग बनाएं ✨",

    "products.title": "मेरे उत्पाद",
    "marketplace.title": "बाज़ार",
    "profile.title": "प्रोफ़ाइल",
    "profile.edit": "✏️ कारीगर प्रोफ़ाइल व वरीयताएं संपादित करें",

    "onboarding.title": "NIRMAAN में आपका स्वागत है",
    "onboarding.subtitle": "अपने बारे में बताएं ताकि हम आपका स्टूडियो असिस्टेंट सेट कर सकें।",
    "onboarding.name": "आपका नाम / व्यवसाय का नाम:",
    "onboarding.language": "पसंदीदा भाषा:",
    "onboarding.language.note": "और भाषाएं जल्द आ रही हैं।",
    "onboarding.craft": "आप क्या बनाते हैं? (एक से अधिक चुनें)",
    "onboarding.seller_type": "विक्रेता प्रकार:",
    "onboarding.region": "आपका क्षेत्र:",
    "onboarding.save": "सहेजें और आगे बढ़ें",

    "langpicker.title": "अपनी भाषा चुनें",
    "langpicker.subtitle": "You can choose Hindi or English — और भाषाएं जल्द आ रही हैं।",
    "langpicker.hi": "हिंदी",
    "langpicker.en": "English",
    "langpicker.continue": "आगे बढ़ें",

    "tabs.marketplace": "बाज़ार",
    "tabs.studio_pro": "प्रोफेशनल स्टूडियो",
    "tabs.original": "मूल",
    "tabs.features": "विशेषताएं",
    "tabs.calc_price": "💰 अपनी कीमत तय करें",
    "tabs.market_price": "🌐 बाज़ार मूल्य देखें",
    "tabs.pricing_insight": "💡 मूल्य जानकारी",
    "tabs.cat_all": "सभी",
    "tabs.cat_pottery": "मिट्टी के बर्तन",
    "tabs.cat_bamboo": "बांस",
    "tabs.cat_metal": "धातु शिल्प",
    "tabs.cat_textiles": "वस्त्र",
    "tabs.cat_jewellery": "आभूषण",
    "tabs.cat_woodcraft": "काष्ठ शिल्प",

    "auth.welcome": "NIRMAAN में आपका स्वागत है",
    "auth.subtitle": "अपने शिल्प की कैटलॉगिंग शुरू करने के लिए पंजीकरण करें या लॉग इन करें।",
    "auth.tab_login": "लॉग इन",
    "auth.tab_register": "नया पंजीकरण",
    "auth.mobile": "मोबाइल नंबर",
    "auth.send_otp": "ओटीपी भेजें",
    "auth.otp": "ओटीपी दर्ज करें",
    "auth.otp_hint": "यह एक डेमो है — कोई भी मोबाइल नंबर काम करेगा, ओटीपी 123456 उपयोग करें।",
    "auth.login_btn": "लॉग इन करें",
    "auth.full_name": "पूरा नाम",
    "auth.gender": "लिंग",
    "auth.gender_male": "पुरुष",
    "auth.gender_female": "महिला",
    "auth.gender_other": "अन्य",
    "auth.craft_type": "मुख्य शिल्प",
    "auth.state": "राज्य",
    "auth.district": "ज़िला / शहर",
    "auth.aadhaar": "आधार / कारीगर पहचान पत्र संख्या (वैकल्पिक)",
    "auth.register_btn": "पंजीकरण पूरा करें",

    "schemes.title": "आपके लिए सरकारी योजनाएं",
    "schemes.subtitle": "कारीगरों के लिए भारत सरकार के सहायता कार्यक्रम।",
    "schemes.continue": "NIRMAAN पर जारी रखें",
    "schemes.about": "योजना के बारे में",
    "schemes.eligibility": "पात्रता",
    "schemes.close": "बंद करें"
  }
};

/**
 * Applies a UI language across every element tagged with data-i18n /
 * data-i18n-placeholder, switches the Hindi (Dekko) font on/off, persists
 * the choice, and updates <html lang="...">.
 */
export function applyLanguage(langCode) {
  const lang = SUPPORTED_UI_LANGUAGES.includes(langCode) ? langCode : "en";
  const dict = TRANSLATIONS[lang];

  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    if (dict[key]) el.textContent = dict[key];
  });

  document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
    const key = el.getAttribute("data-i18n-placeholder");
    if (dict[key]) el.setAttribute("placeholder", dict[key]);
  });

  document.documentElement.setAttribute("lang", lang);
  document.body.classList.toggle("lang-hi", lang === "hi");

  try {
    localStorage.setItem(STORAGE_KEY, lang);
  } catch (e) { /* localStorage unavailable, non-fatal */ }

  return lang;
}

export function getSavedLanguage() {
  try {
    return localStorage.getItem(STORAGE_KEY);
  } catch (e) {
    return null;
  }
}
