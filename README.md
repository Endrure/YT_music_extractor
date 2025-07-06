# User manual
Sadly i dont know how to use bat's yet so everything is done through python so here's how to use it
1. You'll need to make sure you've got all libraries downloaded you can do it by typing in CMD:
  pip install beautifulsoup4 requests mutagen ytmusicapi
2. Go to https://music.youtube.com/library/songs and scroll down loading all the songs(make sure the album covers are loaded properly)
3. Download the hmtl of the page(Ctrl + S) make sure to name it 'YouTube Music.html' with a space and put it in the same folder as python files
4. Open and run YTM2.0.py it will create file 2.0.txt with all the information about songs that you're going to download
5. Open and run comporator_better_quality_working.py it will download songs with working metadata and 400*400 covers at the rate of about 1 song per minute to the folder "songs" in the same directory. At the same time it will create file 'age_restricted_file.txt' with all the songs that couldn't be downloaded due to YT asking to sing in for access to songs with sexual lyrics which i couldnt implement(must be downloaded another way) and it will write the progress in the output in case anything happens. Sometimes YT gets suspicious of the traffic so the will be 10 minutes pause in that case that wont affect downloaded files.
6. You can open and run file checker.py to check if all the songs were downloaded succesfully and metadata_fixer.py in case some metadata and especially covers were downloaded incorrectly or weren't at all(happens if the name is too long)
7. You're all set. Anything and everythingcan be deleted at your will
