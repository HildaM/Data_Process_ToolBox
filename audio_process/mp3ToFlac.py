# Python program to convert MP3 to FLAC

import os
from pydub import AudioSegment

def convert_mp3_to_flac(mp3_file_path):
    # Check if the file exists
    if not os.path.exists(mp3_file_path):
        print("File does not exist.")
        return
    
    # Extract the file path and name without extension
    file_path_without_extension = os.path.splitext(mp3_file_path)[0]
    
    # Define the output FLAC file path
    flac_file_path = f"{file_path_without_extension}.flac"
    
    # Convert MP3 to FLAC
    audio = AudioSegment.from_mp3(mp3_file_path)
    audio.export(flac_file_path, format="flac")
    
    print(f"Converted {mp3_file_path} to {flac_file_path}")

# Example usage
if __name__ == "__main__":
    mp3_file_path = input("Enter the path of the MP3 file: ")
    convert_mp3_to_flac(mp3_file_path)
