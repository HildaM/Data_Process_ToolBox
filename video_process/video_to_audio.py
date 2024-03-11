from moviepy.editor import VideoFileClip

def extract_audio(mp4_file_path, output_audio_name, audio_format):
    """
    从MP4视频文件中提取音频，并将其保存到指定路径和格式。
    
    :param mp4_file_path: MP4视频文件的路径。
    :param output_audio_name: 输出音频文件的名称（不含扩展名）。
    :param audio_format: 用户选择的音频格式。
    """
    # 根据用户选择的格式确定文件扩展名和编解码器
    if audio_format == "1":
        extension = ".mp3"
        codec = "libmp3lame"
    elif audio_format == "2":
        extension = ".flac"
        codec = "flac"
    else:
        print("未选择有效的格式，程序将退出。")
        return

    output_audio_path = output_audio_name + extension
    
    # 尝试加载视频文件
    try:
        video = VideoFileClip(mp4_file_path)
    except IOError as e:
        print(f"无法加载文件：{mp4_file_path}。请确保文件路径正确，且文件存在。")
        return

    # 提取音频
    audio = video.audio
    
    # 尝试将音频保存到指定路径和格式
    try:
        audio.write_audiofile(output_audio_path, codec=codec)
    except Exception as e:
        print(f"保存音频文件时出错：{e}")
    else:
        print(f"音频已成功保存至：{output_audio_path}")
    
    # 关闭视频和音频文件，释放资源
    video.close()
    audio.close()

# 主程序
if __name__ == "__main__":
    print("请输入MP4视频文件的完整路径：")
    mp4_file_path = input().strip()  # 去除可能的前后空格

    print("请选择输出音频的格式（输入数字）：\n1. MP3\n2. FLAC")
    audio_format = input().strip()

    print("请输入输出音频文件的名称（不需要扩展名）：")
    output_audio_name = input().strip()
    
    extract_audio(mp4_file_path, output_audio_name, audio_format)