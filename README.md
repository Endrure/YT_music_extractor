# User Manual

This project downloads and organizes your YouTube Music library songs with metadata and album covers.

---

## Prerequisites

Make sure you have Python installed. Then install the required libraries by running this in your command prompt (CMD):

`pip install beautifulsoup4 requests mutagen ytmusicapi`

---

## How to Use

1. Open [YouTube Music Library](https://music.youtube.com/library/songs) in your browser.  
   Scroll down until all your songs and album covers are fully loaded.

2. Save the webpage as an HTML file:  
   Press **Ctrl + S**, name the file exactly `YouTube Music.html` (with the space),  
   and place it in the same folder as the Python scripts.

3. Run `YTM2.0.py` script:  
   This extracts all song information and saves it to `2.0.txt`.

4. **Before running** `comparator_better_quality_working.py`:  
Right after the import statements at the top of the script, locate the line  
`YTDLP_PATH = r"C:\Users\Me\example\yt-dlp.exe"`
and replace the example path "C:\Users\Me\example\yt-dlp.exe" with the full path to your local yt-dlp.exe file on your computer.
Then run the script:
   This downloads the songs with proper metadata and 400x400 album covers at roughly 1 song per 8 seconds.  
   Songs will be saved inside a `songs` folder created in the same directory.

   - The script also generates `age_restricted_file.txt` listing songs blocked due to age restrictions on YouTube.  
   - The progress and any errors are printed to the console.  
   - If YouTube detects unusual traffic, the script pauses for 10 minutes before retrying, without losing already downloaded files.

5. Optionally, run `checker.py` to verify that all songs were downloaded successfully.

6. Use `metadata_fixer.py` to fix any incorrect or missing metadata and covers, especially for files with long names.

---

## Cleanup

Once everything is done, you can safely delete any intermediate files or scripts as you wish.

---

If you have questions or issues, feel free to open an issue here on GitHub!
