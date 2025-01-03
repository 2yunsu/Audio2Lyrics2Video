import pandas as pd
import time
from pydub import AudioSegment
from pydub.playback import play
import threading

# CSV 파일 경로
csv_file = "output_with_gt.csv"
# 음원 파일 경로
audio_file = "Brahms_Op.32.mp3"

# CSV 데이터 읽기
df = pd.read_csv(csv_file)

# 시간을 초 단위로 변환하는 함수
def time_to_seconds(timestamp):
    parts = timestamp.split(":")
    if len(parts) == 3:  # hh:mm:ss 형식
        h, m, s = map(float, parts)
        return h * 3600 + m * 60 + s
    elif len(parts) == 2:  # mm:ss 형식
        m, s = map(float, parts)
        return m * 60 + s
    else:
        raise ValueError(f"Invalid time format: {timestamp}")

# 시작 시간과 종료 시간을 초 단위로 변환
df['start_seconds'] = df['start_time'].apply(time_to_seconds)
df['end_seconds'] = df['end_time'].apply(time_to_seconds)

# 자막 표시 함수
def display_subtitles(df):
    start_time = time.time()  # 현재 시간을 기준으로 시작
    for _, row in df.iterrows():
        # 자막이 표시될 시간을 기다림
        while time.time() - start_time < row['start_seconds']:
            time.sleep(0.01)  # CPU 점유를 줄이기 위해 잠시 대기
        # 자막 출력
        print(f"{row['lyrics']} ({row['gt']})")
        # 자막이 끝날 때까지 기다림
        while time.time() - start_time < row['end_seconds']:
            time.sleep(0.01)

# 음원 재생 함수
def play_audio(audio_file):
    audio = AudioSegment.from_file(audio_file)
    play(audio)

# 음원 재생과 자막 표시를 동시에 실행
audio_thread = threading.Thread(target=play_audio, args=(audio_file,))
subtitles_thread = threading.Thread(target=display_subtitles, args=(df,))

audio_thread.start()
subtitles_thread.start()

audio_thread.join()
subtitles_thread.join()