### Auto lyrics

## Extract lyrics from audio files
1. Place audio files(`.mp3`) in the './audio' directory.
2. Run `Auto_Lyrics_v9.py` to extract lyrics from the MP3 files:

```
python Auto_Lyrics_v9.py
```
> 'Auto_Lyrics_v9.py' is a modified version for extract many audio files from original code 'Auto_Lyrics_v9.ipynb'.

3. The extracted subtitle (`.srt`) and text (`.txt`) files will be saved in the ./audio/transcriptions directory.

## Generate video files from audio files
1. Place images in the `./audio` directory(default: `black.jpg`)
2. run `mp3_to_mp4.py`
```
python mp3_to_mp4.py
```
3. The generated `.mp4` files will be saved in the `./audio/mp4` directory.

## Generate HTML files by combining MP4 and SRT files.
1. Set SRT file directory in the `main()` function inside `generate_html.py`:
```
def main():
    audio_dir = "./audio/mp4"
    # converted_dir = "./audio/converted"
    converted_dir = "./audio/transciption"
    output_dir = "./output_html"
```
> `converted_dir` stores raw SRT files extracted from MP3 files.
- TODO: The script should be updated to use `./audio/converted` after comparing `50 Deutsche Lieder.csv` with the SRT files.

## How to use
1. place video files(`.mp4`), subtitle(`.srt`) and HTML files in the same directory.
2. Open the HTML file in a browser to view the content.

## TODO
## Generate ground truth lyrics from '50 Deutsche Lieder.xlsx'.
1. Run the following command:
```
python make_csv.py
```

- `compare_lyrics_v2.py`
    - Set `OPENAI_API_KEY`.
    - Compare '50 Deutsche Lieder.csv' with the extracted SRT files.
    - Comparison method
        - Using an LLM: High quality and simple, but expensive since ChatGPT requires a paid API.
        - Using the `fuzzywuzzy` module: Free but more complex to implement, with lower accuracy.

- `make_srt(not_use).py`
    - combine Korean lyrics and German lyrics from '50 Deutsche Lieder.csv'.
 

### repo
GitHub: [auto-lyrics](https://github.com/ras0k/auto-lyrics)
