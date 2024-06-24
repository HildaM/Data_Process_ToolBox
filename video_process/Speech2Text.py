"""
Speech2Text.py 语音转文字
同时支持视频和音频格式：
- mp4
- mp3
- m4a
- wav
- flac

请注意：不适用于歌曲处理，仅适用于讲话、演讲等音频内容。

"""
import os
import whisper
import moviepy.editor as mp
from pydub import AudioSegment
from tqdm import tqdm
import time

# 全局变量：定义项目根目录和相关文件夹
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
TEMP_FOLDER = os.path.join(PROJECT_ROOT, "temp")
RESULT_FOLDER = os.path.join(PROJECT_ROOT, "result")

class Speech2Text:
    # 定义支持的音频和视频格式
    SUPPORTED_AUDIO_FORMATS = {
        'wav': AudioSegment.from_wav,
        'm4a': AudioSegment.from_file,
        'mp3': AudioSegment.from_mp3,
        'flac': AudioSegment.from_file
    }
    SUPPORTED_VIDEO_FORMATS = ['mp4', 'avi', 'mov']

    def __init__(self, whisper_model="large", whisper_device="cuda"):
        self.whisper_model = whisper_model
        self.whisper_device = whisper_device
        self.ensure_directories()

    @staticmethod
    def ensure_directories():
        # 确保临时文件夹和结果文件夹存在
        for directory in [TEMP_FOLDER, RESULT_FOLDER]:
            os.makedirs(directory, exist_ok=True)

    @staticmethod
    def format_time(seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}分{seconds:02d}秒"

    def get_audio_path(self, input_path):
        # 生成临时音频文件的路径
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        return os.path.join(TEMP_FOLDER, f"{base_name}.wav")

    def extract_audio(self, input_path):
        # 从输入文件中提取音频
        audio_path = self.get_audio_path(input_path)
        if os.path.exists(audio_path):
            print(f"音频文件 {audio_path} 已存在。跳过提取步骤。")
            return audio_path

        file_extension = os.path.splitext(input_path)[1][1:].lower()

        if file_extension in self.SUPPORTED_AUDIO_FORMATS:
            print("正在提取音频...")
            # 使用pydub处理音频文件
            audio = self.SUPPORTED_AUDIO_FORMATS[file_extension](input_path)
            audio.export(audio_path, format="wav")
            duration = len(audio) / 1000
            print(f"音频文件提取完成，文件名: {audio_path}, 时长: {self.format_time(duration)}")

        elif file_extension in self.SUPPORTED_VIDEO_FORMATS:
            print("正在从视频中提取音频...")
            # 使用moviepy处理视频文件
            video = mp.VideoFileClip(input_path)
            audio = video.audio
            audio.write_audiofile(audio_path, progress_bar=True)
            duration = video.duration
            video.close()
            print(f"音频文件提取完成，文件名: {audio_path}, 时长: {self.format_time(duration)}")

        else:
            raise ValueError(f"不支持的文件格式: {file_extension}")

        return audio_path


    def transcribe_audio(self, audio_path):
        print("正在转录音频...")
        # 使用Whisper模型进行音频转录
        model = whisper.load_model(self.whisper_model, device=self.whisper_device)
        
        # 开始转录，使用verbose参数显示进度
        start_time = time.time()
        result = model.transcribe(audio_path, language="zh", verbose=False)  # verbose=True 显示进度（注释会非常多）默认为False
        end_time = time.time()
        print(f"转录完成，耗时 {Speech2Text.format_time(end_time - start_time)}")

        return result


    def save_transcription_to_txt(self, transcription_result, output_path):
        print("正在保存转录结果...")
        total_segments = len(transcription_result["segments"])
        with open(output_path, "w", encoding="utf-8") as txt_file:
            # 使用tqdm显示保存进度
            for segment in tqdm(transcription_result["segments"], total=total_segments, desc="保存进度"):
                txt_file.write(f"{segment['text']}\n")

    def process_file(self, input_path):
        # 主处理函数，处理输入的音频或视频文件
        input_path = input_path.strip()  # 去除文件路径两端的空格
        file_extension = os.path.splitext(input_path)[1][1:].lower()
        if file_extension in self.SUPPORTED_VIDEO_FORMATS:
            print(f"正在处理视频文件: {input_path}")
        elif file_extension in self.SUPPORTED_AUDIO_FORMATS:
            print(f"正在处理音频文件: {input_path}")
        else:
            raise ValueError(f"不支持的文件格式: {file_extension}")

        # 步骤1：提取音频
        audio_path = self.extract_audio(input_path)
        # 步骤2：转录音频
        transcription_result = self.transcribe_audio(audio_path)
        
        # 步骤3：保存转录结果
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(RESULT_FOLDER, f"{base_name}_transcription.txt")
        self.save_transcription_to_txt(transcription_result, output_path)
        
        print(f"转录结果已保存至: {output_path}")



if __name__ == "__main__":
    converter = Speech2Text()
    input_path = input("请输入音频或视频文件地址: ")
    converter.process_file(input_path)