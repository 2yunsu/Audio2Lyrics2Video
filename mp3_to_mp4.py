import os
from moviepy.editor import AudioFileClip, ImageClip

def convert_mp3_to_mp4(input_folder, output_folder, image=None):
    """폴더 내 모든 MP3 파일을 MP4로 변환"""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file in os.listdir(input_folder):
        if file.endswith(".mp3"):
            mp3_path = os.path.join(input_folder, file)
            mp4_path = os.path.join(output_folder, file.replace(".mp3", ".mp4"))

            audio = AudioFileClip(mp3_path)

            if image:
                video = ImageClip(image, duration=audio.duration)
                video = video.set_audio(audio)
                video.write_videofile(mp4_path, fps=1)
            else:
                audio.write_videofile(mp4_path, codec="libx264", audio_codec="aac")

            audio.close()
            print(f"✅ 변환 완료: {mp3_path} → {mp4_path}")

# 사용 예제
input_folder = "./audio"  # MP3 파일 폴더
output_folder = "./audio/mp4"  # 변환된 MP4 저장 폴더
background_image = "./audio/black.jpg"  # 배경 이미지 (선택)

convert_mp3_to_mp4(input_folder, output_folder, image=background_image)