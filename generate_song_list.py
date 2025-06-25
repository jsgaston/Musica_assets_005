import os
import json
from mutagen import File

VALID_EXTENSIONS = [".m4a", ".mp3", ".wav", ".flac", ".ogg", ".aac"]

# Configura aquí tu usuario y repo de GitHub
GITHUB_USER = "jsgaston"
GITHUB_REPO = "Musica_assets_004"
GITHUB_BRANCH = "main"
RAW_BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{GITHUB_BRANCH}/"

def is_audio_file(filename):
    return any(filename.lower().endswith(ext) for ext in VALID_EXTENSIONS)

def extract_metadata(filepath):
    audio = File(filepath, easy=True)
    title = os.path.splitext(os.path.basename(filepath))[0]

    return {
        "title": audio.get("title", [title])[0] if audio else title,
        "artist": audio.get("artist", [None])[0] if audio else None,
        "album": audio.get("album", [None])[0] if audio else None,
        "duration": int(audio.info.length) if audio and hasattr(audio, "info") else None,
        "genre": audio.get("genre", [None])[0] if audio else None,
        "year": audio.get("date", [None])[0] if audio else None,  # fallback estándar
        "filename": filepath,
        "url": RAW_BASE_URL + filepath.replace(" ", "%20")
    }


def get_audio_files():
    return [extract_metadata(file) for file in os.listdir(".") if os.path.isfile(file) and is_audio_file(file)]

if __name__ == "__main__":
    song_data = get_audio_files()
    with open("song_list004.json", "w", encoding="utf-8") as f:
        json.dump(song_data, f, indent=2, ensure_ascii=False)
    print(f"✅ Generado song_list004.json con {len(song_data)} canciones.")
