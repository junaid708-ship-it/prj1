# Arabic Letter Pronunciations (WAV, MSA Male)

This repo generates **28 WAV files** — one per Arabic letter (`ا.wav`, `ب.wav`, … `ي.wav`) — in **Modern Standard Arabic**.
By default it uses **gTTS** for pronunciation. You can optionally use **edge-tts** for a *male* MSA voice.

## Quick Start

```bash
# 1) Clone and enter the repo
git clone <your-fork-url>.git arabic-pronunciation
cd arabic-pronunciation

# 2) Create a virtualenv (optional but recommended)
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3) Install deps
pip install -r requirements.txt
# If you want Microsoft Edge male voice instead of gTTS:
pip install edge-tts

# 4) Generate WAVs (gTTS by default)
python generate_letters.py --backend gtts --outdir output_wav

# Or: use Microsoft Edge MSA male voice (requires internet)
python generate_letters.py --backend edge --voice "ar-SA-HamedNeural" --outdir output_wav

# 5) Zip them
python generate_letters.py --zip arabic_pronunciation_letters.zip --outdir output_wav
```

- Output files: `output_wav/ا.wav`, `output_wav/ب.wav`, … `output_wav/ي.wav`
- ZIP: `arabic_pronunciation_letters.zip`

> **Note on male voice**: gTTS doesn’t expose gender. For a **male** MSA voice, use the Edge backend with `--voice ar-SA-HamedNeural`.

## One‑Command GitHub Release (optional)

Use the provided script to create a GitHub Release attaching the ZIP.

```bash
# Prepare files
python generate_letters.py --backend edge --voice "ar-SA-HamedNeural" --outdir output_wav --zip arabic_pronunciation_letters.zip

# Then publish (requires GitHub CLI 'gh' and you to be logged in: gh auth login)
./tools/publish_release.sh v1.0.0 "Arabic letters (WAV, MSA male)"
```

On Windows PowerShell:
```powershell
python generate_letters.py --backend edge --voice "ar-SA-HamedNeural" --outdir output_wav --zip arabic_pronunciation_letters.zip
powershell -ExecutionPolicy Bypass -File tools/publish_release.ps1 -Tag v1.0.0 -Title "Arabic letters (WAV, MSA male)"
```

## Letters Included
ا ب ت ث ج ح خ د ذ ر ز س ش ص ض ط ظ ع غ ف ق ك ل م ن ه و ي

## Troubleshooting
- **Arabic filenames on Windows**: Filenames are UTF-8 and should work on modern Windows. If you prefer ASCII, use `--ascii-names` to generate `01_alif.wav`, `02_baa.wav`, … alongside Arabic names.
- **No audio or distorted**: Ensure `ffmpeg` is installed for conversions when using gTTS.
- **Edge backend errors**: Ensure you have internet access and the `edge-tts` package installed.

## License
MIT for the scripts. Audio you generate is yours to use.
