/**
 * NIRMAAN - Local Storage & Draft Autosave Manager
 * Automatically saves unfinished product creation state and offers draft recovery.
 */
const STORAGE_KEY_DRAFT = "nirmaan_current_draft";
const STORAGE_KEY_SETTINGS = "nirmaan_user_settings";

export const StorageManager = {
  saveDraft(draftData) {
    try {
      localStorage.setItem(STORAGE_KEY_DRAFT, JSON.stringify({
        data: draftData,
        timestamp: new Date().toISOString()
      }));
    } catch (e) {
      console.warn("Could not autosave draft:", e);
    }
  },

  getDraft() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY_DRAFT);
      if (!raw) return null;
      return JSON.parse(raw);
    } catch (e) {
      return null;
    }
  },

  clearDraft() {
    try {
      localStorage.removeItem(STORAGE_KEY_DRAFT);
    } catch (e) {}
  },

  saveSettings(settings) {
    try {
      localStorage.setItem(STORAGE_KEY_SETTINGS, JSON.stringify(settings));
    } catch (e) {}
  },

  getSettings() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY_SETTINGS);
      if (!raw) return { preferredLanguage: "hi", role: "Artisan" };
      return JSON.parse(raw);
    } catch (e) {
      return { preferredLanguage: "hi", role: "Artisan" };
    }
  }
};
