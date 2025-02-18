import os
import subprocess
import zipfile

# === 설정 ===
AUDIO_FOLDER = "./audio"  # 오디오 파일 폴더
OUTPUT_FOLDER = os.path.join(AUDIO_FOLDER, "transcriptions")  # 변환된 텍스트 저장 폴더
WHISPER_MODEL = "large"  # Whisper 모델 선택 (tiny, base, small, medium, large)
ZIP = False  # 압축 여부 (True: 압축, False: 미압축)
if ZIP:
    ZIP_PATH = os.path.join(AUDIO_FOLDER, "transcriptions.zip")  # 압축 파일 경로
# =============

# 저장 폴더 생성
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# 폴더 내 오디오 파일 목록 가져오기
audio_files = [f for f in os.listdir(AUDIO_FOLDER) if f.endswith(('.mp3', '.wav', '.m4a', '.flac'))]

# 타임스탬프 변환 함수
def convert_srt_to_txt(srt_file, txt_file):
    """ SRT 파일을 읽고, 타임스탬프 포함한 TXT 형식으로 변환 """
    with open(srt_file, "r", encoding="utf-8") as srt, open(txt_file, "w", encoding="utf-8") as txt:
        lines = srt.readlines()
        buffer = []
        for line in lines:
            line = line.strip()
            if "-->" in line:  # 타임스탬프 라인
                start, end = line.split(" --> ")
                start = start.replace(",", ".")  # Whisper는 , 대신 . 사용
                end = end.replace(",", ".")
                buffer.append(f"[{start} --> {end}] ")  # 타임스탬프 형식 맞추기
            elif line.isdigit():  # SRT 번호 제거
                continue
            elif line == "":
                if buffer:
                    txt.write("".join(buffer) + "\n")
                    buffer = []
            else:
                buffer.append(line + " ")  # 텍스트 추가

# Whisper로 변환
def transcribe_audio(file_path, output_txt_path):
    srt_path = output_txt_path.replace(".txt", ".srt")  # Whisper SRT 파일 경로

    # Whisper 실행 (SRT 포맷으로 저장)
    command = f'whisper "{file_path}" --model {WHISPER_MODEL} --output_format srt --output_dir "{OUTPUT_FOLDER}"'
    subprocess.run(command, shell=True, check=True)

    # SRT -> TXT 변환
    convert_srt_to_txt(srt_path, output_txt_path)
    print(f"✅ 변환 완료: {file_path} → {output_txt_path}")

# 변환 실행
for audio_file in audio_files:
    audio_path = os.path.join(AUDIO_FOLDER, audio_file)
    txt_filename = os.path.splitext(audio_file)[0] + ".txt"
    txt_path = os.path.join(OUTPUT_FOLDER, txt_filename)
    transcribe_audio(audio_path, txt_path)

print("\n🎉 모든 파일 변환 완료!")

# 변환된 txt 파일을 압축하기
if ZIP:
    with zipfile.ZipFile(ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for txt_file in os.listdir(OUTPUT_FOLDER):
            if txt_file.endswith(".txt"):
                txt_path = os.path.join(OUTPUT_FOLDER, txt_file)
                zipf.write(txt_path, os.path.basename(txt_path))

    print(f"✅ 모든 텍스트 파일이 압축되었습니다: {ZIP_PATH}")


