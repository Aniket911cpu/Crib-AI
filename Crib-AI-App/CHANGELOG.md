# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-01-15
### Added
- **Stealth Overlay**: Electron window with `WDA_EXCLUDEFROMCAPTURE` to remain invisible to screen sharing tools (Zoom/Teams).
- **Audio Pipeline**: Python backend using `soundcard` (WASAPI Loopback) and `Deepgram` for real-time transcription.
- **Panic Mode**: Global hotkey (`Ctrl+Shift+X`) to instantly terminate the application.
- **Context Engine**: LLM prompt builder (`prompt.py`) injecting Resume and Job Description for context-aware answers.
- **Documentation**: Comprehensive setup guide and architecture blueprint.
