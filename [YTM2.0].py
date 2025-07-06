'''
___________________________________________________________________________________________________________
этот файл запускать первым, после скачивания html страницы треков под названием 'YouTube Music.html'
-----------------------------------------------------------------------------------------------------------
Вытягивает из 'YouTube Music.html' название, группу, альбом, ссылку и пихает в файл '2.0.txt' здесь же
‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
'''
from bs4 import BeautifulSoup

with open('YouTube Music.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

tracks_info = []

# Находим все блоки с треками
blocks = soup.find_all('div', class_='flex-columns style-scope ytmusic-responsive-list-item-renderer')

for block in blocks:
    song = None
    artist = None
    album = None
    song_link = None

    # Ищем все ссылки внутри блока
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

print(f'Найдено треков: {len(tracks_info)}')
