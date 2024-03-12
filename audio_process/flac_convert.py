from pydub import AudioSegment
import os

def convert_flac(flac_file_path, output_file_name, output_format, bitrate="320k"):
    # 获取FLAC文件所在的目录
    directory = os.path.dirname(flac_file_path)
    
    # 构建输出文件的完整路径
    output_file_path = os.path.join(directory, f"{output_file_name}.{output_format}")
    
    # 加载FLAC文件
    audio = AudioSegment.from_file(flac_file_path, "flac")
    
    # 根据用户选择的格式导出文件
    if output_format == 'wav':
        audio.export(output_file_path, format="wav")
    elif output_format == 'mp3':
        audio.export(output_file_path, format="mp3", bitrate=bitrate)
    else:
        print("发生错误：不支持的格式。")

if __name__ == "__main__":
    print("欢迎使用FLAC文件转换器！")
    flac_file_path = input("请输入FLAC音频文件的完整路径：")
    print("请选择希望转换的格式：\n1. MP3\n2. WAV")
    format_choice = input("请输入选项的序号（例如，对于MP3请输入1）：")
    
    format_dict = {"1": "mp3", "2": "wav"}
    
    output_format = format_dict.get(format_choice)
    if not output_format:
        print("错误：请输入有效的序号（1或2）。")
    else:
        output_file_name = input("请输入输出文件的名称（不包括扩展名）：")
        convert_flac(flac_file_path, output_file_name, output_format)
        print(f"转换完成！文件已保存。")