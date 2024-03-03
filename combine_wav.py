import os
import subprocess

# 定义一个函数，递归遍历文件夹寻找所有的WAV文件
def find_wav_files(directory, wav_files=[]):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.wav'):
                full_path = os.path.join(root, file)
                wav_files.append(full_path)
    return wav_files

def merge_wav_files(directory, output_filename):
    wav_files = find_wav_files(directory)
    list_file_path = os.path.join(directory, 'filelist.txt')
    
    # 将找到的WAV文件列表写入临时的文本文件中
    with open(list_file_path, 'w') as list_file:
        for wav_file in wav_files:
            list_file.write(f"file '{wav_file}'\n")
    
    # 使用FFmpeg命令合并WAV文件
    command = f'ffmpeg -f concat -safe 0 -i "{list_file_path}" -c copy "{output_filename}"'
    subprocess.run(command, shell=True)
    
    # 删除临时的列表文件
    os.remove(list_file_path)
    
    print(f"All WAV files in {directory} have been merged into {output_filename}.")

# 示例用法
if __name__ == "__main__":
    directory = input("Enter the directory path: ")
    output_filename = input("Enter the output filename: ")
    merge_wav_files(directory, output_filename)
