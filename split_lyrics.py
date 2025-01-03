import pandas as pd

# 원본 CSV 파일 로드
df = pd.read_csv('50 sample.csv')  # 'input_file.csv'에 원본 파일 경로를 넣으세요

# 'Lyrics' 열을 줄바꿈 기준으로 분할하여 여러 행으로 나누기
lyrics_expanded = df['Lyrics'].str.split('\n', expand=True).stack().reset_index(drop=True)

# 새로운 DataFrame 생성
expanded_df = pd.DataFrame({
    'Lyrics': lyrics_expanded
})

# 새로운 CSV 파일로 저장
expanded_df.to_csv('expanded_lyrics.csv', index=False)
