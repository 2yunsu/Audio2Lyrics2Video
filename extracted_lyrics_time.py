import pandas as pd
import re

# CSV 파일 경로
file_path = "extracted_lyrics_kor.csv"

# CSV 파일 읽기 (가정: 내용은 텍스트 파일 형식으로 저장되어 있음)
with open(file_path, "r", encoding="utf-8") as file:
    lines = file.readlines()

# 데이터를 저장할 리스트 초기화
data = []

# 각 줄을 처리하여 start_time, end_time, lyrics로 분리
for line in lines:
    match = re.match(r"\[(\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}\.\d{3})\]\s*(.*)", line)
    if match:
        start_time = match.group(1)
        end_time = match.group(2)
        lyrics = match.group(3)
        data.append({"start_time": start_time, "end_time": end_time, "lyrics": lyrics})

# DataFrame으로 변환
df = pd.DataFrame(data)

# 결과 출력 및 저장 (원하는 파일명으로 저장 가능)
# print(df)
df.to_csv("processed_lyrics_kor.csv", index=False, encoding="utf-8")
