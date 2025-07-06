'''
___________________________________________________________________________________________________________
run this file for songs with incorrect titles, data, covers
-----------------------------------------------------------------------------------------------------------
fixes file metadata, all data about the file must be specified in songs_info for example:
songs_info = {
    "Invader Invader - Kyary Pamyu Pamyu.mp3": (
        "Invader Invader",
        "Kyary Pamyu Pamyu",
        "Family Party"
    ),
    "Invader Invader 2 - Kyary Pamyu Pamyu.mp3": (
        "Invader Invader 2,
        "Kyary Pamyu Pamyu",
        "Family Party"
    ), 
}
‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
'''
import os
import re
import requests
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, ID3NoHeaderError
from ytmusicapi import YTMusic

# Folder with mp3 files
songs_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "songs")

# File data: filename : (title, artist, album)
songs_info = {
    "Invader Invader - Kyary Pamyu Pamyu.mp3": (
        "Invader Invader",
        "Kyary Pamyu Pamyu",
        "Family Party"
    ),
}

ytmusic = YTMusic()

def get_cover_url(title, artist):
    query = f"{title} {artist}"
    results = ytmusic.search(query, filter="songs")
    if not results:
        return None
    thumb_url = results[0].get('thumbnails', [{}])[-1].get('url', '')
    if not thumb_url:
        return None
    return re.sub(r'w\d+-h\d+', 'w400-h400', thumb_url)

# For updating names in the source
def update_script_filename(old_name, new_name):
    script_path = os.path.abspath(__file__)
    with open(script_path, "r", encoding="utf-8") as f:
        code_lines = f.readlines()

    replaced = False
    for i, line in enumerate(code_lines):
        if f'"{old_name}"' in line:
            code_lines[i] = line.replace(f'"{old_name}"', f'"{new_name}"')
            replaced = True
            print(f"Updated line {i+1} in script: '{old_name}' -> '{new_name}'")
            break

    if replaced:
        with open(script_path, "w", encoding="utf-8") as f:
            f.writelines(code_lines)
    else:
        print(f"Did not find line with '{old_name}' in script to replace.")

# To safely and predictably rename the file to a simpler format
def make_new_filename(title, artist):
    # Remove unsuitable filesystem characters
    safe_title = re.sub(r'[\\/:"*?<>|]+', '', title).strip()
    safe_artist = re.sub(r'[\\/:"*?<>|]+', '', artist).strip()
    return f"{safe_title} - {safe_artist}.mp3"

# List of old filenames to then update the script
old_filenames = list(songs_info.keys())

for old_filename in old_filenames:
    title, artist, album = songs_info[old_filename]

    old_filepath = os.path.join(songs_folder, old_filename)
    if not os.path.isfile(old_filepath):
        print(f"File not found: {old_filepath}")
        continue

    print(f"Processing: {old_filename}")

    cover_url = get_cover_url(title, artist)
    if not cover_url:
        print(f"  Cover not found for {title} — {artist}")
        continue

    try:
        response = requests.get(cover_url)
        response.raise_for_status()
        cover_data = response.content
    except Exception as e:
        print(f"  Error downloading cover: {e}")
        continue

    try:
        id3 = ID3(old_filepath)
        id3.delete()
        id3.save()
    except ID3NoHeaderError:
        pass
    except Exception as e:
        print(f"  Error deleting tags: {e}")
        continue

    audio = MP3(old_filepath, ID3=ID3)
    try:
        audio.add_tags()
    except Exception:
        pass

    audio.tags.add(APIC(
        encoding=3,
        mime='image/jpeg',
        type=3,
        desc='Cover',
        data=cover_data
    ))
    audio.tags.add(TIT2(encoding=3, text=title))
    audio.tags.add(TPE1(encoding=3, text=artist))
    audio.tags.add(TALB(encoding=3, text=album))

    audio.save(v2_version=3)
    print(f"  Tags updated for {old_filename}")

    # Now rename the mp3 file itself
    new_filename = make_new_filename(title, artist)
    new_filepath = os.path.join(songs_folder, new_filename)
    if old_filename != new_filename:
        if os.path.exists(new_filepath):
            print(f"  New file {new_filename} already exists, skipping rename.")
        else:
            os.rename(old_filepath, new_filepath)
            print(f"  File renamed: '{old_filename}' -> '{new_filename}'")

            # Update songs_info dictionary — replace key
            songs_info[new_filename] = songs_info.pop(old_filename)

            # Update the script code — replace old name with new
            update_script_filename(old_filename, new_filename)

print("Done!")
