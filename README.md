### Extract lyrics from audio files.
1. place audio files(mp3) to './audio' repo.
2. run 'Auto_Lyrics_v9.py' to extract lyrics from mp3 files.

```
python Auto_Lyrics_v9.py
```
> 'Auto_Lyrics_v9.py' is a modified version for extract many audio files from original code 'Auto_Lyrics_v9.ipynb'.

3. then, srt files and txt files will be saved as './audio/transcriptions' repo.

### Generate video files from audio files.
1. place images to './audio' repo(basic is 'black.jpg')
2. 
```
python mp3_to_mp4.py
```
3. then, mp4 files will be saved as './audio/mp4' repo.

### Generate html files from combine mp4 files and srt files.
1. set srt files repo at 'def main()' in 'generate_html.py'
```
def main():
    audio_dir = "./audio/mp4"
    # converted_dir = "./audio/converted"
    converted_dir = "./audio/transciption"
    output_dir = "./output_html"
```
> transciptrion is a raw srt files from mp3 files.
- Todo
> this code should be changed "./audio/converted" after comparing '50 Deutsche Lieder.csv' and srt files.

### Generate ground truth lyrics from '50 Deutsche Lieder.xlsx'.
1. run
```
python make_csv.py
```




### Todo
- 'compare_lyrics_v2.py'
    - set OPENAI_API_KEY
    - comparing '50 Deutsche Lieder.csv' and srt files.
    - one method is using LLM('compare). its advantage is high quality and simple. but it is expensive since Chat GPT is paid.
    - another method is using 'fuzzywuzzy' module. it's free but hard to code and quality is low.

- 'make_srt(not_use).py'
    - combine Korean lyrics and German lyrics from '50 Deutsche Lieder.csv'.