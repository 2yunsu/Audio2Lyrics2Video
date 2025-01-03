import csv

# 원본 CSV 파일 경로와 새로운 CSV 파일 경로
lyrics_csv_path = "processed_lyrics.csv"  # 대조할 lyrics가 있는 CSV
tokens_csv_path = "50 sample.csv"  # 토큰 리스트를 만든 CSV
output_csv_path = "output_with_gt.csv"  # 결과를 저장할 CSV 파일

# 토큰 리스트 가져오기
lyrics_tokens_list = []
with open(tokens_csv_path, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        if 'Lyrics' in row:
            tokens = row['Lyrics'].split()
            lyrics_tokens_list.extend(tokens)  # 전체 토큰을 하나의 리스트로 추가

# 원본 CSV에 대조하여 일치하는 토큰을 gt 열로 추가하고 사용된 토큰 제거
with open(lyrics_csv_path, mode="r", encoding="utf-8") as input_file, \
     open(output_csv_path, mode="w", encoding="utf-8", newline="") as output_file:

    reader = csv.DictReader(input_file)
    fieldnames = reader.fieldnames + ['gt']  # 기존 필드에 'gt' 열 추가
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        current_lyrics = row['lyrics']
        matching_tokens = []

        # Lyrics와 일치하는 모든 토큰 추출
        for token in list(lyrics_tokens_list):  # 리스트 복사본으로 순회
            if token in current_lyrics:
                matching_tokens.append(token)
                lyrics_tokens_list.remove(token)  # 사용된 토큰 제거

        # gt 열에 매칭된 토큰 추가 (공백으로 연결)
        row['gt'] = " ".join(matching_tokens) if matching_tokens else ""
        writer.writerow(row)

print(f"결과가 {output_csv_path}에 저장되었습니다.")