/**
 * NIRMAAN - Audio & Speech Manager
 * Handles browser Web Speech recognition, microphone recording waveforms, and voice reading (TTS).
 */

export const AudioManager = {
  recognition: null,
  isRecording: false,
  synth: window.speechSynthesis || null,

  // --- Real microphone recording (MediaRecorder) ---
  // This captures the artisan's ACTUAL voice as an audio file so it can be
  // sent to the backend for genuine transcription (see api.js
  // transcribeAudioBlob / /api/voice/transcribe-audio). It intentionally
  // never invents or substitutes a canned recording.
  mediaRecorder: null,
  mediaStream: null,
  recordedChunks: [],
  isCapturingAudio: false,

  _pickSupportedMimeType() {
    const candidates = [
      "audio/webm;codecs=opus",
      "audio/webm",
      "audio/ogg;codecs=opus",
      "audio/ogg",
      "audio/mp4"
    ];
    for (const type of candidates) {
      if (window.MediaRecorder && MediaRecorder.isTypeSupported && MediaRecorder.isTypeSupported(type)) {
        return type;
      }
    }
    return ""; // let the browser pick a default
  },

  async startCapturingAudio() {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia || !window.MediaRecorder) {
      throw new Error("Microphone recording is not supported in this browser.");
    }
    this.mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mimeType = this._pickSupportedMimeType();
    this.mediaRecorder = mimeType
      ? new MediaRecorder(this.mediaStream, { mimeType })
      : new MediaRecorder(this.mediaStream);
    this.recordedChunks = [];

    this.mediaRecorder.ondataavailable = (event) => {
      if (event.data && event.data.size > 0) {
        this.recordedChunks.push(event.data);
      }
    };

    this.mediaRecorder.start();
    this.isCapturingAudio = true;
  },

  /** Resolves with the recorded audio Blob (real voice, not simulated). */
  stopCapturingAudio() {
    return new Promise((resolve, reject) => {
      if (!this.mediaRecorder || !this.isCapturingAudio) {
        reject(new Error("Not currently recording."));
        return;
      }
      this.mediaRecorder.onstop = () => {
        const mimeType = this.mediaRecorder.mimeType || "audio/webm";
        const blob = new Blob(this.recordedChunks, { type: mimeType });
        this.recordedChunks = [];
        this.isCapturingAudio = false;
        if (this.mediaStream) {
          this.mediaStream.getTracks().forEach(track => track.stop());
          this.mediaStream = null;
        }
        resolve(blob);
      };
      try {
        this.mediaRecorder.stop();
      } catch (e) {
        reject(e);
      }
    });
  },

  init() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      this.recognition = new SpeechRecognition();
      this.recognition.continuous = false;
      this.recognition.interimResults = true;
      this.recognition.lang = "hi-IN";
    }
  },

  startListening(onResult, onEnd, lang = "hi-IN") {
    if (!this.recognition) {
      this.init();
    }
    
    if (this.recognition) {
      this.recognition.lang = lang;
      this.isRecording = true;

      this.recognition.onresult = (event) => {
        let transcript = "";
        for (let i = event.resultIndex; i < event.results.length; ++i) {
          transcript += event.results[i][0].transcript;
        }
        if (onResult) onResult(transcript);
      };

      this.recognition.onerror = (event) => {
        console.warn("Speech recognition notice:", event.error);
        this.isRecording = false;
        if (onEnd) onEnd();
      };

      this.recognition.onend = () => {
        this.isRecording = false;
        if (onEnd) onEnd();
      };

      try {
        this.recognition.start();
      } catch (e) {
        console.warn("Speech start exception:", e);
      }
    } else {
      console.log("Web Speech not natively supported in this browser, using simulation fallback.");
    }
  },

  stopListening() {
    if (this.recognition && this.isRecording) {
      try {
        this.recognition.stop();
      } catch (e) {}
      this.isRecording = false;
    }
  },

  speakText(text, lang = "hi-IN") {
    if (!this.synth) return;
    try {
      this.synth.cancel(); // Stop prior speech
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = lang;
      utterance.rate = 0.95;
      this.synth.speak(utterance);
    } catch (e) {
      console.warn("TTS error:", e);
    }
  }
};
