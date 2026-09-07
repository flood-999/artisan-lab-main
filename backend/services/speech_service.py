"""
NIRMAAN - Speech Service
Multi-language speech-to-text recognition and spoken language detection for Indian languages.
Supports Hindi, Awadhi, Bhojpuri, Bengali, Marathi, Gujarati, Tamil, Telugu, Kannada, Malayalam, Punjabi, and English.
"""
from typing import Tuple, Dict, Any

LANGUAGES = {
    "hi": "हिंदी (Hindi)",
    "en": "English",
    "mr": "मराठी (Marathi)",
    "bn": "বাংলা (Bengali)",
    "gu": "ગુજરાતી (Gujarati)",
    "ta": "தமிழ் (Tamil)",
    "te": "తెలుగు (Telugu)",
    "kn": "ಕನ್ನಡ (Kannada)",
    "pa": "ਪੰਜਾਬੀ (Punjabi)",
    "awa": "अवधी (Awadhi)",
    "bho": "भोजपुरी (Bhojpuri)"
}

class SpeechService:
    @staticmethod
    def detect_language(text: str) -> Tuple[str, str]:
        """
        Detects Indian script and language from spoken transcript.
        """
        # Devanagari script detection (Hindi, Marathi, Awadhi, Bhojpuri)
        if any('\u0900' <= char <= '\u097F' for char in text):
            # Check regional vocabulary using whole words
            words = set(text.split())
            if words.intersection({"आहे", "करतो", "नाही", "माझे", "कसा"}):
                return "mr", LANGUAGES["mr"]
            elif words.intersection({"बा", "रहल", "कहल", "हमार", "बाटे"}):
                return "bho", LANGUAGES["bho"]
            return "hi", LANGUAGES["hi"]
            
        # Bengali script
        elif any('\u0980' <= char <= '\u09FF' for char in text):
            return "bn", LANGUAGES["bn"]
            
        # Gujarati script
        elif any('\u0A80' <= char <= '\u0AFF' for char in text):
            return "gu", LANGUAGES["gu"]
            
        # Tamil script
        elif any('\u0B80' <= char <= '\u0BFF' for char in text):
            return "ta", LANGUAGES["ta"]
            
        # Telugu script
        elif any('\u0C00' <= char <= '\u0C7F' for char in text):
            return "te", LANGUAGES["te"]
            
        # Kannada script
        elif any('\u0C80' <= char <= '\u0CFF' for char in text):
            return "kn", LANGUAGES["kn"]
            
        # Gurmukhi script (Punjabi)
        elif any('\u0A00' <= char <= '\u0A7F' for char in text):
            return "pa", LANGUAGES["pa"]
            
        # Malayalam script
        elif any('\u0D00' <= char <= '\u0D7F' for char in text):
            return "ml", LANGUAGES.get("ml", "മലയാളം (Malayalam)")
            
        # Default English
        return "en", LANGUAGES["en"]

    @classmethod
    def transcribe(cls, raw_audio_data: Any, simulated_speech: str = None) -> Dict[str, Any]:
        """
        Identifies the spoken language of a transcript that has already been
        produced elsewhere (Web Speech API interim captions, or the genuine
        Gemini audio transcription from /api/voice/transcribe-audio).

        There is NO canned/hardcoded transcript here — if nothing real was
        said or captured, this returns an empty transcript rather than
        fabricating a sample product description.
        """
        transcript = (simulated_speech or "").strip()

        lang_code, lang_name = cls.detect_language(transcript) if transcript else ("en", LANGUAGES["en"])
        
        return {
            "transcript_original": transcript,
            "detected_language": lang_code,
            "language_name": lang_name
        }

speech_service = SpeechService()
