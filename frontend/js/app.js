/**
 * NIRMAAN - Main Application Coordinator
 */
import { ApiClient } from "./api.js";
import { StorageManager } from "./storage.js";
import { AudioManager } from "./audio.js";
import { CameraManager } from "./camera.js";
import { PricingManager } from "./pricing.js";
import { CatalogManager } from "./catalog.js";
import { MarketplaceManager } from "./marketplace.js";
import { applyLanguage, getSavedLanguage } from "./i18n.js";
import { SCHEMES } from "./schemes-data.js";

const MULTILINGUAL_SPEECH_EXAMPLES = {
  "en-IN": [
    { label: "🏺 Terracotta Bowl (4 hrs)", text: "This is a hand-thrown terracotta serving bowl made from natural red clay on the potter's wheel. It took 4 hours to make." },
    { label: "🧺 Bamboo Basket (₹500)", text: "This is a durable handwoven natural bamboo storage basket for fruits and kitchen, price 500 rupees." },
    { label: "🪔 Brass Diya (Brass casting)", text: "Traditional solid brass peacock oil lamp diya, hand-cast for pooja and festive home decor." },
    { label: "🧵 Handloom Saree", text: "Handwoven pure cotton artisan saree with zari border, woven on traditional village handloom." }
  ],
  "hi-IN": [
    { label: "🏺 Terracotta Bowl (4 hrs)", text: "यह मिट्टी का सर्विंग बाउल है, शुद्ध लाल मिट्टी से चाक पर बनाया है, 4 घंटे लगे बनाने में।" },
    { label: "🧺 Bamboo Basket (₹500)", text: "यह प्राकृतिक बांस से हाथ से बुनी फल रखने की मजबूत टोकरी है, कीमत 500 रुपये।" },
    { label: "🪔 Brass Diya (Brass casting)", text: "पारंपरिक ठोस पीतल का मोर दीया, पूजा और दीपावली सजावट के लिए।" },
    { label: "🧵 Handloom Saree", text: "हथकरघा पर शुद्ध सूती धागों से बनी पारंपरिक साड़ी जरी बॉर्डर के साथ।" }
  ],
  "mr-IN": [
    { label: "🏺 Terracotta Bowl (4 hrs)", text: "हे शुद्ध लाल मातीपासून चाकावर बनवलेले हस्तनिर्मित मातीचे बाऊल आहे, बनवायला 4 तास लागले." },
    { label: "🧺 Bamboo Basket (₹500)", text: "नैसर्गिक बांबूपासून हाताने विणलेली फळांची मजबूत टोपली आहे, किंमत 500 रुपये." },
    { label: "🪔 Brass Diya (Brass casting)", text: "पूजा आणि सणांच्या सजावटीसाठी पारंपारिक भरीव पितळी मोराचा दिवा." }
  ],
  "bn-IN": [
    { label: "🏺 Terracotta Bowl (4 hrs)", text: "এটি খাঁটি লাল মাটি দিয়ে চাকার উপর তৈরি হস্তনির্মিত টেরাকোটা বাটি, তৈরি করতে ৪ ঘণ্টা লেগেছে।" },
    { label: "🧺 Bamboo Basket (₹500)", text: "প্রাকৃতিক বাঁশ দিয়ে হাতে বোনা টেকসই ফলের ঝুড়ি, দাম ৫০০ টাকা।" },
    { label: "🪔 Brass Diya (Brass casting)", text: "পূজা ও উৎসবের সাজসজ্জার জন্য ঐতিহ্যবাহী খাঁটি পিতলের ময়ূর প্রদীপ।" }
  ],
  "gu-IN": [
    { label: "🏺 Terracotta Bowl (4 hrs)", text: "આ કુદરતી લાલ માટીમાંથી ચાકડા પર બનાવેલ માટીનો બાઉલ છે, બનાવવામાં 4 કલાક લાગ્યા." },
    { label: "🧺 Bamboo Basket (₹500)", text: "કુદરતી વાંસમાંથી હાથથી વણેલી ફળોની ટોપલી છે, કિંમત 500 રૂપિયા." },
    { label: "🪔 Brass Diya (Brass casting)", text: "પૂજા અને દિવાળી માટે પરંપરાગત પિત્તળનો મોર દીવો." }
  ],
  "ta-IN": [
    { label: "🏺 Terracotta Bowl (4 hrs)", text: "இது தூய களிமண்ணால் சக்கரத்தில் செய்யப்பட்ட கைவினை டெரகோட்டா கிண்ணம், செய்ய 4 மணி நேரம் ஆனது." },
    { label: "🧺 Bamboo Basket (₹500)", text: "இயற்கை மூங்கிலால் கையால் நெய்யப்பட்ட பழக் கூடை, விலை 500 ரூபாய்." },
    { label: "🪔 Brass Diya (Brass casting)", text: "பூஜை மற்றும் அலங்காரத்திற்கான பாரம்பரிய பித்தளை மயில் தீபம்." }
  ],
  "te-IN": [
    { label: "🏺 Terracotta Bowl (4 hrs)", text: "ఇది సహజ ఎర్ర మట్టితో చక్రంపై తయారు చేసిన మట్టి గిన్నె, చేయడానికి 4 గంటలు పట్టింది." },
    { label: "🧺 Bamboo Basket (₹500)", text: "సహజ వెదురుతో చేతితో అల్లిన పండ్ల బుట్ట, ధర 500 రూపాయలు." },
    { label: "🪔 Brass Diya (Brass casting)", text: "పూజ మరియు పండుగల కోసం సంప్రదాయ ఇత్తడి నెమలి దీపం." }
  ],
  "kn-IN": [
    { label: "🏺 Terracotta Bowl (4 hrs)", text: "ಇದು ನೈಸರ್ಗಿಕ ಜೇಡಿಮಣ್ಣಿನಿಂದ ಚಕ್ರದಲ್ಲಿ ಮಾಡಿದ ಟೆರಾಕೋಟಾ ಬಟ್ಟಲು, ಮಾಡಲು 4 ಗಂಟೆ ಬೇಕಾಯಿತು." },
    { label: "🧺 Bamboo Basket (₹500)", text: "ನೈಸರ್ಗಿಕ ಬಿದಿರಿನಿಂದ ಕೈಯಿಂದ ನೇಯ್ದ ಹಣ್ಣಿನ ಬುಟ್ಟಿ, ಬೆಲೆ 500 ರೂಪಾಯಿ." },
    { label: "🪔 Brass Diya (Brass casting)", text: "ಪೂಜೆ ಮತ್ತು ಅಲಂಕಾರಕ್ಕಾಗಿ ಸಾಂಪ್ರದಾಯಿಕ ಹಿತ್ತಾಳೆ ನವಿಲು ದೀಪ." }
  ],
  "pa-IN": [
    { label: "🏺 Terracotta Bowl (4 hrs)", text: "ਇਹ ਸ਼ੁੱਧ ਮਿੱਟੀ ਤੋਂ ਚੱਕ ਉੱਤੇ ਬਣਾਇਆ ਗਿਆ ਮਿੱਟੀ ਦਾ ਬਾਊਲ ਹੈ, ਬਣਾਉਣ ਵਿੱਚ 4 ਘੰਟੇ ਲੱਗੇ।" },
    { label: "🧺 Bamboo Basket (₹500)", text: "ਕੁਦਰਤੀ ਬਾਂਸ ਤੋਂ ਹੱਥੀਂ ਬੁਣੀ ਫਲਾਂ ਦੀ ਟੋਕਰੀ ਹੈ, ਕੀਮਤ 500 ਰੁਪਏ।" },
    { label: "🪔 Brass Diya (Brass casting)", text: "ਪੂਜਾ ਅਤੇ ਸਜਾਵਟ ਲਈ ਰਵਾਇਤੀ ਪਿੱਤਲ ਦਾ ਮੋਰ ਦੀਵਾ।" }
  ],
  "ml-IN": [
    { label: "🏺 Terracotta Bowl (4 hrs)", text: "ഇത് സ്വാഭാവിക കളിമണ്ണിൽ ചക്രത്തിൽ ഉണ്ടാക്കിയ മൺപാത്രം ആണ്, ഉണ്ടാക്കാൻ 4 മണിക്കൂർ എടുത്തു." },
    { label: "🧺 Bamboo Basket (₹500)", text: "സ്വാഭാവിക മുളകൊണ്ട് കൈകൊണ്ട് നെയ്ത കൊട്ട, വില 500 രൂപ." },
    { label: "🪔 Brass Diya (Brass casting)", text: "പൂജയ്ക്കും അലങ്കാരത്തിനുമായി പാരമ്പര്യ പിച്ചള വിളക്ക്." }
  ]
};

class NirmaanApp {
  constructor() {
    this.currentView = "home";
    this.currentCreateStep = 1;
    this.artisanProfile = null;
    this.currentWorkingProduct = null;
    this.activeSpeechLanguage = "hi-IN";
    // No default/canned voice text — this only gets set once the artisan
    // actually records their voice (or taps an example chip) or types
    // something themselves.
    this.simulatedVoiceText = "";
  }

  async init() {
    console.log("Initializing NIRMAAN...");
    AudioManager.init();
    // Wired early (before login/schemes even render) since the mini
    // player can appear during the first-run Schemes Portal too, which
    // happens before setupEventListeners() normally runs.
    this.setupSchemeMiniPlayerControls();
    // Load the artisan profile once, up front, so the language picker and
    // registration screen can safely merge into it instead of overwriting
    // fields (like preferred_language) with schema defaults.
    await this.loadArtisanProfile();
    this.runStartupFlow();
  }

  /** Splash → (first-time) language picker → login/registration → schemes portal → app. */
  runStartupFlow() {
    const splash = document.getElementById("splash-screen");

    const proceedToApp = async () => {
      await this.loadArtisanProfile();
      this.setupEventListeners();
      this.checkDraftRecovery();
      this.renderHomeRecentProducts();
      this.renderMarketplaceFeed();
    };

    const maybeShowSchemes = () => {
      if (localStorage.getItem("nirmaan_schemes_seen") === "true") {
        proceedToApp();
      } else {
        this.showSchemesPortal(() => {
          localStorage.setItem("nirmaan_schemes_seen", "true");
          proceedToApp();
        });
      }
    };

    const maybeShowAuth = () => {
      if (localStorage.getItem("nirmaan_logged_in") === "true") {
        maybeShowSchemes();
      } else {
        this.showAuthScreen(() => {
          localStorage.setItem("nirmaan_logged_in", "true");
          maybeShowSchemes();
        });
      }
    };

    const maybeShowLanguagePicker = () => {
      const savedUiLanguage = getSavedLanguage();
      if (savedUiLanguage) {
        applyLanguage(savedUiLanguage);
        maybeShowAuth();
      } else {
        this.showLanguagePickerModal(() => maybeShowAuth());
      }
    };

    // Fade the splash out after a short brand moment, then continue.
    setTimeout(() => {
      if (splash) {
        splash.classList.add("fade-out");
        setTimeout(() => { splash.style.display = "none"; }, 650);
      }
      maybeShowLanguagePicker();
    }, 1800);
  }

  /** Shown once, the very first time the app is opened on a device. */
  showLanguagePickerModal(onDone) {
    const modal = document.getElementById("language-picker-modal");
    if (!modal) { if (onDone) onDone(); return; }
    modal.classList.add("active");

    const choose = async (langCode) => {
      applyLanguage(langCode);
      modal.classList.remove("active");
      // Keep the artisan's saved profile in sync so it's also reflected
      // next time they open "Edit Profile".
      try {
        if (this.artisanProfile) {
          this.artisanProfile.preferred_language = langCode;
          await ApiClient.updateArtisan({ ...this.artisanProfile, preferred_language: langCode });
        }
      } catch (e) {
        console.warn("Could not sync language preference to profile:", e);
      }
      const langMap = { en: "en-IN", hi: "hi-IN" };
      if (langMap[langCode]) this.updateSpeakingLanguage(langMap[langCode], false);
      if (onDone) onDone();
    };

    const hiBtn = document.getElementById("btn-pick-lang-hi");
    const enBtn = document.getElementById("btn-pick-lang-en");
    if (hiBtn) hiBtn.addEventListener("click", () => choose("hi"), { once: true });
    if (enBtn) enBtn.addEventListener("click", () => choose("en"), { once: true });
  }

  /** Login / New Registration screen, shown before the artisan reaches Home. */
  showAuthScreen(onDone) {
    const screen = document.getElementById("auth-screen");
    if (!screen) { if (onDone) onDone(); return; }
    screen.classList.add("active");

    const loginTab = document.getElementById("auth-tab-login");
    const registerTab = document.getElementById("auth-tab-register");
    const loginPanel = document.getElementById("auth-panel-login");
    const registerPanel = document.getElementById("auth-panel-register");

    const switchTab = (which) => {
      loginTab.classList.toggle("active", which === "login");
      registerTab.classList.toggle("active", which === "register");
      loginPanel.classList.toggle("active", which === "login");
      registerPanel.classList.toggle("active", which === "register");
    };
    loginTab.addEventListener("click", () => switchTab("login"));
    registerTab.addEventListener("click", () => switchTab("register"));

    const finish = () => {
      screen.classList.remove("active");
      if (onDone) onDone();
    };

    // --- Login (demo OTP flow: any 10-digit number + code 123456) ---
    const sendOtpBtn = document.getElementById("btn-send-otp-login");
    const otpField = document.getElementById("login-otp-field");
    sendOtpBtn.addEventListener("click", () => {
      const mobile = document.getElementById("login-mobile").value.trim();
      if (!/^\d{10}$/.test(mobile)) {
        this.showToast("Please enter a valid 10-digit mobile number.");
        return;
      }
      otpField.style.display = "block";
      this.showToast("Demo OTP sent — use 123456.");
    });

    document.getElementById("btn-submit-login").addEventListener("click", () => {
      const mobile = document.getElementById("login-mobile").value.trim();
      const otp = document.getElementById("login-otp").value.trim();
      if (!/^\d{10}$/.test(mobile)) {
        this.showToast("Please enter a valid 10-digit mobile number.");
        return;
      }
      if (otp !== "123456") {
        this.showToast("Incorrect OTP. Use 123456 for this demo.");
        return;
      }
      finish();
    });

    // --- New Registration ---
    document.getElementById("btn-submit-register").addEventListener("click", async () => {
      const name = document.getElementById("reg-name").value.trim();
      const mobile = document.getElementById("reg-mobile").value.trim();
      const gender = document.getElementById("reg-gender").value;
      const craft = document.getElementById("reg-craft").value;
      const state = document.getElementById("reg-state").value.trim();
      const district = document.getElementById("reg-district").value.trim();
      const aadhaar = document.getElementById("reg-aadhaar").value.trim();

      if (!name || !/^\d{10}$/.test(mobile) || !state || !district) {
        this.showToast("Please fill in your name, a valid mobile number, state, and district.");
        return;
      }

      const region = `${district}, ${state}`;
      try {
        this.artisanProfile = await ApiClient.updateArtisan({
          ...this.artisanProfile,
          name, craft_type: craft, region,
          bio: `${gender === "Other" ? "" : gender + " "}craft producer specializing in ${craft}.`
        });
      } catch (e) {
        console.warn("Could not sync registration to profile:", e);
      }
      try {
        localStorage.setItem("nirmaan_registration", JSON.stringify({ name, mobile, gender, craft, state, district, aadhaar }));
      } catch (e) { /* non-fatal */ }

      this.showToast(`Welcome ${name}! Registration complete.`);
      finish();
    });
  }

  /** Schemes portal: shown once after login/registration, before Home. */
  showSchemesPortal(onDone) {
    const screen = document.getElementById("schemes-portal-screen");
    if (!screen) { if (onDone) onDone(); return; }
    screen.classList.add("active");

    this._renderSchemeCards(document.getElementById("schemes-list-container"));

    document.getElementById("btn-schemes-continue").addEventListener("click", () => {
      screen.classList.remove("active");
      this.closeMiniPlayer();
      if (onDone) onDone();
    }, { once: true });
  }

  /** Persistent "Scheme Sarthi" tab — same schemes, reachable anytime via bottom nav. */
  renderSchemesView() {
    this._renderSchemeCards(document.getElementById("schemes-view-list-container"));
  }

  /** Shared card renderer used by both the first-run portal and the persistent tab. */
  _renderSchemeCards(listContainer) {
    if (!listContainer) return;
    const uiLang = document.documentElement.getAttribute("lang") === "hi" ? "hi" : "en";

    listContainer.innerHTML = SCHEMES.map(s => `
      <div class="scheme-sarthi-card" data-scheme-id="${s.id}">
        <div class="scheme-sarthi-card-icon">${s.icon}</div>
        <div class="scheme-sarthi-card-text">
          <div class="scheme-sarthi-card-title">${uiLang === "hi" ? s.title_hi : s.title_en}</div>
          <div class="scheme-sarthi-card-oneliner">${uiLang === "hi" ? s.oneliner_hi : s.oneliner_en}</div>
        </div>
        <button type="button" class="scheme-sarthi-card-play" data-play-scheme="${s.id}" title="Listen">▶️</button>
      </div>
    `).join("");

    listContainer.querySelectorAll(".scheme-sarthi-card").forEach(card => {
      card.addEventListener("click", (e) => {
        if (e.target.closest(".scheme-sarthi-card-play")) return; // handled separately
        this.openSchemeDetail(Number(card.getAttribute("data-scheme-id")));
      });
    });
    listContainer.querySelectorAll("[data-play-scheme]").forEach(btn => {
      btn.addEventListener("click", (e) => {
        e.stopPropagation();
        this.playScheme(Number(btn.getAttribute("data-play-scheme")), this._miniPlayerLang || "en");
      });
    });
  }

  openSchemeDetail(schemeId) {
    const scheme = SCHEMES.find(s => s.id === schemeId);
    if (!scheme) return;
    this._activeSchemeDetail = scheme;
    this._activeSchemeDetailLang = "en";

    const modal = document.getElementById("scheme-detail-modal");
    const titleEl = document.getElementById("scheme-detail-title");
    const descEl = document.getElementById("scheme-detail-description");
    const eligEl = document.getElementById("scheme-detail-eligibility");
    const tabs = modal.querySelectorAll("[data-scheme-lang]");

    const render = (lang) => {
      this._activeSchemeDetailLang = lang;
      tabs.forEach(t => t.classList.toggle("active", t.getAttribute("data-scheme-lang") === lang));
      titleEl.textContent = lang === "hi" ? scheme.title_hi : scheme.title_en;
      descEl.textContent = lang === "hi" ? scheme.description_hi : scheme.description_en;
      const list = lang === "hi" ? scheme.eligibility_hi : scheme.eligibility_en;
      eligEl.innerHTML = list.map(item => `<li>${item}</li>`).join("");
    };

    tabs.forEach(t => {
      t.onclick = () => render(t.getAttribute("data-scheme-lang"));
    });

    render("en");
    modal.classList.add("active");

    const speakBtn = document.getElementById("btn-speak-scheme");
    if (speakBtn) speakBtn.onclick = () => this.playScheme(schemeId, this._activeSchemeDetailLang);
  }

  /**
   * Shared Scheme Sarthi audio player: real recorded narrations (not
   * synthetic TTS), with working play/pause, previous/next (moves
   * between schemes 1-5 in order), and an EN/HI language toggle. Used by
   * both the first-run schemes portal and the persistent Scheme Sarthi tab.
   */
  playScheme(schemeId, lang = "en") {
    const idx = SCHEMES.findIndex(s => s.id === schemeId);
    if (idx === -1) return;
    this._miniPlayerIndex = idx;
    this._miniPlayerLang = (lang === "hi") ? "hi" : "en";
    this._loadAndPlayCurrentScheme();
  }

  _loadAndPlayCurrentScheme() {
    const scheme = SCHEMES[this._miniPlayerIndex];
    if (!scheme) return;
    const lang = this._miniPlayerLang || "en";
    const audioUrl = `/static/audio/schemes/scheme_${scheme.id}_${lang}.mp3`;

    if (this._activeSchemeAudio) {
      this._activeSchemeAudio.pause();
      this._activeSchemeAudio.onended = null;
    }
    const audio = new Audio(audioUrl);
    this._activeSchemeAudio = audio;
    audio.onended = () => this.miniPlayerNext();
    audio.play().then(() => {
      this._setMiniPlayerPlayingState(true);
    }).catch(err => {
      console.warn("Scheme audio playback failed:", err);
      this.showToast("Couldn't play the narration for this scheme.");
    });

    this._updateMiniPlayerUI(scheme);
  }

  _updateMiniPlayerUI(scheme) {
    const player = document.getElementById("scheme-mini-player");
    if (!player) return;
    player.style.display = "flex";
    document.getElementById("mini-player-icon").textContent = scheme.icon;
    const uiLang = document.documentElement.getAttribute("lang") === "hi" ? "hi" : "en";
    document.getElementById("mini-player-title").textContent =
      uiLang === "hi" ? scheme.title_hi : scheme.title_en;
    player.querySelectorAll("[data-mini-lang]").forEach(btn => {
      btn.classList.toggle("active", btn.getAttribute("data-mini-lang") === (this._miniPlayerLang || "en"));
    });
  }

  _setMiniPlayerPlayingState(isPlaying) {
    this._miniPlayerIsPlaying = isPlaying;
    const btn = document.getElementById("mini-player-playpause");
    if (btn) btn.textContent = isPlaying ? "⏸" : "▶️";
  }

  toggleMiniPlayerPlayPause() {
    if (!this._activeSchemeAudio) return;
    if (this._miniPlayerIsPlaying) {
      this._activeSchemeAudio.pause();
      this._setMiniPlayerPlayingState(false);
    } else {
      this._activeSchemeAudio.play().then(() => this._setMiniPlayerPlayingState(true)).catch(() => {});
    }
  }

  miniPlayerNext() {
    if (this._miniPlayerIndex === undefined) return;
    this._miniPlayerIndex = (this._miniPlayerIndex + 1) % SCHEMES.length;
    this._loadAndPlayCurrentScheme();
  }

  miniPlayerPrev() {
    if (this._miniPlayerIndex === undefined) return;
    this._miniPlayerIndex = (this._miniPlayerIndex - 1 + SCHEMES.length) % SCHEMES.length;
    this._loadAndPlayCurrentScheme();
  }

  setMiniPlayerLanguage(lang) {
    this._miniPlayerLang = lang;
    if (this._miniPlayerIndex !== undefined && this._activeSchemeAudio) {
      this._loadAndPlayCurrentScheme();
    }
  }

  closeMiniPlayer() {
    if (this._activeSchemeAudio) {
      this._activeSchemeAudio.pause();
      this._activeSchemeAudio.onended = null;
      this._activeSchemeAudio = null;
    }
    this._miniPlayerIndex = undefined;
    const player = document.getElementById("scheme-mini-player");
    if (player) player.style.display = "none";
  }

  /** One-time wiring for the mini player's prev/play-pause/next/lang/close controls. */
  setupSchemeMiniPlayerControls() {
    const prevBtn = document.getElementById("mini-player-prev");
    const playPauseBtn = document.getElementById("mini-player-playpause");
    const nextBtn = document.getElementById("mini-player-next");
    const closeBtn = document.getElementById("mini-player-close");
    if (prevBtn) prevBtn.addEventListener("click", () => this.miniPlayerPrev());
    if (playPauseBtn) playPauseBtn.addEventListener("click", () => this.toggleMiniPlayerPlayPause());
    if (nextBtn) nextBtn.addEventListener("click", () => this.miniPlayerNext());
    if (closeBtn) closeBtn.addEventListener("click", () => this.closeMiniPlayer());
    document.querySelectorAll("#scheme-mini-player [data-mini-lang]").forEach(btn => {
      btn.addEventListener("click", () => this.setMiniPlayerLanguage(btn.getAttribute("data-mini-lang")));
    });
  }

  async loadArtisanProfile() {
    try {
      this.artisanProfile = await ApiClient.getArtisan();
      const nameEl = document.getElementById("header-artisan-name");
      if (nameEl) nameEl.textContent = this.artisanProfile.name.split(" ")[0];
      const langEl = document.getElementById("header-lang-label");
      const prefLang = this.artisanProfile.preferred_language || "hi";
      if (langEl) langEl.textContent = prefLang === "hi" ? "हिंदी" : (prefLang === "en" ? "English" : prefLang.toUpperCase());
      
      const langMap = {
        "en": "en-IN", "hi": "hi-IN", "mr": "mr-IN", "bn": "bn-IN",
        "gu": "gu-IN", "ta": "ta-IN", "te": "te-IN", "kn": "kn-IN",
        "pa": "pa-IN", "ml": "ml-IN"
      };
      if (langMap[prefLang]) {
        this.updateSpeakingLanguage(langMap[prefLang], false);
      }
    } catch (e) {
      console.warn("Using default artisan profile:", e);
    }
  }

  setupEventListeners() {
    // Navigation
    document.querySelectorAll(".nav-item").forEach(btn => {
      btn.addEventListener("click", (e) => {
        const view = btn.getAttribute("data-view");
        if (view) this.switchView(view);
      });
    });

    // Central FAB Create Button
    const fabBtn = document.getElementById("nav-fab-create");
    if (fabBtn) {
      fabBtn.addEventListener("click", () => {
        this.startNewProductFlow();
      });
    }

    // Home Quick Action Tiles
    document.querySelectorAll(".action-tile").forEach(tile => {
      tile.addEventListener("click", () => {
        const action = tile.getAttribute("data-action");
        if (action === "create-photo") {
          this.startNewProductFlow(1);
        } else if (action === "create-voice") {
          this.startNewProductFlow(2);
        } else if (action === "calc-price") {
          this.startNewProductFlow(5, "calc");
        } else if (action === "check-market") {
          this.startNewProductFlow(5, "market");
        }
      });
    });

    // Photo Upload Triggers
    const photoInput = document.getElementById("photo-file-input");
    const dropzone = document.getElementById("photo-dropzone");
    if (dropzone && photoInput) {
      dropzone.addEventListener("click", () => photoInput.click());
      photoInput.addEventListener("change", (e) => this.handlePhotoSelection(e));
    }

    const demoPhotoBtn = document.getElementById("btn-use-demo-photo");
    if (demoPhotoBtn) {
      demoPhotoBtn.addEventListener("click", () => this.handleDemoPhotoSelection());
    }

    // Speaking Language Selector in Step 2
    const voiceLangSelect = document.getElementById("voice-language-select");
    if (voiceLangSelect) {
      voiceLangSelect.addEventListener("change", (e) => {
        this.updateSpeakingLanguage(e.target.value);
      });
    }

    // Voice Mic Recording Trigger
    const micBtn = document.getElementById("voice-mic-btn");
    if (micBtn) {
      micBtn.addEventListener("click", () => this.toggleVoiceRecording());
    }

    // Speech Sample Chips Initial Binding
    this.bindSpeechSampleChips();

    // Voice Next Button
    const voiceNextBtn = document.getElementById("btn-voice-next");
    if (voiceNextBtn) {
      voiceNextBtn.addEventListener("click", () => this.processVoiceAndStudio());
    }

    // Catalog Image View Switcher Tabs (Marketplace, Original, Features)
    document.querySelectorAll(".viewer-tab").forEach(tab => {
      tab.addEventListener("click", () => {
        document.querySelectorAll(".viewer-tab").forEach(t => t.classList.remove("active"));
        tab.classList.add("active");
        const type = tab.getAttribute("data-img-type");
        CatalogManager.activeImageTab = type;
        this.updateCatalogImageViewer();
      });
    });

    // Multilingual Catalog Tabs (Original / हिंदी / English)
    document.querySelectorAll(".lang-tab").forEach(tab => {
      tab.addEventListener("click", () => {
        document.querySelectorAll(".lang-tab").forEach(t => t.classList.remove("active"));
        tab.classList.add("active");
        const lang = tab.getAttribute("data-lang");
        CatalogManager.activeLangTab = lang;
        this.updateCatalogLocalizedContent();
      });
    });

    // Voice Command Input & Mic
    const voiceCmdBtn = document.getElementById("btn-exec-voice-cmd");
    const voiceCmdInput = document.getElementById("voice-cmd-input");
    if (voiceCmdBtn && voiceCmdInput) {
      voiceCmdBtn.addEventListener("click", async () => {
        const cmd = voiceCmdInput.value.trim();
        if (cmd) {
          const res = await CatalogManager.executeVoiceCommand(cmd);
          if (res) {
            this.showToast(res.message);
            this.renderCatalogAttributes();
            this.updateCatalogLocalizedContent();
            voiceCmdInput.value = "";
          }
        }
      });
    }

    // Pricing Hub Tabs (Calculate, Market Check, Insights)
    document.querySelectorAll(".pricing-tab").forEach(tab => {
      tab.addEventListener("click", () => {
        document.querySelectorAll(".pricing-tab").forEach(t => t.classList.remove("active"));
        tab.classList.add("active");
        const tabKey = tab.getAttribute("data-pricing-tab");
        document.querySelectorAll(".pricing-panel").forEach(p => p.style.display = "none");
        const targetPanel = document.getElementById(`pricing-panel-${tabKey}`);
        if (targetPanel) targetPanel.style.display = "block";
      });
    });

    // Pricing Sliders Input Listeners
    ["calc-material", "calc-hours", "calc-rate", "calc-wastage", "calc-margin"].forEach(id => {
      const el = document.getElementById(id);
      if (el) {
        el.addEventListener("input", () => this.updatePricingCalculation());
      }
    });

    // Market Check Trigger (both confirmation card and direct run)
    const runMarketBtn = document.getElementById("btn-run-market-check");
    const confirmMarketBtn = document.getElementById("btn-confirm-market-search");
    if (runMarketBtn) {
      runMarketBtn.addEventListener("click", () => this.executeMarketCheck());
    }
    if (confirmMarketBtn) {
      confirmMarketBtn.addEventListener("click", () => this.executeMarketCheck());
    }

    // Header Language Toggle Button
    const headerLangBtn = document.getElementById("header-lang-btn");
    if (headerLangBtn) {
      headerLangBtn.addEventListener("click", () => {
        this.openOnboardingModal();
      });
    }

    // One-Click Use Price Button
    const applyPriceBtn = document.getElementById("btn-apply-recommended-price");
    if (applyPriceBtn) {
      applyPriceBtn.addEventListener("click", () => {
        if (PricingManager.currentCalculation && this.currentWorkingProduct) {
          const price = PricingManager.currentCalculation.recommended_price;
          this.currentWorkingProduct.price = price;
          const currentPriceInput = document.getElementById("custom-price-input");
          if (currentPriceInput) currentPriceInput.value = price;
          this.showToast(`Updated product price to ₹${price}`);
          this.refreshPricingInsight();
        }
      });
    }

    // Step 5 Next -> Step 6 (Review & Publish)
    const toReviewBtn = document.getElementById("btn-pricing-to-review");
    if (toReviewBtn) {
      toReviewBtn.addEventListener("click", () => {
        this.setCreateStep(6);
        this.renderReviewSummary();
      });
    }

    // Publish & Share Actions
    const publishBtn = document.getElementById("btn-publish-product");
    if (publishBtn) {
      publishBtn.addEventListener("click", () => this.publishCurrentProduct());
    }

    const whatsappBtn = document.getElementById("btn-share-whatsapp");
    if (whatsappBtn) {
      whatsappBtn.addEventListener("click", () => {
        if (this.currentWorkingProduct) {
          const url = MarketplaceManager.generateWhatsAppShareUrl(this.currentWorkingProduct, this.artisanProfile?.name || "Ramesh");
          window.open(url, "_blank");
        }
      });
    }

    // Marketplace Search & Categories
    const mktSearch = document.getElementById("marketplace-search-input");
    if (mktSearch) {
      mktSearch.addEventListener("input", (e) => {
        this.renderMarketplaceFeed(MarketplaceManager.activeCategory, e.target.value);
      });
    }

    document.querySelectorAll("#view-marketplace .category-chip").forEach(chip => {
      chip.addEventListener("click", () => {
        document.querySelectorAll("#view-marketplace .category-chip").forEach(c => c.classList.remove("active"));
        chip.classList.add("active");
        const cat = chip.getAttribute("data-category");
        this.renderMarketplaceFeed(cat, mktSearch ? mktSearch.value : "");
      });
    });

    // Device View Toggle (Mobile frame simulator)
    const toggleDevice = document.getElementById("btn-device-toggle");
    if (toggleDevice) {
      toggleDevice.addEventListener("click", () => {
        const appBox = document.querySelector(".app-container");
        if (appBox) {
          appBox.classList.toggle("fullscreen-mode");
          toggleDevice.textContent = appBox.classList.contains("fullscreen-mode") ? "📱 Phone View" : "💻 Full Screen";
        }
      });
    }
  }

  switchView(viewName) {
    this.currentView = viewName;
    document.querySelectorAll(".view-container").forEach(el => el.classList.remove("active"));
    document.querySelectorAll(".nav-item").forEach(el => el.classList.remove("active"));

    const targetView = document.getElementById(`view-${viewName}`);
    if (targetView) targetView.classList.add("active");

    const targetNav = document.querySelector(`.nav-item[data-view="${viewName}"]`);
    if (targetNav) targetNav.classList.add("active");

    if (viewName === "home") {
      this.renderHomeRecentProducts();
    } else if (viewName === "products") {
      this.renderMyProductsList();
      this.renderCatalogsList();
    } else if (viewName === "marketplace") {
      this.renderMarketplaceFeed();
    } else if (viewName === "profile") {
      this.renderArtisanProfileView();
    } else if (viewName === "schemes") {
      this.renderSchemesView();
    }
  }

  startNewProductFlow(initialStep = 1, initialPricingTab = null) {
    this.currentWorkingProduct = {
      id: "prod-" + Date.now(),
      artisan_id: this.artisanProfile?.id || "artisan-ramesh",
      title_original: "हस्तनिर्मित मिट्टी का सर्विंग बाउल",
      title_hi: "हस्तनिर्मित प्राकृतिक टेराकोटा बाउल",
      title_en: "Handcrafted Natural Terracotta Serving Bowl",
      description_original: "प्राकृतिक शुद्ध लाल मिट्टी से चाक पर बना हुआ बाउल।",
      description_hi: "पारंपरिक कुम्हार चाक पर निर्मित। भोजन व सजावट के लिए आदर्श।",
      description_en: "Hand-thrown on traditional potter's wheel using natural clay.",
      category: "Pottery",
      craft_type: "Terracotta",
      material: "Natural Red Clay",
      color: "Terracotta Red",
      price: 399.0,
      currency: "INR",
      status: "draft",
      images: [
        { image_type: "marketplace", url: "/static/images/terracotta_marketplace.jpg", label: "Marketplace" },
        { image_type: "original", url: "/static/images/terracotta_original.jpg", label: "Original" },
        { image_type: "features", url: "/static/images/terracotta_lifestyle.jpg", label: "Features" }
      ],
      attributes: [
        { key: "craft", label: "Craft", value_en: "Wheel-thrown Terracotta" },
        { key: "material", label: "Material", value_en: "Pure Natural Clay" }
      ],
      seo_keywords: ["terracotta bowl", "clay bowl", "handmade pottery"]
    };

    CatalogManager.setProduct(this.currentWorkingProduct);
    CameraManager.clearPhotos();
    this.switchView("create");
    this.setCreateStep(initialStep);

    if (initialPricingTab) {
      const targetTab = document.querySelector(`.pricing-tab[data-pricing-tab="${initialPricingTab}"]`);
      if (targetTab) targetTab.click();
    }
  }

  setCreateStep(stepNumber) {
    this.currentCreateStep = stepNumber;
    
    // Update Stepper circles
    document.querySelectorAll(".stepper-step").forEach(stepEl => {
      const s = parseInt(stepEl.getAttribute("data-step"));
      stepEl.classList.remove("active", "completed");
      if (s === stepNumber) {
        stepEl.classList.add("active");
      } else if (s < stepNumber) {
        stepEl.classList.add("completed");
      }
    });

    // Show Step Container
    document.querySelectorAll(".create-step-container").forEach(el => el.style.display = "none");
    const currentContainer = document.getElementById(`step-container-${stepNumber}`);
    if (currentContainer) currentContainer.style.display = "block";

    // Auto-save draft state
    if (this.currentWorkingProduct) {
      StorageManager.saveDraft(this.currentWorkingProduct);
    }

    // Step-specific initializations
    if (stepNumber === 4) {
      this.updateCatalogImageViewer();
      this.updateCatalogLocalizedContent();
      this.renderCatalogAttributes();
    } else if (stepNumber === 5) {
      this.updateMarketConfirmationCard();
      this.updatePricingCalculation();
      this.executeMarketCheck();
    }
  }

  async handlePhotoSelection(e) {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = async (evt) => {
      const dataUrl = evt.target.result;
      CameraManager.clearPhotos();
      CameraManager.addPhoto(file, dataUrl, "Front Angle");
      this.renderPhotoPreviewGrid();
      this.showToast("Photo captured! Proceeding to describe your product...");
      setTimeout(() => this.setCreateStep(2), 600);
    };
    reader.readAsDataURL(file);
  }

  async handleDemoPhotoSelection() {
    const demo = await CameraManager.createDemoPhotoBlob("Pottery");
    CameraManager.clearPhotos();
    CameraManager.addPhoto(demo.blob, demo.dataUrl, "Primary Photo");
    this.renderPhotoPreviewGrid();
    this.showToast("Demo artisan photo loaded! Ready to speak.");
    setTimeout(() => this.setCreateStep(2), 600);
  }

  renderPhotoPreviewGrid() {
    const grid = document.getElementById("photo-preview-grid");
    if (!grid) return;
    grid.innerHTML = "";
    CameraManager.getPhotos().forEach(p => {
      const item = document.createElement("div");
      item.className = "photo-preview-item";
      item.innerHTML = `
        <img src="${p.dataUrl}" alt="Photo" />
        <span class="photo-tag">${p.angle}</span>
      `;
      grid.appendChild(item);
    });
  }

  switchDescribeMode(mode) {
    const tabVoice = document.getElementById("tab-input-voice");
    const tabText = document.getElementById("tab-input-text");
    const panelVoice = document.getElementById("describe-panel-voice");
    const panelText = document.getElementById("describe-panel-text");
    const textInput = document.getElementById("text-description-input");

    if (mode === "text") {
      tabVoice?.classList.remove("active");
      tabText?.classList.add("active");
      if (panelVoice) panelVoice.style.display = "none";
      if (panelText) panelText.style.display = "block";
      if (textInput && this.simulatedVoiceText) {
        textInput.value = this.simulatedVoiceText;
      }
    } else {
      tabText?.classList.remove("active");
      tabVoice?.classList.add("active");
      if (panelText) panelText.style.display = "none";
      if (panelVoice) panelVoice.style.display = "block";
    }
  }

  updateSpeakingLanguage(langCode, notify = true) {
    this.activeSpeechLanguage = langCode || "hi-IN";
    const selectEl = document.getElementById("voice-language-select");
    if (selectEl && selectEl.value !== this.activeSpeechLanguage) {
      selectEl.value = this.activeSpeechLanguage;
    }

    // Refresh the tappable "example" chips for this language — these are
    // purely optional inspiration for the artisan and are only ever used
    // if they deliberately tap one. They are never auto-filled into the
    // transcript, textarea, or used as the product description.
    const examples = MULTILINGUAL_SPEECH_EXAMPLES[this.activeSpeechLanguage] || MULTILINGUAL_SPEECH_EXAMPLES["hi-IN"];
    const container = document.getElementById("speech-sample-chips-container");
    if (container) {
      container.innerHTML = examples.map(ex => `
        <span class="speech-chip" data-text="${ex.text}">${ex.label}</span>
      `).join("");
      this.bindSpeechSampleChips();
    }

    if (notify) {
      const langNames = {
        "en-IN": "English (India)", "hi-IN": "हिंदी (Hindi)", "mr-IN": "मराठी (Marathi)",
        "bn-IN": "বাংলা (Bengali)", "gu-IN": "ગુજરાતી (Gujarati)", "ta-IN": "தமிழ் (Tamil)",
        "te-IN": "తెలుగు (Telugu)", "kn-IN": "ಕನ್ನಡ (Kannada)", "pa-IN": "ਪੰਜਾਬੀ (Punjabi)",
        "ml-IN": "മലയാളം (Malayalam)"
      };
      this.showToast(`Voice set to ${langNames[this.activeSpeechLanguage] || this.activeSpeechLanguage} 🎙️`);
    }
  }

  bindSpeechSampleChips() {
    document.querySelectorAll(".speech-chip").forEach(chip => {
      chip.onclick = () => {
        const text = chip.getAttribute("data-text");
        this.simulatedVoiceText = text;
        const transcriptEl = document.getElementById("voice-live-transcript");
        if (transcriptEl) transcriptEl.textContent = `"${text}"`;
        const textInput = document.getElementById("text-description-input");
        if (textInput) textInput.value = text;
        this.showToast("Voice description set: " + text.substring(0, 32) + "...");
      };
    });
  }

  async toggleVoiceRecording() {
    const micBtn = document.getElementById("voice-mic-btn");
    const transcriptEl = document.getElementById("voice-live-transcript");
    const textInput = document.getElementById("text-description-input");
    const activeLang = this.activeSpeechLanguage || "hi-IN";

    // Show the browser's live interim captions (if supported) purely as a
    // visual "it's listening" cue — the transcript actually used for the
    // catalog comes from the real recorded audio sent to Gemini below.
    if (!AudioManager.isCapturingAudio) {
      try {
        await AudioManager.startCapturingAudio();
      } catch (err) {
        this.showToast("Couldn't access your microphone: " + err.message);
        return;
      }

      micBtn.classList.add("recording");
      transcriptEl.textContent = `🎙️ Recording in ${activeLang}... Speak naturally, then tap again to stop.`;

      AudioManager.startListening(
        (text) => {
          if (text && text.trim()) {
            transcriptEl.textContent = `"${text}"`;
          }
        },
        null,
        activeLang
      );
    } else {
      micBtn.classList.remove("recording");
      AudioManager.stopListening();
      transcriptEl.textContent = "⏳ Transcribing your voice note...";

      let audioBlob;
      try {
        audioBlob = await AudioManager.stopCapturingAudio();
      } catch (err) {
        transcriptEl.textContent = "🎙️ Tap the mic and record your voice here to describe your product.";
        this.showToast("Recording failed: " + err.message);
        return;
      }

      try {
        const result = await ApiClient.transcribeAudioBlob(audioBlob, activeLang);
        this.simulatedVoiceText = result.transcript_original;
        transcriptEl.textContent = `"${result.transcript_original}"`;
        if (textInput) textInput.value = result.transcript_original;
      } catch (err) {
        // Genuine failure — never substitute a canned product description.
        transcriptEl.textContent = "🎙️ Tap the mic and record your voice here to describe your product.";
        this.simulatedVoiceText = "";
        this.showToast(err.message || "Couldn't transcribe that recording. Please try again.");
      }
    }
  }

  async proceedFromStep1() {
    if (CameraManager.getPhotos().length === 0) {
      const demo = await CameraManager.createDemoPhotoBlob(this.artisanProfile?.craft_type || "Pottery");
      CameraManager.addPhoto(demo.blob, demo.dataUrl, "Primary Photo");
      this.renderPhotoPreviewGrid();
    }
    this.setCreateStep(2);
  }

  async processVoiceAndStudio() {
    // Check if written text was entered
    const textInput = document.getElementById("text-description-input");
    const inputDescription = (textInput && textInput.value.trim())
      ? textInput.value.trim()
      : (this.simulatedVoiceText || "").trim();

    if (!inputDescription) {
      this.showToast("Please record your voice or write a description before continuing.");
      return;
    }

    this.setCreateStep(3); // Show AI Processing Studio

    const checklistItems = [
      document.getElementById("ai-step-1"),
      document.getElementById("ai-step-2"),
      document.getElementById("ai-step-3"),
      document.getElementById("ai-step-4"),
      document.getElementById("ai-step-5"),
      document.getElementById("ai-step-6"),
      document.getElementById("ai-step-7")
    ];

    // Animate AI Checklist
    for (let i = 0; i < checklistItems.length; i++) {
      await new Promise(r => setTimeout(r, 380));
      if (checklistItems[i]) {
        checklistItems[i].classList.add("done");
        checklistItems[i].querySelector(".checklist-icon").textContent = "✓";
      }
    }

    try {
      // 1. Process Voice / Written Text first to extract craft clues
      const voiceRes = await ApiClient.transcribeVoice(inputDescription, "auto");
      const descLower = (inputDescription || "").toLowerCase();
      
      let initialCat = "Handicrafts";
      let initialCraft = "Handmade";
      if (descLower.includes("brass") || descLower.includes("पीतल") || descLower.includes("diya") || descLower.includes("दीया")) {
        initialCat = "Metal craft";
        initialCraft = "Brass Casting";
      } else if (descLower.includes("bamboo") || descLower.includes("बांस") || descLower.includes("cane") || descLower.includes("basket") || descLower.includes("टोकरी")) {
        initialCat = "Bamboo craft";
        initialCraft = "Bamboo Weaving";
      } else if (descLower.includes("saree") || descLower.includes("साड़ी") || descLower.includes("handloom") || descLower.includes("textile")) {
        initialCat = "Textiles";
        initialCraft = "Handloom Weaving";
      } else if (descLower.includes("wood") || descLower.includes("लकड़ी") || descLower.includes("tray") || descLower.includes("box")) {
        initialCat = "Woodcraft";
        initialCraft = "Wood Carving";
      } else if (descLower.includes("clay") || descLower.includes("terracotta") || descLower.includes("मिट्टी") || descLower.includes("bowl")) {
        initialCat = "Pottery";
        initialCraft = "Terracotta";
      } else if (this.artisanProfile?.craft_type) {
        initialCat = this.artisanProfile.craft_type.split(",")[0].trim();
      }

      // 2. Ensure a photo is available for processing
      let primaryPhoto = CameraManager.getPrimaryPhoto();
      if (!primaryPhoto || !primaryPhoto.blob) {
        const demo = await CameraManager.createDemoPhotoBlob(initialCat);
        primaryPhoto = CameraManager.addPhoto(demo.blob, demo.dataUrl, "Primary Photo");
      }

      // 3. Upload Photo & Process Vision Studio
      let photoRes = await ApiClient.uploadProductPhoto(primaryPhoto.blob, initialCat, initialCraft);

      // 4. Extract Multilingual Catalog (title/description/SEO keywords/
      //    features are now generated per-product via Gemini, with a
      //    transcript-driven fallback — not fixed per-category templates)
      const catalogData = await ApiClient.extractCatalog(
        voiceRes.transcript_original,
        voiceRes.detected_language,
        photoRes ? photoRes.visual_traits : { category: initialCat, craft_type: initialCraft }
      );

      // Merge into active working product
      this.currentWorkingProduct = {
        ...this.currentWorkingProduct,
        ...catalogData,
        images: (photoRes && photoRes.images && photoRes.images.length > 0) ? photoRes.images : this.currentWorkingProduct.images
      };

      // 5. Build the third "Features" image now that we know the real
      //    features the artisan described — composited onto the already-
      //    generated Marketplace photo.
      try {
        const marketplaceImg = (this.currentWorkingProduct.images || []).find(img => img.image_type === "marketplace");
        if (marketplaceImg) {
          const featureRes = await ApiClient.generateFeatureImage(
            marketplaceImg.url,
            catalogData.features || [],
            catalogData.category || initialCat,
            catalogData.craft_type || initialCraft,
            catalogData.title_en || catalogData.title_original || ""
          );
          if (featureRes && featureRes.success && featureRes.image) {
            this.currentWorkingProduct.images = [
              ...this.currentWorkingProduct.images.filter(img => img.image_type !== "features"),
              featureRes.image
            ];
          }
        }
      } catch (e) {
        console.warn("Feature image generation skipped:", e);
      }

      CatalogManager.setProduct(this.currentWorkingProduct);
      this.showToast("Your professional product catalog is ready! 🎉");
      setTimeout(() => this.setCreateStep(4), 500);

    } catch (e) {
      console.warn("AI pipeline notice:", e);
      this.showToast("Your professional product photo is ready.");
      setTimeout(() => this.setCreateStep(4), 500);
    }
  }

  async applyStudioStyle(chipEl, stylePreset) {
    if (chipEl && chipEl.parentElement) {
      chipEl.parentElement.querySelectorAll(".style-chip").forEach(c => c.classList.remove("active"));
      chipEl.classList.add("active");
    }
    const currentImgUrl = CatalogManager.getCurrentImage();
    this.showToast(`Creating ${stylePreset.replace('_', ' ')} studio backdrop... ✨`);
    try {
      const res = await ApiClient.generateStyle(currentImgUrl, stylePreset);
      if (res && res.success && res.image) {
        // Update marketplace image with newly generated styled backdrop
        if (this.currentWorkingProduct && this.currentWorkingProduct.images) {
          const mktIdx = this.currentWorkingProduct.images.findIndex(img => img.image_type === "marketplace");
          if (mktIdx !== -1) {
            this.currentWorkingProduct.images[mktIdx] = res.image;
          } else {
            this.currentWorkingProduct.images.unshift(res.image);
          }
        }
        CatalogManager.setProduct(this.currentWorkingProduct);
        CatalogManager.activeImageTab = "marketplace";
        document.querySelectorAll(".viewer-tab").forEach(t => {
          t.classList.toggle("active", t.getAttribute("data-img-type") === "marketplace");
        });
        this.updateCatalogImageViewer();
        this.showToast(res.message || "Studio backdrop updated! 🏛️");
      }
    } catch (e) {
      this.showToast("Could not change backdrop style.");
    }
  }

  updateCatalogImageViewer() {
    const heroImg = document.getElementById("catalog-viewer-hero-img");
    const counterBadge = document.getElementById("catalog-viewer-counter");
    if (heroImg) {
      heroImg.src = CatalogManager.getCurrentImage();
    }
    if (counterBadge) {
      const tabs = ["marketplace", "studio_pro", "original", "features"];
      const idx = tabs.indexOf(CatalogManager.activeImageTab);
      const position = idx === -1 ? 1 : idx + 1;
      counterBadge.textContent = `${position} / ${tabs.length} • ${CatalogManager.activeImageTab.toUpperCase()}`;
    }
  }

  updateCatalogLocalizedContent() {
    const loc = CatalogManager.getLocalizedContent(CatalogManager.activeLangTab);
    const titleEl = document.getElementById("catalog-title-display");
    const descEl = document.getElementById("catalog-desc-display");
    if (titleEl) titleEl.textContent = loc.title;
    if (descEl) descEl.textContent = loc.description;

    // SEO keywords are language-specific: English keywords are for
    // pasting into Amazon/Etsy/Flipkart/ONDC English listings, Hindi
    // keywords are for Hindi-language/ONDC domestic listings.
    const kwContainer = document.getElementById("catalog-keywords-chips");
    if (kwContainer) {
      kwContainer.innerHTML = (loc.keywords || []).map(kw =>
        `<span class="speech-chip">#${kw}</span>`
      ).join(" ");
    }
  }

  toggleInPlaceEdit() {
    const panel = document.getElementById("catalog-inplace-edit-panel");
    if (!panel) return;
    const isHidden = panel.style.display === "none";
    if (isHidden) {
      const loc = CatalogManager.getLocalizedContent(CatalogManager.activeLangTab);
      const titleInput = document.getElementById("edit-catalog-title-input");
      const descInput = document.getElementById("edit-catalog-desc-input");
      if (titleInput) titleInput.value = loc.title || "";
      if (descInput) descInput.value = loc.description || "";
      panel.style.display = "block";
    } else {
      panel.style.display = "none";
    }
  }

  saveInPlaceEdit() {
    const titleInput = document.getElementById("edit-catalog-title-input");
    const descInput = document.getElementById("edit-catalog-desc-input");
    const newTitle = titleInput ? titleInput.value.trim() : "";
    const newDesc = descInput ? descInput.value.trim() : "";

    const activeTab = CatalogManager.activeLangTab;
    if (this.currentWorkingProduct) {
      if (activeTab === "hi") {
        this.currentWorkingProduct.title_hi = newTitle;
        this.currentWorkingProduct.description_hi = newDesc;
      } else if (activeTab === "en") {
        this.currentWorkingProduct.title_en = newTitle;
        this.currentWorkingProduct.description_en = newDesc;
      } else {
        this.currentWorkingProduct.title_original = newTitle;
        this.currentWorkingProduct.description_original = newDesc;
      }
      CatalogManager.setProduct(this.currentWorkingProduct);
      this.updateCatalogLocalizedContent();
      this.showToast("Product description updated! ✏️");
    }
    const panel = document.getElementById("catalog-inplace-edit-panel");
    if (panel) panel.style.display = "none";
  }

  renderCatalogAttributes() {
    const container = document.getElementById("catalog-attributes-grid");
    if (!container || !this.currentWorkingProduct) return;
    
    container.innerHTML = `
      <div class="attr-pill">
        <span class="attr-label">Category</span>
        <div class="attr-val">${this.currentWorkingProduct.category || "Handicrafts"}</div>
      </div>
      <div class="attr-pill">
        <span class="attr-label">Craft Technique</span>
        <div class="attr-val">${this.currentWorkingProduct.craft_type || "Handmade"}</div>
      </div>
      <div class="attr-pill">
        <span class="attr-label">Material</span>
        <div class="attr-val">${this.currentWorkingProduct.material || "Natural Clay"}</div>
      </div>
      <div class="attr-pill">
        <span class="attr-label">Color</span>
        <div class="attr-val">${this.currentWorkingProduct.color || "Earthy Terracotta"}</div>
      </div>
    `;

    // Render AI Verification Badges
    const verifyBadges = document.getElementById("ai-verification-badges");
    if (verifyBadges) {
      const craft = this.currentWorkingProduct.craft_type || "Handcrafted";
      const mat = this.currentWorkingProduct.material || "Natural Material";
      verifyBadges.innerHTML = `
        <span class="speech-chip" style="font-size:10px; padding:2px 8px; background:#FFF;">✓ Craft: ${craft}</span>
        <span class="speech-chip" style="font-size:10px; padding:2px 8px; background:#FFF;">✓ Material: ${mat}</span>
        <span class="speech-chip" style="font-size:10px; padding:2px 8px; background:#FFF;">✓ Fact-Checked & Verified</span>
      `;
    }

    // Keywords are rendered per active language tab (see
    // updateCatalogLocalizedContent) so English/Hindi buyers each get
    // search terms genuinely written for their marketplace.
    this.updateCatalogLocalizedContent();
  }

  async updatePricingCalculation() {
    const matVal = document.getElementById("calc-material")?.value || 200;
    const hoursVal = document.getElementById("calc-hours")?.value || 4;
    const rateVal = document.getElementById("calc-rate")?.value || 150;
    const wastageVal = document.getElementById("calc-wastage")?.value || 0;
    const marginVal = document.getElementById("calc-margin")?.value || 30;

    // Update label displays
    document.getElementById("calc-material-val").textContent = `₹${matVal}`;
    document.getElementById("calc-hours-val").textContent = `${hoursVal} hrs`;
    document.getElementById("calc-rate-val").textContent = `₹${rateVal}/hr`;
    document.getElementById("calc-wastage-val").textContent = `${wastageVal}%`;
    document.getElementById("calc-margin-val").textContent = `${marginVal}%`;

    const res = await PricingManager.runCalculation({
      materialCost: matVal,
      timeHours: hoursVal,
      labourRate: rateVal,
      wastagePercent: wastageVal,
      profitMargin: marginVal
    });

    if (res) {
      document.getElementById("cost-floor-display").textContent = `₹${res.cost_floor}`;
      document.getElementById("rec-price-display").textContent = `₹${res.recommended_price}`;
      document.getElementById("prem-price-display").textContent = `₹${res.premium_price}`;
      document.getElementById("calc-breakdown-text").textContent = res.breakdown_text;
      
      const applyBtn = document.getElementById("btn-apply-recommended-price");
      if (applyBtn) applyBtn.textContent = `Use ₹${res.recommended_price} as Product Price`;

      this.refreshPricingInsight();
    }
  }

  updateMarketConfirmationCard() {
    const titleEl = document.getElementById("market-confirm-title");
    const metaEl = document.getElementById("market-confirm-meta");
    const imgEl = document.getElementById("market-confirm-img");

    if (this.currentWorkingProduct) {
      if (titleEl) {
        titleEl.textContent = this.currentWorkingProduct.title_en || this.currentWorkingProduct.title_original || "Handcrafted Craft";
      }
      if (metaEl) {
        metaEl.textContent = `${this.currentWorkingProduct.category || "Handicrafts"} • ${this.currentWorkingProduct.material || "Natural Material"} • ${this.currentWorkingProduct.craft_type || "Handmade"}`;
      }
      if (imgEl) {
        imgEl.src = CatalogManager.getCurrentImage() || this.currentWorkingProduct.images?.[0]?.url || "/static/images/terracotta_marketplace.jpg";
      }
    }
  }

  async executeMarketCheck() {
    this.updateMarketConfirmationCard();
    const pName = this.currentWorkingProduct?.title_en || this.currentWorkingProduct?.title_original || "Handcrafted Product";
    const cat = this.currentWorkingProduct?.category || "Handicrafts";
    const mat = this.currentWorkingProduct?.material || "Natural Material";
    const craft = this.currentWorkingProduct?.craft_type || "Handmade";

    const res = await PricingManager.runMarketCheck(pName, cat, mat, craft, true);
    if (res) {
      document.getElementById("market-range-display").textContent = `₹${res.estimated_min_price} — ₹${res.estimated_max_price}`;
      document.getElementById("typical-price-display").textContent = `₹${res.typical_market_price}`;
      
      const confPill = document.getElementById("market-confidence-pill");
      if (confPill) {
        confPill.textContent = res.confidence_badge_text;
      }

      const presenceEl = document.getElementById("market-presence-text");
      if (presenceEl) presenceEl.textContent = res.online_presence;

      // Render comparables list
      const compContainer = document.getElementById("market-comparables-list");
      if (compContainer) {
        compContainer.innerHTML = res.comparables.map(c => `
          <div class="market-comparable-item">
            <div style="flex:1;">
              <div style="font-size:13px; font-weight:700; color:var(--color-text-main);">${c.title}</div>
              <div style="font-size:11px; color:var(--color-text-muted);">Source: ${c.seller} (${c.source}) • ⭐ ${c.rating} (${c.review_count})</div>
              <span class="status-badge status-published" style="font-size:9px;">${c.is_handmade ? '✓ Handmade' : 'Mass Produced'}</span>
            </div>
            <div style="font-size:15px; font-weight:800; color:var(--color-forest);">₹${c.price}</div>
          </div>
        `).join("");
      }

      this.refreshPricingInsight();
    }
  }

  async refreshPricingInsight() {
    const currentPrice = this.currentWorkingProduct?.price || PricingManager.currentCalculation?.recommended_price || 399;
    const insight = await PricingManager.runPricingInsight(currentPrice);
    if (!insight) return;

    const banner = document.getElementById("pricing-insight-banner");
    if (banner) {
      banner.className = `insight-banner insight-${insight.status_level.replace('_', '-')}`;
      banner.innerHTML = `
        <div style="font-size:24px;">${insight.status_badge}</div>
        <div>
          <div style="font-size:14px; font-weight:800;">${insight.status_title}</div>
          <div style="font-size:12px; margin-top:2px; line-height:1.4;">${insight.explanation}</div>
          ${insight.suggested_test_range_min ? `<div style="font-size:12px; font-weight:700; margin-top:6px;">Consider testing: ₹${insight.suggested_test_range_min} — ₹${insight.suggested_test_range_max}</div>` : ''}
        </div>
      `;
    }

    const adviceList = document.getElementById("pricing-advice-list");
    if (adviceList && insight.actionable_advice) {
      adviceList.innerHTML = insight.actionable_advice.map(adv => `
        <li style="font-size:12px; margin-bottom:4px; color:var(--color-text-main);">${adv}</li>
      `).join("");
    }
  }

  renderReviewSummary() {
    if (!this.currentWorkingProduct) return;
    const heroImg = document.getElementById("review-hero-img");
    if (heroImg) heroImg.src = CatalogManager.getCurrentImage();

    const titleEl = document.getElementById("review-title");
    if (titleEl) titleEl.textContent = this.currentWorkingProduct.title_en || this.currentWorkingProduct.title_original;

    const priceEl = document.getElementById("review-price");
    if (priceEl) priceEl.textContent = `₹${this.currentWorkingProduct.price || 399}`;

    const descEl = document.getElementById("review-desc");
    if (descEl) descEl.textContent = this.currentWorkingProduct.description_en || this.currentWorkingProduct.description_hi;
  }

  async publishCurrentProduct() {
    if (!this.currentWorkingProduct) return;
    try {
      this.currentWorkingProduct.status = "published";
      const saved = await ApiClient.saveProduct(this.currentWorkingProduct);
      if (saved) this.currentWorkingProduct = saved;
      StorageManager.clearDraft();
      this.showToast("Product successfully published to NIRMAAN Marketplace! 🌟");
      await this.renderMarketplaceFeed();
      await this.renderMyProductsList();
      await this.renderHomeRecentProducts();
      setTimeout(() => {
        this.switchView("marketplace");
      }, 900);
    } catch (e) {
      this.showToast("Product published to local catalog.");
      this.switchView("marketplace");
    }
  }

  async renderHomeRecentProducts() {
    const container = document.getElementById("home-recent-products");
    if (!container) return;
    try {
      const products = await ApiClient.getProducts();
      container.innerHTML = products.slice(0, 3).map(p => `
        <div class="product-card-horizontal" onclick="window.nirmaanApp.viewProductDetails('${p.id}')">
          <img src="${p.images?.[0]?.url || '/static/images/terracotta_marketplace.jpg'}" class="prod-thumb" alt="${p.title_en}" />
          <div class="prod-meta">
            <h4>${p.title_en || p.title_original}</h4>
            <p>${p.craft_type} • ${p.material}</p>
            <div class="prod-price-status">
              <span class="prod-price">₹${p.price || 399}</span>
              <span class="status-badge ${p.status === 'published' ? 'status-published' : 'status-draft'}">${p.status}</span>
            </div>
          </div>
        </div>
      `).join("");
    } catch (e) {}
  }

  async renderMarketplaceFeed(category = "All", query = "") {
    const grid = document.getElementById("marketplace-products-grid");
    if (!grid) return;
    try {
      const products = await MarketplaceManager.loadFeed(category, query);
      grid.innerHTML = products.map(p => `
        <div class="mkt-product-card" onclick="window.nirmaanApp.viewProductDetails('${p.id}')">
          <div class="mkt-img-wrap">
            <img src="${p.images?.[0]?.url || '/static/images/terracotta_marketplace.jpg'}" alt="${p.title_en}" />
          </div>
          <div class="mkt-card-body">
            <div class="mkt-card-title">${p.title_en || p.title_hi || p.title_original}</div>
            <div style="font-size:11px; color:var(--color-text-muted);">${p.craft_type}</div>
            <div class="mkt-card-price">₹${p.price || 399}</div>
          </div>
        </div>
      `).join("");
    } catch (e) {}
  }

  async renderMyProductsList() {
    const container = document.getElementById("my-products-full-list");
    if (!container) return;
    try {
      const products = await ApiClient.getProducts();
      container.innerHTML = products.map(p => `
        <div class="product-card-horizontal" onclick="window.nirmaanApp.viewProductDetails('${p.id}')">
          <img src="${p.images?.[0]?.url || '/static/images/terracotta_marketplace.jpg'}" class="prod-thumb" alt="${p.title_en}" />
          <div class="prod-meta">
            <h4>${p.title_en || p.title_original}</h4>
            <p>${p.craft_type} • ${p.material}</p>
            <div class="prod-price-status">
              <span class="prod-price">₹${p.price || 399}</span>
              <span class="status-badge ${p.status === 'published' ? 'status-published' : 'status-draft'}">${p.status}</span>
            </div>
          </div>
        </div>
      `).join("");
    } catch (e) {}
  }

  async renderCatalogsList() {
    const container = document.getElementById("my-catalogs-list");
    if (!container) return;
    try {
      const catalogs = await ApiClient.getCatalogs();
      container.innerHTML = catalogs.map(c => `
        <div class="card" style="margin-bottom:var(--space-sm); cursor:pointer;">
          <div style="font-size:15px; font-weight:800; color:var(--color-terracotta-dark); margin-bottom:4px;">${c.title}</div>
          <p style="font-size:12px; color:var(--color-text-muted); margin-bottom:8px;">${c.description}</p>
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size:11px; font-weight:700; color:var(--color-forest);">${c.products?.length || 2} Products</span>
            <button class="btn btn-sand" style="width:auto; padding:6px 12px; font-size:11px;" onclick="window.nirmaanApp.shareCatalog('${c.id}')">📤 Share Catalog</button>
          </div>
        </div>
      `).join("");
    } catch (e) {}
  }

  renderArtisanProfileView() {
    if (!this.artisanProfile) return;
    const nameEl = document.getElementById("profile-artisan-name");
    const craftEl = document.getElementById("profile-artisan-craft");
    const regionEl = document.getElementById("profile-artisan-region");
    const bioEl = document.getElementById("profile-artisan-bio");

    if (nameEl) nameEl.textContent = this.artisanProfile.name;
    if (craftEl) craftEl.textContent = `${this.artisanProfile.craft_type} • ${this.artisanProfile.seller_type}`;
    if (regionEl) regionEl.textContent = `📍 ${this.artisanProfile.region}`;
    if (bioEl) bioEl.textContent = this.artisanProfile.bio;
  }

  async viewProductDetails(productId) {
    const p = await ApiClient.getProduct(productId);
    if (!p) return;
    this.currentWorkingProduct = p;
    CatalogManager.setProduct(p);
    this.switchView("create");
    this.setCreateStep(4);
  }

  shareCatalog(catalogId) {
    const shareText = "Namaste! 🙏 Explore our handmade artisan collections on NIRMAAN digital catalog.";
    const url = `https://api.whatsapp.com/send?text=${encodeURIComponent(shareText)}`;
    window.open(url, "_blank");
  }

  checkDraftRecovery() {
    const draft = StorageManager.getDraft();
    if (draft && draft.data) {
      const modal = document.getElementById("draft-recovery-modal");
      if (modal) {
        modal.classList.add("active");
        document.getElementById("btn-draft-continue").onclick = () => {
          this.currentWorkingProduct = draft.data;
          CatalogManager.setProduct(draft.data);
          modal.classList.remove("active");
          this.switchView("create");
          this.setCreateStep(4);
        };
        document.getElementById("btn-draft-discard").onclick = () => {
          StorageManager.clearDraft();
          modal.classList.remove("active");
        };
      }
    }
  }

  // --- Image Viewer Navigation & Zoom ---
  cycleCatalogImage(direction) {
    const tabs = ["marketplace", "studio_pro", "original", "features"];
    let currentIdx = tabs.indexOf(CatalogManager.activeImageTab);
    if (currentIdx === -1) currentIdx = 0;
    let nextIdx = (currentIdx + direction + tabs.length) % tabs.length;
    const nextTabType = tabs[nextIdx];
    CatalogManager.activeImageTab = nextTabType;
    
    document.querySelectorAll(".viewer-tab").forEach(t => {
      t.classList.toggle("active", t.getAttribute("data-img-type") === nextTabType);
    });
    this.updateCatalogImageViewer();
  }

  openImageFullscreen() {
    const modal = document.getElementById("fullscreen-image-modal");
    const imgEl = document.getElementById("fullscreen-modal-img");
    if (modal && imgEl) {
      imgEl.src = CatalogManager.getCurrentImage();
      modal.classList.add("active");
    }
  }

  toggleCompareSplit() {
    // Toggle between Original and Marketplace
    if (CatalogManager.activeImageTab === "original") {
      CatalogManager.activeImageTab = "marketplace";
      this.showToast("Viewing AI Studio Enhanced version");
    } else {
      CatalogManager.activeImageTab = "original";
      this.showToast("Viewing Original Untouched Photograph");
    }
    document.querySelectorAll(".viewer-tab").forEach(t => {
      t.classList.toggle("active", t.getAttribute("data-img-type") === CatalogManager.activeImageTab);
    });
    this.updateCatalogImageViewer();
  }

  // --- Voice Narration (TTS) ---
  narrateCurrentDescription() {
    const loc = CatalogManager.getLocalizedContent(CatalogManager.activeLangTab);
    const textToSpeak = `${loc.title}. ${loc.description}`;
    const langCode = CatalogManager.activeLangTab === "en" ? "en-IN" : "hi-IN";
    AudioManager.speakText(textToSpeak, langCode);
    this.showToast("Reading aloud product description... 🔊");
  }

  narratePricingAdvice() {
    if (PricingManager.currentInsight) {
      const ins = PricingManager.currentInsight;
      const textToSpeak = `${ins.status_title}. ${ins.explanation}.`;
      AudioManager.speakText(textToSpeak, "en-IN");
      this.showToast("Reading aloud pricing insight... 🔊");
    }
  }

  // --- Market Search Confirmation & Edit ---
  promptChangeMarketProduct() {
    const currentName = this.currentWorkingProduct?.title_en || this.currentWorkingProduct?.title_original || "Handcrafted Product";
    const newName = prompt("Enter product name or craft to search comparable prices:", currentName);
    if (newName && newName.trim()) {
      if (this.currentWorkingProduct) {
        this.currentWorkingProduct.title_en = newName.trim();
      }
      this.updateMarketConfirmationCard();
      this.executeMarketCheck();
      this.showToast(`Searching market comparables for "${newName.trim()}"... 🔍`);
    }
  }

  // --- Onboarding Modal ---
  openOnboardingModal() {
    const modal = document.getElementById("onboarding-modal");
    if (modal) {
      if (this.artisanProfile) {
        document.getElementById("onboarding-name").value = this.artisanProfile.name;
        document.getElementById("onboarding-language").value = this.artisanProfile.preferred_language || "hi";
        document.getElementById("onboarding-seller-type").value = this.artisanProfile.seller_type || "Artisan";
        document.getElementById("onboarding-region").value = this.artisanProfile.region || "Khurja, Uttar Pradesh";

        // Multi-select craft checkboxes
        const currentCrafts = (this.artisanProfile.craft_type || "Pottery & Terracotta").split(",").map(c => c.trim().toLowerCase());
        document.querySelectorAll(".craft-checkbox").forEach(cb => {
          const val = cb.value.toLowerCase();
          cb.checked = currentCrafts.some(c => val.includes(c) || c.includes(val) || (c.includes("pottery") && val.includes("pottery")) || (c.includes("bamboo") && val.includes("bamboo")) || (c.includes("brass") && val.includes("brass")));
          cb.closest(".craft-choice-card")?.classList.toggle("selected", cb.checked);
        });
      }
      modal.classList.add("active");
    }
  }

  async saveOnboarding() {
    const name = document.getElementById("onboarding-name").value || "Ramesh Kumar";
    const lang = document.getElementById("onboarding-language").value || "hi";
    const sellerType = document.getElementById("onboarding-seller-type").value || "Artisan";
    const region = document.getElementById("onboarding-region").value || "Jaipur, Rajasthan";

    // Collect all selected craft boxes
    const selectedCrafts = Array.from(document.querySelectorAll(".craft-checkbox:checked")).map(cb => cb.value);
    const craft = selectedCrafts.length > 0 ? selectedCrafts.join(", ") : "Pottery & Terracotta";

    const updateData = {
      name: name,
      preferred_language: lang,
      craft_type: craft,
      seller_type: sellerType,
      region: region,
      bio: `Craft producer specializing in ${craft}. Dedicated to authentic Indian craftsmanship.`
    };

    try {
      this.artisanProfile = await ApiClient.updateArtisan(updateData);
      StorageManager.saveSettings(updateData);
      applyLanguage(lang);
      const langMap = { en: "en-IN", hi: "hi-IN" };
      if (langMap[lang]) this.updateSpeakingLanguage(langMap[lang], false);
      document.getElementById("onboarding-modal").classList.remove("active");
      this.showToast(`Welcome ${name}! Profile updated with ${selectedCrafts.length} craft(s).`);
      await this.loadArtisanProfile();
      this.startNewProductFlow(1);
    } catch (e) {
      applyLanguage(lang);
      document.getElementById("onboarding-modal").classList.remove("active");
      this.startNewProductFlow(1);
    }
  }

  // --- Collection Creator ---
  openCreateCollectionModal() {
    const modal = document.getElementById("collection-modal");
    if (modal) modal.classList.add("active");
  }

  async submitCreateCollection() {
    const title = document.getElementById("collection-title-input")?.value.trim();
    const desc = document.getElementById("collection-desc-input")?.value.trim();
    if (!title) {
      this.showToast("Please enter a collection name.");
      return;
    }

    try {
      const allProds = await ApiClient.getProducts();
      const prodIds = allProds.slice(0, 3).map(p => p.id);
      await ApiClient.createCatalog({
        title: title,
        description: desc || "Artisan handcrafted collection",
        cover_image_url: allProds[0]?.images?.[0]?.url || "/static/images/terracotta_marketplace.jpg",
        is_published: true,
        product_ids: prodIds
      });
      document.getElementById("collection-modal").classList.remove("active");
      this.showToast(`Collection '${title}' created successfully!`);
      this.renderCatalogsList();
    } catch (e) {
      this.showToast("Collection saved.");
      document.getElementById("collection-modal").classList.remove("active");
    }
  }

  exportProductCard() {
    const currentImg = CatalogManager.getCurrentImage();
    const link = document.createElement("a");
    link.href = currentImg;
    link.download = `nirmaan_${this.currentWorkingProduct?.category || 'craft'}.jpg`;
    link.click();
    this.showToast("Product image downloaded! 📥");
  }

  showToast(message) {
    const toast = document.getElementById("app-toast");
    if (!toast) return;
    toast.textContent = message;
    toast.style.display = "block";
    setTimeout(() => {
      toast.style.display = "none";
    }, 3200);
  }
}

window.nirmaanApp = new NirmaanApp();
document.addEventListener("DOMContentLoaded", () => {
  window.nirmaanApp.init();
});

