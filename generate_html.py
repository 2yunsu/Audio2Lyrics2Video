import os
import glob
import srt
from pathlib import Path
import json
import re
from moviepy.editor import *

def parse_srt_to_text(srt_path):
    """SRT 파일에서 순번을 제거하고, 시간과 가사를 유지하여 반환"""
    with open(srt_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    parsed_lines = []
    temp_block = []  # 한 블록(시간 + 가사) 저장용

    for line in lines:
        line = line.strip()
        
        # 숫자로 된 순번 제거
        if re.match(r"^\d+$", line):
            continue
        
        # 타임스탬프 감지
        if re.match(r"^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$", line):
            # 이전 블록 저장 후 초기화
            if temp_block:
                parsed_lines.append("\n".join(temp_block) + "\n")
                temp_block = []
            temp_block.append(line)  # 시간 정보 추가
        else:
            temp_block.append(line)  # 가사 추가

    # 마지막 블록 저장
    if temp_block:
        parsed_lines.append("\n".join(temp_block) + "\n")

    return "\n".join(parsed_lines)


def generate_html(mp3_file, srt_content):
    """MP3와 SRT 데이터를 포함하는 HTML 문자열 생성"""
    mp3_filename = os.path.basename(mp3_file)
    html_text = f"""
    <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{mp3_filename} Video Player</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 0;
      display: flex;
      flex-direction: column;
      align-items: center;
      background-color: #f4f4f4;
    }}
    video {{
      width: 80%;
      margin-top: 20px;
      position: relative;
    }}
    .subtitles {{
      width: 80%;
      margin-top: 20px;
      background: white;
      padding: 10px;
      border-radius: 5px;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }}
    .subtitle {{
      margin: 5px 0;
    }}
    .subtitle a {{
      color: #007BFF;
      text-decoration: none;
    }}
    .subtitle a:hover {{
      text-decoration: underline;
    }}
    .hidden {{
      display: none;
    }}
  </style>
</head>
<body>
  <video id="video" controls>
    <source src= "{mp3_filename}" type="video/mp4">
    <track id="subtitle-track" label="Deutsch" kind="subtitles" srclang="de" src="BrahmsOp.32.vtt" default>
    Your browser does not support the video tag.
  </video>

  <div class="subtitles" id="subtitles"></div>

  <script>
    // SRT data
    const srtData = {json.dumps(srt_content)};

    const subtitlesContainer = document.getElementById('subtitles');
    const video = document.getElementById('video');

    // Parse SRT
    function parseSRT(srt) {{
      const subtitles = [];
      const lines = srt.split('\\n');
      let subtitle = {{ start: null, end: null, text: '' }};

      lines.forEach((line) => {{
        const timeMatch = line.match(/(\d{{2}}:\d{{2}}:\d{{2}}),(\d{{3}}) --> (\d{{2}}:\d{{2}}:\d{{2}}),(\d{{3}})/);
        if (timeMatch) {{
          if (subtitle.text) subtitles.push(subtitle);
          subtitle = {{
            start: timeToSeconds(timeMatch[1], timeMatch[2]),
            end: timeToSeconds(timeMatch[3], timeMatch[4]),
            text: ''
          }};
        }} else if (line.trim() === '') {{
          if (subtitle.text) subtitles.push(subtitle);
          subtitle = {{ start: null, end: null, text: '' }};
        }} else {{
          subtitle.text += (subtitle.text ? '\\n' : '') + line;
        }}
      }});
      return subtitles;
    }}

    function timeToSeconds(hhmmss, milliseconds) {{
      const [hours, minutes, seconds] = hhmmss.split(':').map(Number);
      return hours * 3600 + minutes * 60 + seconds + milliseconds / 1000;
    }}

    // // Convert parsed subtitles to WebVTT format
    // function convertToVTT(subtitles) {{
    //   let vtt = 'WEBVTT\\n\\n';
    //   subtitles.forEach((subtitle) => {{
    //     const start = secondsToVTT(subtitle.start);
    //     const end = secondsToVTT(subtitle.end);
    //     vtt += `${{start}} --> ${{end}}\\n${{subtitle.text}}\\n\\n`;
    //   }});
    //   return vtt;
    // }}

        // Convert parsed subtitles to WebVTT format
    function convertToVTT(subtitles) {{
    let vtt = 'WEBVTT\\n\\n'; // Ensure proper WebVTT header
    subtitles.forEach((subtitle) => {{
        if (subtitle.text.trim()) {{ // Ignore empty or invalid subtitles
        const start = secondsToVTT(subtitle.start);
        const end = secondsToVTT(subtitle.end);
        vtt += `${{start}} --> ${{end}}\\n${{subtitle.text.trim()}}\\n\\n`;
        }}
    }});
    return vtt;
    }}

    function secondsToVTT(seconds) {{
      const hh = String(Math.floor(seconds / 3600)).padStart(2, '0');
      const mm = String(Math.floor((seconds % 3600) / 60)).padStart(2, '0');
      const ss = String(Math.floor(seconds % 60)).padStart(2, '0');
      const ms = String(Math.floor((seconds % 1) * 1000)).padStart(3, '0');
      return `${{hh}}:${{mm}}:${{ss}}.${{ms}}`;
    }}

    // Generate subtitle list
    function generateSubtitleList(subtitles) {{
      subtitles.forEach((subtitle) => {{
        const div = document.createElement('div');
        div.className = 'subtitle';
        const link = document.createElement('a');
        link.href = '#';
        link.textContent = subtitle.text;
        link.onclick = (e) => {{
          e.preventDefault();
          video.currentTime = subtitle.start;
          video.play();
        }};
        div.appendChild(link);
        subtitlesContainer.appendChild(div);
      }});
    }}

    // Add VTT track to video
    function addTrackToVideo(vttData) {{
      const blob = new Blob([vttData], {{ type: 'text/vtt' }});
      const url = URL.createObjectURL(blob);
      const track = document.getElementById('subtitle-track');
      track.src = url;
    }}

    // Main execution
    const subtitles = parseSRT(srtData);
    const vttData = convertToVTT(subtitles);
    addTrackToVideo(vttData);
    generateSubtitleList(subtitles);
  </script>
</body>
</html>

"""
    return html_text

def main():
    audio_dir = "./audio/mp4"
    # converted_dir = "./audio/converted"
    converted_dir = "./audio/transciption"
    output_dir = "./output_html"
    os.makedirs(output_dir, exist_ok=True)
    
    mp3_files = glob.glob(os.path.join(audio_dir, "*.mp4"))
    
    for mp3_file in mp3_files:
        filename = Path(mp3_file).stem
        srt_file = os.path.join(converted_dir, f"{filename}.srt")
        
        if os.path.exists(srt_file):
            subtitle_text = parse_srt_to_text(srt_file)
            html_content = generate_html(mp3_file, subtitle_text)
            output_path = os.path.join(output_dir, f"{filename}.html")
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            print(f"Generated: {output_path}")
        else:
            print(f"Warning: No matching SRT file for {mp3_file}")

if __name__ == "__main__":
    main()
