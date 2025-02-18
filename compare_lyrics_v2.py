import os
import openai
import re
import pandas as pd
from fuzzywuzzy import process
import unicodedata

# === 🔧 설정 ===
SRT_FOLDER = "./audio/transcriptions"
CSV_PATH = "50 Deutsche Lieder.csv"
OPENAI_API_KEY = ""  # 🔑 OpenAI API 키 입력

# OpenAI API 설정
openai.api_key = OPENAI_API_KEY

# CSV 데이터 불러오기
df = pd.read_csv(CSV_PATH, encoding="utf-8")

# === 📌 제목 추출 함수 ===
def extract_title(filename):
    """SRT 파일명에서 ' - ' 와 '(' 사이의 문자열을 추출하여 Title로 사용"""
    match = re.search(r" - (.*?) \(", filename)
    return match.group(1).strip() if match else None

def find_best_match(title, title_list):
    best_match = process.extractOne(title, title_list)
    return best_match[0] if best_match else None

def normalize_text(text):
    """유니코드 정규화를 적용해 독일어의 ö, ü, ä 같은 문자를 ASCII로 변환"""
    if pd.isna(text):  # NaN 값 체크
        return ""  
    return unicodedata.normalize('NFKD', str(text)).encode('ASCII', 'ignore').decode('utf-8')

def clean_text(text):
    return re.sub(r"[^\w\s]", "", text).strip().lower()

def remove_duplicates(text):
    """중복된 단어 또는 문장을 제거하는 함수"""
    words = text.split()
    unique_words = []
    prev_word = None
    for word in words:
        if word != prev_word:
            unique_words.append(word)
        prev_word = word
    return " ".join(unique_words)

def transform_text_by_tokens(original_text, gt_lyrics):
    """문맥을 고려하여 가장 유사한 원본 가사 조각으로 변환하고 중복 제거"""
    original_tokens = original_text.split()
    gt_lyrics_lines = gt_lyrics.split("\n")  # 원본 가사를 줄 단위로 나누기
    gt_phrases = [" ".join(line.split()[:4]) for line in gt_lyrics_lines]  # 문맥을 고려해 4단어씩 묶기
    breakpoint()
    transformed_tokens = []
    skip_next = False

    for i, token in enumerate(original_tokens):
        if skip_next:
            skip_next = False
            continue

        # 현재 단어 + 다음 단어까지 포함한 프레이즈(최대 2그램)
        phrase = " ".join(original_tokens[i:i+2])

        # 전체 원본 가사에서 가장 유사한 문구 찾기
        best_match, score = process.extractOne(phrase, gt_phrases) if gt_phrases else (phrase, 0)

        if score >= 85:  # 높은 유사도일 때 변환
            transformed_tokens.append(best_match)
            skip_next = True  # 2그램을 매칭했으므로 다음 단어는 건너뛴다
        else:
            best_match, score = process.extractOne(token, gt_lyrics_lines) if gt_lyrics_lines else (token, 0)
            transformed_tokens.append(best_match if score >= 80 else token)

    # 중복 제거
    transformed_text = remove_duplicates(" ".join(transformed_tokens))
    return transformed_text

def read_srt(srt_path):
    """SRT 파일을 읽어서 (번호, 타임스탬프, 문장) 리스트 반환"""
    with open(srt_path, "r", encoding="utf-8") as f:
        content = f.read()

    entries = []
    blocks = content.strip().split("\n\n")  # 빈 줄 기준으로 블록 나누기
    for block in blocks:
        lines = block.split("\n")
        if len(lines) >= 3:
            num = lines[0]
            timestamp = lines[1]
            text = " ".join(lines[2:])
            entries.append((num, timestamp, text))
    return entries

# # === 📌 SRT 파일 읽기 ===
# def read_srt(file_path):
#     """SRT 파일을 읽어서 (번호, 타임스탬프, 가사) 리스트로 반환"""
#     with open(file_path, "r", encoding="utf-8") as f:
#         lines = f.readlines()
    
#     srt_entries = []
#     i = 0
#     while i < len(lines):
#         if lines[i].strip().isdigit():  # 번호
#             num = int(lines[i].strip())
#             i += 1
#             timestamp = lines[i].strip()  # 타임스탬프
#             i += 1
#             lyrics = []
#             while i < len(lines) and lines[i].strip() and "-->" not in lines[i]:
#                 lyrics.append(lines[i].strip())
#                 i += 1
#             original_lyrics = " ".join(lyrics)
#             srt_entries.append((num, timestamp, original_lyrics))
#         i += 1
    
#     return srt_entries


# # === 🔥 GPT 변환 함수 ===
# def convert_lyrics_with_gpt(original_lyrics, gt_lyrics, gt_kr_lyrics):
#     """ChatGPT API를 사용하여 원본 SRT 가사를 변환"""
#     prompt = f"""
#     {original_lyrics}.srt는 Audio to Text 모델로 추출한 가사이고, {gt_lyrics}는 원문 가사, {gt_kr_lyrics}는 한국어 번역 가사야.
#     {original_lyrics}.srt 가사의 시간대별 가사를 시간 정보는 유지한 채 {gt_lyrics}에 대응하는 독일어 가사로 바꾸어주고,
#     각 독일어 가사 오른쪽에 "/n {gt_kr_lyrics}"를 추가해줘.
#     """
    
#     response = openai.ChatCompletion.create(
#         model="gpt-4",
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0.7
#     )
    
#     return response["choices"][0]["message"]["content"].strip()

# === 🔍 폴더 내 모든 SRT 파일 변환 ===
for srt_file in os.listdir(SRT_FOLDER):
    if srt_file.endswith(".srt"):
        srt_path = os.path.join(SRT_FOLDER, srt_file)
        title = extract_title(srt_file)
        print("title:", title)
        
        if title:
            # matched_row = df[df["Title"] == title]
            # matched_row = df[df["Title"].str.strip().str.lower() == title.strip().lower()]
            normalized_title = normalize_text(title)  # 파일 이름을 변환
            df["Normalized_Title"] = df["Title"].apply(normalize_text)  # CSV의 Title 열 변환
            best_match, score, _ = process.extractOne(title, df["Normalized_Title"])
            if score >= 80:
                matched_row = df[df["Normalized_Title"] == best_match]
            else:
                matched_row = pd.DataFrame()  # 매칭 실패 시 빈 DataFrame 반환
            # matched_row = df[df["Normalized_Title"] == normalized_title]  # 변환된 문자열로 비교


            if not matched_row.empty:
                srt_entries = read_srt(srt_path)
                gt_lyrics = matched_row.iloc[0]["Lyrics"]
                gt_kr_lyrics = matched_row.iloc[0]["Ko_lyrics"]

                # 변환된 가사 저장할 리스트
                new_srt_content = []
                for num, timestamp, original_text in srt_entries:
                    # 전처리 적용
                    # cleaned_original = clean_text(original_text)
                    # cleaned_lyrics = [clean_text(line) for line in gt_lyrics]

                    # transformed_text = convert_lyrics_with_gpt(original_text, gt_lyrics, gt_kr_lyrics)
                    # transformed_text = process.extractOne(original_text, gt_lyrics.split("\n"))[0]
                    # breakpoint()
                    transformed_text = transform_text_by_tokens(original_text, gt_lyrics)
                    new_srt_content.append(f"{num}\n{timestamp}\n{transformed_text}\n")
                # 변환된 SRT 저장
                new_srt_path = os.path.join("./audio/converted", srt_file)
                with open(new_srt_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(new_srt_content))

                print(f"✅ 변환 완료: {new_srt_path}")
            else:
                print(f"⚠️ {title}: CSV에서 찾을 수 없음")

print("\n🎉 모든 변환이 완료되었습니다!")
