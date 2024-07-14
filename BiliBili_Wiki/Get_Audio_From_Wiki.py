# 从B站Wiki下载语音文件
# 参数说明：
# game_name: 游戏名称，例如 klbq
# character_name: 角色名称，例如 花鸟卷
# end_index：语音文件的最大索引，例如 19（建议取大一点的值，保证语音文件下载完全）

import requests
import urllib.parse
import os
from pathlib import Path

def make_request(game_name, wpvalue, cookies=None):
    encoded_wpvalue = urllib.parse.quote(wpvalue)
    url = f"https://wiki.biligame.com/{game_name}/%E7%89%B9%E6%AE%8A:%E9%87%8D%E5%AE%9A%E5%90%91/file?wptype=file&wpvalue={encoded_wpvalue}"
    
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Referer": f"https://wiki.biligame.com/{game_name}/%E7%89%B9%E6%AE%8A:%E9%87%8D%E5%AE%9A%E5%90%91/file",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
        "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"'
    }
    
    if cookies:
        headers["Cookie"] = cookies
    
    response = requests.get(url, headers=headers)
    return response

def download_audio_files(game_name, character_name, language, end_index, cookies=None):
    folder_name = f"{game_name}_{character_name}_{language}"
    Path(folder_name).mkdir(parents=True, exist_ok=True)
    
    for i in range(end_index + 1):
        index = f"{i:03d}"  # 将索引格式化为三位数，例如 000, 001, ..., 019
        wpvalue = f"{character_name}语音-{index}{language}.mp3"
        
        print(f"Downloading: {wpvalue}")
        response = make_request(game_name, wpvalue, cookies)
        
        if response.status_code == 200:
            file_path = os.path.join(folder_name, wpvalue)
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f"Successfully downloaded: {wpvalue}")
        else:
            print(f"Failed to download: {wpvalue}. Status code: {response.status_code}")

if __name__ == "__main__":
    game_name = input("Enter the game name (e.g., klbq): ")
    character_name = input("Enter the character name: ")
    language = input("Enter the language (e.g., CN, JP): ")
    end_index = int(input("Enter the end index: "))
    
    # B站登录后的 cookies。一般不需要使用。如果无法下载则需要登录 B站并获取 cookies
    cookies = "your_cookies_here"
    
    download_audio_files(game_name, character_name, language, end_index, cookies)