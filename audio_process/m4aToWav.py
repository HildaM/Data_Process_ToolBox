from pydub import AudioSegment
import os

def convert_m4a_to_wav(input_file_path):
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

    # 使用 pydub 进行格式转换
    audio = AudioSegment.from_file(input_file_path, format='m4a')
    audio.export(output_file_path, format='wav')

    print(f"转换完成，输出文件路径为：{output_file_path}")

if __name__ == "__main__":
    input_file_path = input("请输入 m4a 文件路径：")
    convert_m4a_to_wav(input_file_path)
