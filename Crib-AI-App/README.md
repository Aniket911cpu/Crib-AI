# 🦜 Crib AI

> **The Stealthy, Real-Time Interview Copilot.**
> *Ace your technical interviews with an invisible, context-aware AI assistant.*

![License](https://img.shields.io/badge/license-MIT-blue)
![Platform](https://img.shields.io/badge/platform-Windows-blue)
![Status](https://img.shields.io/badge/status-active-success)

**Crib AI** is a state-of-the-art desktop application designed to provide real-time assistance during video interviews (Zoom, Teams, Google Meet). It stays "always-on-top" but remains **completely invisible** to screen-sharing software, listening to the interviewer and providing concise, context-aware answers instantly.

---

## 🏗️ Architecture

Crib AI uses a hybrid architecture for maximum performance and stealth:

- **Frontend (Electron + React)**: Renders the transparent overlay. Uses OS-level window affinity (`WDA_EXCLUDEFROMCAPTURE`) to hide from screen capture.
- **Backend (Python FastAPI)**:
  - **Audio Engine**: Captures system audio (interviewer's voice) via `soundcard` (WASAPI Loopback).
  - **Transcription**: Streams audio to Deepgram Nova-2 for ultra-low latency (<300ms) text.
  - **Context Engine**: Injects your Resume and Job Description into the LLM prompt.
  - **Vision Engine**: Captures screen regions to solve LeetCode/Coding problems using OCR.

---

## 🌟 Key Features

### 👻 True Stealth Mode
The application window is configured to be **invisible to screen sharing**. You can share your entire screen on Zoom, and the participants will see everything *except* the Crib AI overlay.

### ⚡ Real-Time Transcription
Using Deepgram's streaming API, Crib AI transcribes the interviewer's speech instantly. No more asking "Can you repeat that?".

### 🧠 Context-Aware Answers
Crib AI doesn't just answer questions; it answers them *as you*.
- Upload your **Resume**.
- Upload the **Job Description**.
- The AI tailors every answer to highlight your specific experience relevant to the role.

### 👁️ Coding Context Vision (New!)
Stuck on a LeetCode problem? Crib AI captures the coding window, extracts the text via OCR, and provides the optimal solution and time complexity analysis.

### 🚨 Panic Mode & Ghost Mode
- **Panic Mode (`Ctrl+Shift+X`)**: Instantly kills the application process if you feel compromised.
- **Ghost Mode**: Toggles the UI to 30% opacity for minimal distraction.

---

## 🛠️ Prerequisites

Before running Crib AI, ensure you have the following installed:

1.  **Node.js** (v16+) - For the Frontend.
2.  **Python** (v3.10+) - For the Backend.
3.  **Tesseract OCR** - For the Vision features.
    - [Download for Windows](https://github.com/UB-Mannheim/tesseract/wiki)
    - Add it to your System PATH.

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/crib-ai.git
cd Crib-AI-App
```

### 2. Backend Setup
1.  Navigate to the backend directory:
    ```bash
    cd backend
    ```
2.  Create a virtual environment (recommended):
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Configure Environment Variables:
    - Rename `.env.example` to `.env`.
    - Add your API Keys:
      ```ini
      DEEPGRAM_API_KEY=your_key_here
      GROQ_API_KEY=your_key_here
      OPENAI_API_KEY=your_key_here
      ```
5.  **Firebase Setup (Required)**:
    - You must have a Firebase Project.
    - Set up **Authentication** (Email/Password provider).
    - Set up **Firestore Database**.
    - For the backend to verify tokens, ensure you have Google Application Credentials set up if running in a restricted environment (locally it usually works with default login or you may need to export `GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account.json"`).

### 3. Frontend Setup
1.  Navigate to the electron directory:
    ```bash
    cd ../electron
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  **Configure Firebase**:
    - Open `electron/firebase_config.js`.
    - Replace the placeholder `apiKey`, `authDomain`, etc. with your values from the Firebase Console.

---

## 🎮 Usage Guide

### Starting the App
1.  **Start the Backend**:
    From `backend/`:
    ```bash
    python -m app.audio_stream
    # Or run the main server if using the full API
    ```
2.  **Start the Frontend**:
    From `electron/`:
    ```bash
    npm start
    ```

### Hotkeys & Controls
| Action | Shortcut / Control | Description |
| :--- | :--- | :--- |
| **Panic Mode** | `Ctrl + Shift + X` | Instantly terminates the app. |
| **Ghost Mode** | UI Button ("👻") | Toggles 30% visual opacity. |
| **Click-Through** | Mouse Hover | UI becomes interactive on hover, click-through otherwise. |

---

## ⚠️ Troubleshooting

**"No Audio is being transcribed!"**
- Ensure your computer's audio output is set to the default device. Crib AI listens to the `default_speaker` via loopback.
- Check your Deepgram API Key quota.

**"The overlay is black/opaque!"**
- Ensure you are running Windows 10/11 with Aero/Composition enabled.
- Update your Graphics Drivers.

**"Interviewer saw the window!"**
- **CRITICAL**: Always test with a friend on Zoom before a real interview.
- `WDA_EXCLUDEFROMCAPTURE` generally works 99% of the time, but specific screen capture tools (like OBS "Display Capture") might bypass it. Zoom "Screen Share" typically respects it.

---

## ⚖️ Ethical Disclaimer
This tool is intended for educational purposes and to assist with anxiety during interviews. Using this tool to misrepresent your skills or cheat in assessments may violate the terms of service of interview platforms and potential employment contracts. **Use responsibly.**

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.
