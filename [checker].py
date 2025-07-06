'''
___________________________________________________________________________________________________________
это файл проверки всё ли скачалось
-----------------------------------------------------------------------------------------------------------
проверяет все ли файлы из 2.0 есть в скачанных, те которых нет записывает в missing.txt лишние в extra.txt
‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
'''
import os
import re

# Функция очистки имени файла от запрещённых символов Windows
def sanitize_filename(name):
    # Удаляем символы: \ / : * ? " < > |
    return re.sub(r'[\\/:"*?<>|]+', '', name).strip()

# Определяем директорию, где находится этот скрипт
script_dir = os.path.dirname(os.path.abspath(__file__))

# Пути к файлу плейлиста и папке песен — относительно скрипта
playlist_path = os.path.join(script_dir, "2.0.txt")
songs_folder = os.path.join(script_dir, "songs")

output_folder = script_dir  # Можно менять, если нужно

# Чтение списка песен из файла
with open(playlist_path, "r", encoding="utf-8") as file:
    lines = file.readlines()[1:]  # Пропустить заголовок

expected_files = {}
for line in lines:
    parts = [p.strip() for p in line.strip().split("|")]
    if len(parts) < 4:
        continue
    song, artist, album, link = parts
    filename = f"{sanitize_filename(song)} - {sanitize_filename(artist)}.mp3"
    expected_files[filename] = line.strip()

# Файлы в папке
actual_files = {
    f for f in os.listdir(songs_folder)
    if f.lower().endswith(".mp3")
}

expected_set = set(expected_files.keys())

# Песни, которые отсутствуют
missing = expected_set - actual_files
# Песни, которые лишние
extra = actual_files - expected_set

# Запись отсутствующих песен
missing_path = os.path.join(output_folder, "missing.txt")
with open(missing_path, "w", encoding="utf-8") as f:
    f.write("Song|Artist|Album|Link\n")
    for filename in missing:
        f.write(expected_files[filename] + "\n")

# Запись лишних песен
extra_path = os.path.join(output_folder, "extra.txt")
with open(extra_path, "w", encoding="utf-8") as f:
    for filename in extra:
        f.write(filename + "\n")

print(f"Создан файл отсутствующих: {missing_path}")
print(f"Создан файл лишних: {extra_path}")

# Считаем количество треков в плейлисте (пропускаем заголовок)
with open(playlist_path, "r", encoding="utf-8") as f:
    playlist_lines = [line.strip() for line in f.readlines() if line.strip()]
    playlist_count = len(playlist_lines) - 1  # минус строка "Song|Artist|Album|Link"

# Считаем количество mp3-файлов в папке
songs_count = len([
    f for f in os.listdir(songs_folder)
    if f.lower().endswith(".mp3")
])

# Вывод
print(f"🎵 В плейлисте: {playlist_count} треков")
print(f"📁 В папке: {songs_count} файлов")
if playlist_count == songs_count:
    print("✅ Количество совпадает.")
else:
    print("⚠️ Количество НЕ совпадает.")
