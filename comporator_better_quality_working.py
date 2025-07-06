'''
___________________________________________________________________________________________________________
Run this file second
-----------------------------------------------------------------------------------------------------------
Downloads all files starting from number start_line, adding covers and metadata.
File names are in the format:
song - author.mp3
Metadata and links are taken from 2.0.txt, and covers come from the YouTube Music API.
Files causing errors are visible by line number, files that YouTube marks as age-restricted
are recorded in the file age_restricted_file.
‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
'''
import os
import re
import subprocess
import requests
import time
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB
from ytmusicapi import YTMusic

# Path to yt-dlp
YTDLP_PATH = r"C:\Users\Me\example\yt-dlp.exe"

# Starting line number for reading and numbering songs (starts from 1)
start_line = 2
# Paths to files and folders
songs_txt = os.path.join(base_dir, "missing.txt")
songs_folder = os.path.join(base_dir, "songs")
age_restricted_file = os.path.join(base_dir, "age_restricted.txt")

ytmusic = YTMusic()

def safe_filename(s):
    return "".join(c for c in s if c not in r'\/:*?"<>|').strip()

def get_cover_url(title, artist):
    query = f"{title} {artist}"
    results = ytmusic.search(query, filter="songs")
    if not results:
        return None
    thumb_url = results[0].get('thumbnails', [{}])[-1].get('url', '')
    if not thumb_url:
        return None
    return re.sub(r'w\d+-h\d+', 'w400-h400', thumb_url)

# Read the song list starting from start_line (considering zero-based indexing)
with open(songs_txt, encoding="utf-8") as f:
    lines = f.readlines()[start_line - 1:]

songs = []
for line in lines:
    parts = [p.strip() for p in line.strip().split("|")]
    if len(parts) < 4:
        continue
    songs.append({
        "title": parts[0],
        "artist": parts[1],
        "album": parts[2],
        "url": parts[3],
    })

age_file = open(age_restricted_file, "a", encoding="utf-8")

i = 0
while i < len(songs):
    song = songs[i]
    line_num = i + start_line  # calculate current line number in original file

    print(f"📥 Downloading: {song['title']} — {song['artist']} (line {line_num})")

    filename_base = f"{song['title']} - {song['artist']}"
    safe_filename_base = safe_filename(filename_base)
    output_template = os.path.join(songs_folder, safe_filename_base + ".%(ext)s")

    try:
        result = subprocess.run([
            YTDLP_PATH,
            "-x", "--audio-format", "mp3",
            "--no-playlist", "--quiet", "--no-warnings",
            "-o", output_template,
            song["url"]
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)

    except subprocess.CalledProcessError as e:
        err_text = e.stderr or ""
        if "Sign in to confirm your age" in err_text or "Use --cookies" in err_text:
            print(f"❌ Age restriction on line {line_num}: {song['title']} — {song['artist']}")
            age_file.write(f"{line_num}: {song['title']} — {song['artist']}\n")
            age_file.flush()
            i += 1
            continue
        else:
            print(f"❌ Error downloading line {line_num}: {song['title']} — {song['artist']}")
            print("⏳ Waiting 10 minutes before retry...")
            time.sleep(600)
            continue

    mp3_path = os.path.join(songs_folder, safe_filename_base + ".mp3")

    cover_url = get_cover_url(song['title'], song['artist'])
    if not cover_url:
        print(f"  ❌ Cover not found for {song['title']} — {song['artist']}")
        i += 1
        continue

    try:
        response = requests.get(cover_url)
        response.raise_for_status()
        cover_data = response.content
    except Exception as e:
        print(f"  ❌ Error downloading cover: {e}")
        i += 1
        continue

    audio = MP3(mp3_path, ID3=ID3)
    try:
        audio.add_tags()
    except Exception:
        pass

    audio.tags.add(APIC(encoding=3, mime='image/jpeg', type=3, desc='Cover', data=cover_data))
    audio.tags.add(TIT2(encoding=3, text=song['title']))
    audio.tags.add(TPE1(encoding=3, text=song['artist']))
    audio.tags.add(TALB(encoding=3, text=song['album']))
    audio.save()

    i += 1

age_file.close()
print("✅ Done!")
