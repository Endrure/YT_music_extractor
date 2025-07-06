'''
___________________________________________________________________________________________________________
This is a file to check if everything has been downloaded
-----------------------------------------------------------------------------------------------------------
Checks if all files from 2.0.txt exist in the downloaded songs folder;
those missing are written to missing.txt, extra files are written to extra.txt
‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
'''
import os
import re

# Function to clean filename from Windows forbidden characters
def sanitize_filename(name):
    # Remove characters: \ / : * ? " < > |
    return re.sub(r'[\\/:"*?<>|]+', '', name).strip()

# Determine the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Paths to the playlist file and songs folder — relative to the script
playlist_path = os.path.join(script_dir, "2.0.txt")
songs_folder = os.path.join(script_dir, "songs")

output_folder = script_dir  # Can be changed if needed

# Read the list of songs from the file
with open(playlist_path, "r", encoding="utf-8") as file:
    lines = file.readlines()[1:]  # Skip the header line

expected_files = {}
for line in lines:
    parts = [p.strip() for p in line.strip().split("|")]
    if len(parts) < 4:
        continue
    song, artist, album, link = parts
    filename = f"{sanitize_filename(song)} - {sanitize_filename(artist)}.mp3"
    expected_files[filename] = line.strip()

# Files in the songs folder
actual_files = {
    f for f in os.listdir(songs_folder)
    if f.lower().endswith(".mp3")
}

expected_set = set(expected_files.keys())

# Songs that are missing
missing = expected_set - actual_files
# Songs that are extra (not expected)
extra = actual_files - expected_set

# Write missing songs to file
missing_path = os.path.join(output_folder, "missing.txt")
with open(missing_path, "w", encoding="utf-8") as f:
    f.write("Song|Artist|Album|Link\n")
    for filename in missing:
        f.write(expected_files[filename] + "\n")

# Write extra songs to file
extra_path = os.path.join(output_folder, "extra.txt")
with open(extra_path, "w", encoding="utf-8") as f:
    for filename in extra:
        f.write(filename + "\n")

print(f"Created missing file list: {missing_path}")
print(f"Created extra file list: {extra_path}")

# Count tracks in playlist (skip header)
with open(playlist_path, "r", encoding="utf-8") as f:
    playlist_lines = [line.strip() for line in f.readlines() if line.strip()]
    playlist_count = len(playlist_lines) - 1  # minus the header "Song|Artist|Album|Link"

# Count mp3 files in songs folder
songs_count = len([
    f for f in os.listdir(songs_folder)
    if f.lower().endswith(".mp3")
])

# Output summary
print(f"🎵 In playlist: {playlist_count} tracks")
print(f"📁 In folder: {songs_count} files")
if playlist_count == songs_count:
    print("✅ Counts match.")
else:
    print("⚠️ Counts DO NOT match.")
