"""
NIRMAAN - Audio Transcription Service
Genuinely transcribes the artisan's recorded voice note using Gemini's
native audio understanding (no browser Web Speech API dependency, and no
canned/hardcoded fallback transcript). This is what makes every product's
description come from what the artisan ACTUALLY said, instead of falling
back to a fixed sample (e.g. a "brass diya" / "terracotta bowl" example).

If Gemini isn't configured or the call fails, `transcribe()` returns None
and the caller must surface a real "please try again" state to the user —
it must NOT be papered over with fabricated product text.
"""
import os
import re
import json
from typing import Optional, Dict, Any

from ..config import GEMINI_API_KEY, GEMINI_TEXT_MODEL
from .speech_service import LANGUAGES, speech_service

PROMPT = """You are transcribing a short voice note recorded by an Indian artisan
describing ONE handmade product they are about to list for sale.

Listen to the attached audio carefully and:
1. Transcribe EXACTLY what the artisan said, verbatim, in the original
   language/script they spoke in (do not translate, do not summarize,
   do not invent words that are not in the recording).
2. Identify the spoken language.

Return STRICT JSON only, with exactly these keys and nothing else, no
markdown code fences, no commentary:
{"transcript": "...", "language_name": "...", "language_code": "..."}

language_code must be one of: hi, en, mr, bn, gu, ta, te, kn, pa, ml, awa, bho.
If the audio is silent, unintelligible, or contains no speech, set
"transcript" to an empty string "" instead of guessing or fabricating content.
"""


class AudioTranscriptionService:
    def __init__(self):
        self._client = None
        self.last_error = None

    def _get_api_key(self) -> str:
        return (os.getenv("GEMINI_API_KEY", "").strip() or
                os.getenv("GOOGLE_API_KEY", "").strip() or
                GEMINI_API_KEY).strip()

    def is_available(self) -> bool:
        key = self._get_api_key()
        return bool(key and len(key) > 5)

    def _get_client(self):
        if not self.is_available():
            return None
        if self._client is None:
            try:
                from google import genai
                self._client = genai.Client(api_key=self._get_api_key())
            except Exception as e:
                print(f"[AudioTranscriptionService] Could not initialize Google GenAI client: {e}")
                return None
        return self._client

    @staticmethod
    def _strip_code_fence(text: str) -> str:
        text = text.strip()
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
        return text.strip()

    @staticmethod
    def _transcode_to_wav(audio_bytes: bytes) -> bytes:
        """
        Browsers record voice notes as audio/webm (Chrome/Edge) or
        audio/mp4 (Safari) via MediaRecorder — neither is in Gemini's
        officially supported audio MIME list (wav/mp3/aiff/aac/ogg/flac).
        This decodes whatever the browser sent and re-encodes it as a
        plain 16kHz mono WAV, which Gemini reliably accepts, using
        PyAV's bundled FFmpeg (no system ffmpeg install required).
        """
        import av
        import io

        input_container = av.open(io.BytesIO(audio_bytes))
        try:
            in_stream = input_container.streams.audio[0]
        except (IndexError, AttributeError):
            input_container.close()
            raise ValueError("No audio stream found in recording")

        output_buffer = io.BytesIO()
        output_container = av.open(output_buffer, mode="w", format="wav")
        out_stream = output_container.add_stream("pcm_s16le", rate=16000)
        out_stream.layout = "mono"

        resampler = av.AudioResampler(format="s16", layout="mono", rate=16000)

        for frame in input_container.decode(in_stream):
            frame.pts = None
            for rframe in resampler.resample(frame):
                for packet in out_stream.encode(rframe):
                    output_container.mux(packet)

        for packet in out_stream.encode(None):
            output_container.mux(packet)

        output_container.close()
        input_container.close()
        return output_buffer.getvalue()

    def transcribe(self, audio_bytes: bytes, mime_type: str = "audio/webm") -> Optional[Dict[str, Any]]:
        """
        Sends the raw recorded audio to Gemini and returns the genuine
        transcript + detected language, or None if unavailable/failed.
        Sets self.last_error with a human-readable reason on failure, so
        the API layer can surface *why* instead of a bare 503.
        """
        self.last_error = None
        client = self._get_client()
        if not client:
            self.last_error = "Gemini API key is not configured on the server (.env GEMINI_API_KEY missing/invalid)."
            return None
        if not audio_bytes:
            self.last_error = "No audio data was received from the browser."
            return None

        # Gemini's generateContent only officially accepts wav/mp3/aiff/
        # aac/ogg/flac — but browsers record webm (Chrome/Edge) or mp4
        # (Safari). Always transcode to WAV server-side so this works
        # regardless of what the browser's MediaRecorder produced.
        wav_bytes = None
        try:
            wav_bytes = self._transcode_to_wav(audio_bytes)
        except Exception as e:
            print(f"[AudioTranscriptionService] Transcoding to WAV failed, sending original bytes: {type(e).__name__}: {e}")

        send_bytes = wav_bytes if wav_bytes else audio_bytes
        send_mime = "audio/wav" if wav_bytes else mime_type

        try:
            from google.genai import types

            model = os.getenv("GEMINI_TEXT_MODEL", GEMINI_TEXT_MODEL or "gemini-3.6-flash").strip()
            response = client.models.generate_content(
                model=model,
                contents=[
                    types.Part.from_bytes(data=send_bytes, mime_type=send_mime),
                    PROMPT,
                ],
                config=types.GenerateContentConfig(response_mime_type="application/json"),
            )
            raw_text = getattr(response, "text", None)
            if not raw_text:
                self.last_error = "Gemini returned an empty response for this recording."
                print("[AudioTranscriptionService] Empty response text from Gemini")
                return None

            cleaned = self._strip_code_fence(raw_text)
            data = json.loads(cleaned)

            transcript = (data.get("transcript") or "").strip()
            if not transcript:
                return {"transcript_original": "", "detected_language": "en", "language_name": LANGUAGES["en"]}

            lang_code = (data.get("language_code") or "").strip().lower()
            if lang_code not in LANGUAGES:
                # Fall back to script-based detection of the real transcript
                # (still driven by genuine text, never a canned example).
                lang_code, _ = speech_service.detect_language(transcript)

            language_name = LANGUAGES.get(lang_code, data.get("language_name") or LANGUAGES["en"])

            return {
                "transcript_original": transcript,
                "detected_language": lang_code,
                "language_name": language_name,
            }

        except json.JSONDecodeError as e:
            self.last_error = f"Could not parse Gemini's response as JSON: {e}"
            print(f"[AudioTranscriptionService] Could not parse JSON from Gemini response: {e}")
            return None
        except Exception as e:
            self.last_error = f"{type(e).__name__}: {e}"
            print(f"[AudioTranscriptionService] Transcription failed: {type(e).__name__}: {e}")
            return None


audio_transcription_service = AudioTranscriptionService()
