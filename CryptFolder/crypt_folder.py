import os
import base64

def encode_to_base64(content):
    return base64.b64encode(content).decode('utf-8')

def decode_from_base64(content):
    return base64.b64decode(content.encode('utf-8'))

def should_encrypt(relative_path):
    return relative_path.endswith('.go') or relative_path.endswith('.mod') or relative_path.endswith('.md')

def encrypt_file(file_path, relative_path):
    try:
        # 修改文件后缀为 .txt
        txt_file_path = file_path + '.txt'
        os.rename(file_path, txt_file_path)
      
        with open(txt_file_path, 'rb') as file:
            content = file.read()
      
        os.rename(txt_file_path, file_path)  # 还原文件名
      
        encoded_content = encode_to_base64(content)
        original_extension = os.path.splitext(relative_path)[1]

        # 添加文件信息和标识符，使用不可在文件内容中出现的分隔符
        file_info = f"FILE_START|||{relative_path}|||{original_extension}\n"
        encrypted_content = file_info + encoded_content + "\nFILE_END\n"

        return encrypted_content
    except Exception as e:
        print(f"加密文件 {relative_path} 时出错: {str(e)}")
        return None

def encrypt_folder(folder_path):
    encrypted_content = ""
    for root, dirs, files in os.walk(folder_path):
        if '.git' in dirs:
            dirs.remove('.git')  # 不处理.git文件夹
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, folder_path)
            if should_encrypt(relative_path):
                encrypted_file = encrypt_file(file_path, relative_path)
                if encrypted_file:
                    encrypted_content += encrypted_file

    folder_name = os.path.basename(folder_path)
    return f"FOLDER_START|{folder_name}\n{encrypted_content}FOLDER_END\n"

def encrypt_project(project_path):
    encrypted_content = encrypt_folder(project_path)

    # 将加密内容写入文件
    with open('encrypted_project.txt', 'w', encoding='utf-8') as f:
        f.write(encrypted_content)

    print("项目加密完成，加密文件保存为 'encrypted_project.txt'")

def decrypt_file(file_content):
    try:
        # 分离文件路径和编码内容
        parts = file_content.split('\n', 2)
        if len(parts) != 3 or not parts[0].startswith("FILE_START|||"):
            raise ValueError("无效的文件内容格式")

        file_info_parts = parts[0].split('|||')
        if len(file_info_parts) != 3:
            raise ValueError("无效的文件信息格式")

        relative_path = file_info_parts[1]
        original_extension = file_info_parts[2]
        encoded_content = parts[1]

        decoded_content = decode_from_base64(encoded_content)

        return relative_path, decoded_content, original_extension
    except Exception as e:
        print(f"解密文件时出错: {str(e)}")
        print(f"问题内容: {file_content[:100]}...")  # 打印前100个字符用于调试
        return None, None, None

def decrypt_project(encrypted_file_path, output_path):
    try:
        with open(encrypted_file_path, 'r', encoding='utf-8') as f:
            encrypted_content = f.read()

        folders = encrypted_content.split('FOLDER_START|')
        for folder in folders[1:]:  # 跳过第一个空元素
            folder_parts = folder.split('\n', 1)
            if len(folder_parts) < 2:
                print(f"警告: 跳过无效的文件夹内容")
                continue

            folder_name = folder_parts[0]
            folder_content = folder_parts[1].split('FOLDER_END')[0]

            files = folder_content.split('FILE_START|||')
            for file in files[1:]:  # 跳过第一个空元素
                file_parts = file.split('FILE_END')
                if len(file_parts) < 1:
                    print(f"警告: 跳过无效的文件内容")
                    continue

                file_content = 'FILE_START|||' + file_parts[0]  # 补上前缀
                relative_path, decrypted_content, original_extension = decrypt_file(file_content)

                if relative_path and decrypted_content is not None:
                    # 创建完整的文件路径，包括根目录
                    full_path = os.path.join(output_path, relative_path)
                    os.makedirs(os.path.dirname(full_path), exist_ok=True)

                    # 创建 .txt 文件
                    txt_path = full_path + ".txt"
                    with open(txt_path, 'wb') as f:
                        f.write(decrypted_content)

                    # 重命名为原始文件名
                    base_name, _ = os.path.splitext(full_path)
                    original_path = base_name + original_extension
                    os.rename(txt_path, original_path)
                    print(f"成功解密文件: {relative_path}")
                else:
                    print(f"警告: 跳过无法解密的文件")

        print(f"项目解密完成，解密后的文件保存在 '{output_path}' 目录下")
    except Exception as e:
        print(f"解密项目时出错: {str(e)}")

def main():
    while True:
        print("\n欢迎使用文件夹加密解密工具")
        print("1. 加密项目")
        print("2. 解密项目")
        print("3. 退出")

        choice = input("请选择操作 (1/2/3): ").strip()

        if choice == '1':
            project_path = input("请输入要加密的项目文件夹路径: ").strip()
            if os.path.isdir(project_path):
                encrypt_project(project_path)
            else:
                print("错误：无效的文件夹路径")

        elif choice == '2':
            encrypted_file_path = input("请输入加密文件的路径: ").strip()
            output_path = input("请输入解密后文件的保存路径: ").strip()

            if os.path.isfile(encrypted_file_path):
                decrypt_project(encrypted_file_path, output_path)
            else:
                print("错误：无效的加密文件路径")

        elif choice == '3':
            print("感谢使用，再见！")
            break

        else:
            print("无效的选择，请重新输入")

if __name__ == "__main__":
    main()