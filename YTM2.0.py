'''
___________________________________________________________________________________________________________
Run this file first, after downloading the HTML page of tracks named 'YouTube Music.html'
-----------------------------------------------------------------------------------------------------------
Extracts from 'YouTube Music.html' the song title, artist, album, and link, and puts them into the file '2.0.txt' in the same folder
‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
'''
from bs4 import BeautifulSoup

with open('YouTube Music.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

tracks_info = []

# Find all blocks containing tracks
blocks = soup.find_all('div', class_='flex-columns style-scope ytmusic-responsive-list-item-renderer')

for block in blocks:
    song = None
    artist = None
    album = None
    song_link = None

    # Search for all links inside the block
    links = block.find_all('a', class_='yt-simple-endpoint style-scope yt-formatted-string')

    for a in links:
        href = a.get('href', '')
        text = a.text.strip()
        if not text:
            continue

        if 'watch?v=' in href:
            song = text
            if href.startswith('http'):
                song_link = href
            else:
                song_link = 'https://music.youtube.com' + href
        elif 'channel/' in href:
            if artist is None:
                artist = text
            else:
                artist += ', ' + text
        elif 'browse/' in href:
            album = text

    if artist is None:
        artist_span = block.find('yt-formatted-string', class_='flex-column style-scope ytmusic-responsive-list-item-renderer')
        if artist_span:
            artist = artist_span.get_text(strip=True)

    if song:
        tracks_info.append({
            'song': song,
            'artist': artist if artist else '',
            'album': album if album else '',
            'link': song_link if song_link else ''
        })

with open('2.0.txt', 'w', encoding='utf-8') as f:
    f.write('Song|Artist|Album|Link\n')
    for t in tracks_info:
        f.write(f"{t['song']} | {t['artist']} | {t['album']} | {t['link']}\n")

print(f'Found tracks: {len(tracks_info)}')
