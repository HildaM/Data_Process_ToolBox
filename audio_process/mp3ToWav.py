# Python program to convert MP3 to WAV

import os
from pydub import AudioSegment

def convert_mp3_to_wav(mp3_file_path):
    # Check if the file exists
    if not os.path.exists(mp3_file_path):
        print("File does not exist.")
        return
    
    # Extract the file path and name without extension
    file_path_without_extension = os.path.splitext(mp3_file_path)[0]
    
    # Define the output WAV file path
    wav_file_path = f"{file_path_without_extension}.wav"
    
    # Convert MP3 to WAV
    audio = AudioSegment.from_mp3(mp3_file_path)
    audio.export(wav_file_path, format="wav")
    
    print(f"Converted {mp3_file_path} to {wav_file_path}")

# Example usage
if __name__ == "__main__":
    mp3_file_path = input("Enter the path of the MP3 file: ")
    convert_mp3_to_wav(mp3_file_path)
