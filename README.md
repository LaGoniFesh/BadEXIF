# 🖼️ EXIF Metadata Injector

A Python tool to inject payloads into image metadata for red team, recon, and CTF scenarios.

> ⚠️ **For educational and authorized use only**. Do not use this tool to embed payloads in images without full consent.

---

## 💡 Features

- Inject text into EXIF metadata of `.jpg`, `.png`, `.bmp`
- Encode payloads (Base64, ROT13)
- Stealth mode: adds noise/random fields
- View existing metadata
- Supports: JPEG (EXIF), PNG (tEXt), BMP (comment stub)

---

## 🛠️ Installation

```bash
pip install -r requirements.txt
