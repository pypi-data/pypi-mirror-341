# My WhatsApp Package

A Python library to interact with your personal WhatsApp account using the [whatsapp-mcp](https://github.com/lharries/whatsapp-mcp) Go bridge.

**Disclaimer:** This package relies on unofficial methods (via `whatsmeow` used by the Go bridge) to connect to WhatsApp. WhatsApp's terms of service might prohibit this, and using it could potentially lead to your account being flagged or banned. Use at your own risk. This is primarily for educational or personal use.

## Features

- Handles setup (Go/Git check, repository cloning).
- Manages the background Go bridge process.
- Prompts for QR code scanning on first connect.
- Send text messages.
- Send media files (images, videos, audio, documents).
- Retrieve new incoming messages (including media download).

## Prerequisites

- **Python:** 3.8+
- **Go:** Latest version recommended (install from [go.dev](https://go.dev/dl/)). Must be added to your system's PATH.
- **Git:** Required for cloning the `whatsapp-mcp` repository (install from [git-scm.com](https://git-scm.com/downloads)). Must be added to your system's PATH.
- **C Compiler (Windows):** If using Windows, you need a C compiler like MSYS2/MinGW configured with `CGO_ENABLED=1` for the `go-sqlite3` dependency used by the bridge. Follow the [Windows Compatibility steps](https://github.com/lharries/whatsapp-mcp#windows-compatibility) from the original `whatsapp-mcp` README.
- **FFmpeg (Optional):** Required by the Go bridge if you want to send arbitrary audio files as playable _voice_ messages (it converts them to `.ogg` Opus). If not installed, you can only send `.ogg` Opus files as voice messages or other audio as plain file documents.

## Installation

```bash
pip install shubh_whatsapp # Or pip install . if installing from source
```
