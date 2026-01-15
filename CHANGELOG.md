# Changelog

All notable changes to this project will be documented in this file.

## [0.3.0] - 2026-01-15
### Added
- **SaaS Authentication**: Integrated Firebase Auth. Users must login to access features.
- **Pricing Tiers**:
    - **Free**: Basic access.
    - **Pro**: Unlimited usage.
    - **Premium**: Includes Ghost Mode & Coding Vision.
- **Feedback System**: Built-in "Report Issue" form directly in the overlay.
- **User Management**: Backend verification of user tokens and plan status.

- **Audio Pipeline**: Python backend using `soundcard` (WASAPI Loopback) and `Deepgram` for real-time transcription.
- **Panic Mode**: Global hotkey (`Ctrl+Shift+X`) to instantly terminate the application.
- **Context Engine**: LLM prompt builder (`prompt.py`) injecting Resume and Job Description for context-aware answers.
- **Documentation**: Comprehensive setup guide and architecture blueprint.
