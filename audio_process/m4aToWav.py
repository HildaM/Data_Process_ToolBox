import os
import subprocess
from pydub import AudioSegment

def convert_m4a_to_wav(input_file_path):
    # 使用绝对路径
    input_file_path = os.path.abspath(input_file_path)

    # 检查输入文件是否存在
    if not os.path.isfile(input_file_path):
        print(f"文件 {input_file_path} 不存在")
        return

    # 获取文件名和扩展名
    file_name, file_extension = os.path.splitext(input_file_path)
    
    # 检查文件扩展名是否为 .m4a
    if file_extension.lower() != '.m4a':
        print("输入文件不是 m4a 格式")
        return

    # 输出文件路径
    output_file_path = file_name + '.wav'

    try:
        # 使用 pydub 进行格式转换
        audio = AudioSegment.from_file(input_file_path, format='m4a')
        audio.export(output_file_path, format='wav')
        print(f"转换完成，输出文件路径为：{output_file_path}")
    except Exception as e:
        print(f"使用 pydub 转换失败：{str(e)}")
        print("尝试使用 FFmpeg 直接转换...")
        
        try:
            # 使用 FFmpeg 命令行直接转换
            subprocess.run(['ffmpeg', '-i', input_file_path, output_file_path], check=True)
            print(f"FFmpeg 转换完成，输出文件路径为：{output_file_path}")
        except subprocess.CalledProcessError as e:
            print(f"FFmpeg 转换失败：{str(e)}")
        except FileNotFoundError:
            print("FFmpeg 未安装或未添加到系统路径")

if __name__ == "__main__":
    input_file_path = input("请输入 m4a 文件路径：")
    convert_m4a_to_wav(input_file_path)