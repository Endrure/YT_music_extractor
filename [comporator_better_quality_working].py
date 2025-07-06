'''
___________________________________________________________________________________________________________
этот файл запускать вторым
-----------------------------------------------------------------------------------------------------------
скачивает все файлы начиная с номера start_line, добавляя им обложки и метаданные, названия файлов формата
song - author.mp3, метаданные и ссылки берутся из 2.0.txt а картинки с API YT музыки
файлы выдающие ошибку видно в строке, файлы которые ютуб считает для взрослых в файле age_restricted_file
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

# Путь к yt-dlp
YTDLP_PATH = r"C:\Users\Me\example\yt-dlp.exe"

# Начальная строка для чтения и нумерации песен (начинается с 1)
start_line = 2
# Пути к файлам и папкам
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

# Читаем список песен начиная с start_line (учитываем, что индексация с 0)
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
    line_num = i + start_line  # вычисляем текущий номер строки в исходном файле

    print(f"📥 Скачиваем: {song['title']} — {song['artist']} (строка {line_num})")

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
            print(f"❌ Возрастное ограничение на строке {line_num}: {song['title']} — {song['artist']}")
            age_file.write(f"{line_num}: {song['title']} — {song['artist']}\n")
            age_file.flush()
            i += 1
            continue
        else:
            print(f"❌ Ошибка при скачивании строки {line_num}: {song['title']} — {song['artist']}")
            print("⏳ Ждём 10 минут перед повтором...")
            time.sleep(600)
            continue

    mp3_path = os.path.join(songs_folder, safe_filename_base + ".mp3")

    cover_url = get_cover_url(song['title'], song['artist'])
    if not cover_url:
        print(f"  ❌ Обложка не найдена для {song['title']} — {song['artist']}")
        i += 1
        continue

    try:
        response = requests.get(cover_url)
        response.raise_for_status()
        cover_data = response.content
    except Exception as e:
        print(f"  ❌ Ошибка скачивания обложки: {e}")
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
print("✅ Готово!")
