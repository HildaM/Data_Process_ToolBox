# 文件夹文件批量重命名

import os
import shutil
from pathlib import Path

def batch_rename_files(source_folder, prefix):
    # 获取源文件夹的父目录和名称
    parent_dir = os.path.dirname(source_folder)
    source_folder_name = os.path.basename(source_folder)
    
    # 创建新文件夹名称
    new_folder_name = f"{source_folder_name}_renamed"
    new_folder_path = os.path.join(parent_dir, new_folder_name)
    
    # 创建新文件夹
    os.makedirs(new_folder_path, exist_ok=True)
    
    # 获取源文件夹中的所有文件
    files = sorted(os.listdir(source_folder))
    
    # 遍历文件并重命名
    for index, filename in enumerate(files, start=1):
        # 获取文件扩展名
        file_extension = os.path.splitext(filename)[1]
        
        # 创建新的文件名
        new_filename = f"{prefix}_{index:03d}{file_extension}"
        
        # 源文件的完整路径
        source_file = os.path.join(source_folder, filename)
        
        # 新文件的完整路径
        new_file = os.path.join(new_folder_path, new_filename)
        
        # 复制并重命名文件
        shutil.copy2(source_file, new_file)
        
        print(f"Renamed: {filename} -> {new_filename}")
    
    print(f"\nAll files have been renamed and copied to: {new_folder_path}")

if __name__ == "__main__":
    source_folder = input("Enter the source folder path: ")
    prefix = input("Enter the file name prefix: ")
    
    # 验证源文件夹路径是否存在
    if not os.path.isdir(source_folder):
        print("Error: The specified folder does not exist.")
    else:
        batch_rename_files(source_folder, prefix)