# Crib AI

**Crib AI** is a stealthy, real-time interview copilot application designed to assist users during technical interviews. It features a transparent "always-on-top" overlay, real-time audio transcription, and context-aware AI answers.

## 🚀 Features
- **Stealth Overlay**: Invisible to screen-sharing software (Zoom/Teams).
- **Real-Time Transcription**: Low-latency audio loopback and ASR via Deepgram.
- **Panic Mode**: Global hotkey (`Ctrl+Shift+X`) to instantly hide the app.
- **Coding Vision**: Experimental screen capture for coding problems.
- **Speedometer**: Visual pacing indicator.

## 🛠️ Installation
Please refer to [walkthrough.md](walkthrough.md) (or the internal documentation) for detailed setup instructions.

### Quick Start
1. **Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   # Set DEEPGRAM_API_KEY
   python app/audio_stream.py
   ```

2. **Frontend**:
   ```bash
   cd electron
   npm install
   npm start
   ```

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
