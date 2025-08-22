#!/usr/bin/env python3
import argparse, os, zipfile, sys, csv

LETTERS = ["ا","ب","ت","ث","ج","ح","خ","د","ذ","ر","ز","س","ش","ص","ض","ط","ظ","ع","غ","ف","ق","ك","ل","م","ن","ه","و","ي"]

TRANSLIT = [
    ("ا","alif"),("ب","baa"),("ت","taa"),("ث","thaa"),("ج","jeem"),("ح","haa"),
    ("خ","khaa"),("د","dal"),("ذ","dhal"),("ر","raa"),("ز","zaay"),("س","seen"),
    ("ش","sheen"),("ص","saad"),("ض","daad"),("ط","taa_emph"),("ظ","dhaa_emph"),
    ("ع","ain"),("غ","ghain"),("ف","faa"),("ق","qaaf"),("ك","kaaf"),("ل","laam"),
    ("م","meem"),("ن","noon"),("ه","haa2"),("و","waaw"),("ي","yaa")
]

def ensure_outdir(path):
    os.makedirs(path, exist_ok=True)

def save_index(outdir):
    idx = os.path.join(outdir, "letters_index.csv")
    with open(idx, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["letter","transliteration","filename_ar","filename_ascii"])
        for (ch, tr) in TRANSLIT:
            w.writerow([ch, tr, f"{ch}.wav", f"{TRANSLIT.index((ch,tr))+1:02d}_{tr}.wav"])
    return idx

def synthesize_gtts(text, path):
    from gtts import gTTS
    from pydub import AudioSegment
    mp3_tmp = path.replace(".wav",".mp3")
    tts = gTTS(text=text, lang="ar")
    tts.save(mp3_tmp)
    AudioSegment.from_mp3(mp3_tmp).export(path, format="wav")
    os.remove(mp3_tmp)

async def synthesize_edge_async(text, path, voice):
    import edge_tts, asyncio
    communicate = edge_tts.Communicate(text, voice=voice, rate="-10%")
    await communicate.save(path)

def synthesize_edge(text, path, voice):
    import asyncio
    asyncio.run(synthesize_edge_async(text, path, voice))

def main():
    p = argparse.ArgumentParser(description="Generate Arabic letters as WAV files and ZIP them.")
    p.add_argument("--backend", choices=["gtts","edge"], default="gtts", help="TTS backend")
    p.add_argument("--voice", default="ar-SA-HamedNeural", help="Edge voice (male ar-SA-HamedNeural, female ar-EG-SalmaNeural, etc.)")
    p.add_argument("--outdir", default="output_wav", help="Output directory for WAV files")
    p.add_argument("--zip", dest="zipname", default=None, help="Optional zip filename to create")
    p.add_argument("--ascii-names", action="store_true", help="Also write ASCII-named copies (01_alif.wav, etc.)")
    args = p.parse_args()

    ensure_outdir(args.outdir)
    index_csv = save_index(args.outdir)

    for ch, tr in TRANSLIT:
        wav_path = os.path.join(args.outdir, f"{ch}.wav")
        if args.backend == "gtts":
            try:
                synthesize_gtts(ch, wav_path)
            except Exception as e:
                print(f"[gTTS] Failed for {ch}: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            try:
                synthesize_edge(ch, wav_path, args.voice)
            except Exception as e:
                print(f"[edge-tts] Failed for {ch}: {e}", file=sys.stderr)
                sys.exit(1)

        if args.ascii_names:
            ascii_name = f"{TRANSLIT.index((ch,tr))+1:02d}_{tr}.wav"
            ascii_path = os.path.join(args.outdir, ascii_name)
            try:
                import shutil
                shutil.copyfile(wav_path, ascii_path)
            except Exception as e:
                print(f"[ascii copy] Failed for {ch}: {e}", file=sys.stderr)

    if args.zipname:
        with zipfile.ZipFile(args.zipname, "w") as z:
            for fn in os.listdir(args.outdir):
                z.write(os.path.join(args.outdir, fn), fn)
        print(f"ZIP created: {args.zipname}")

    print("Done. Files in:", args.outdir)
    print("Index file:", index_csv)

if __name__ == "__main__":
    main()
