import csv
import os

def add_hours_to_time(time_str):
    # 시간 정보가 없으면 "00"을 추가하여 시:분:초 형식으로 변경
    minutes, seconds = time_str.split(":")
    return f"00:{minutes}:{seconds}"

def csv_to_single_srt(csv_file, srt_file):
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(srt_file), exist_ok=True)

    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        srt_output = []
        counter = 1  # Subtitle numbering

        for row in reader:
            # Extract start_time, end_time, and text from the CSV
            start_time = row["start_time"]
            end_time = row["end_time"]
            text = row["lyrics"]

            # Add "00" for hours if time format is only minutes:seconds
            start_time = add_hours_to_time(start_time)
            end_time = add_hours_to_time(end_time)

            # Format into SRT block
            srt_output.append(f"{counter}\n{start_time.replace('.', ',')} --> {end_time.replace('.', ',')}\n{text}\n\n")
            counter += 1

    # Write all subtitles to a single .srt file
    with open(srt_file, "w", encoding="utf-8") as f:
        f.writelines(srt_output)

    print(f"SRT file saved as '{srt_file}'")

# Input CSV file and output SRT file
csv_file = "processed_lyrics_kor.csv"
srt_file = "srt_files/Wie bist du, meine Königin.srt"  # Make sure this is a full path to a file, not just a directory

# Convert CSV to single SRT file
csv_to_single_srt(csv_file, srt_file)