import os
import whisper
import moviepy.editor as mp

"""
对歌曲效果不好，非常差。
只适合用于普通视频
"""

# 全局变量
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
TEMP_FOLDER = os.path.join(PROJECT_ROOT, "temp")
AUDIO_PATH = os.path.join(TEMP_FOLDER, "extracted_audio.wav")
TIMEFRAME_FILE = os.path.join(TEMP_FOLDER, "timeframe.txt")
RESULT_FOLDER = os.path.join(PROJECT_ROOT, "result")

# Step 1: Extract audio from the video file
def extract_audio(video_path):
    audio_path = AUDIO_PATH
    if not os.path.exists(audio_path):
        video = mp.VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path)
    else:
        print(f"Audio file {audio_path} already exists. Skipping extraction.")

# Step 2: Convert audio to timestamped text using the Whisper model
def transcribe_audio(model, device):
    if os.path.exists(TIMEFRAME_FILE):
        print(f"TimeFrame file {TIMEFRAME_FILE} already exists. Skipping extraction.")
        return TIMEFRAME_FILE, True

    model = whisper.load_model(model, device=device)
    result = model.transcribe(AUDIO_PATH)
    return result, False

# Step 3: Save the transcribed text to a TXT file, with timestamps rounded to two decimal places
def save_transcription_to_txt(transcription_result, txt_path):
    with open(txt_path, "w", encoding="utf-8") as txt_file:
        for segment in transcription_result["segments"]:
            # start = round(segment['start'], 2)
            # end = round(segment['end'], 2)
            txt_file.write(f"{segment['text']}\n")



if __name__ == "__main__":
    video_path = input("请输入视频文件地址: ")
    extract_audio(video_path)
    transcription_result, exist = transcribe_audio("large", device="cuda")

    save_transcription_to_txt(transcription_result, TIMEFRAME_FILE)