import os
from pydub import AudioSegment
from pathlib import Path

def convert_mp3_to_wav(mp3_file_path, output_folder):
    # Extract the file name without extension
    file_name = os.path.basename(mp3_file_path)
    file_name_without_extension = os.path.splitext(file_name)[0]
    
    # Define the output WAV file path
    wav_file_path = os.path.join(output_folder, f"{file_name_without_extension}.wav")
    
    # Convert MP3 to WAV
    audio = AudioSegment.from_mp3(mp3_file_path)
    audio.export(wav_file_path, format="wav")
    
    print(f"Converted {mp3_file_path} to {wav_file_path}")

def batch_convert_mp3_to_wav(input_folder):
    # Create output folder
    output_folder = os.path.join(os.path.dirname(input_folder), f"{os.path.basename(input_folder)}_wav")
    os.makedirs(output_folder, exist_ok=True)
    
    # Get all MP3 files in the input folder
    mp3_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.mp3')]
    
    # Convert each MP3 file to WAV
    for mp3_file in mp3_files:
        mp3_file_path = os.path.join(input_folder, mp3_file)
        convert_mp3_to_wav(mp3_file_path, output_folder)
    
    print(f"\nAll MP3 files have been converted to WAV and saved in: {output_folder}")

if __name__ == "__main__":
    input_folder = input("Enter the path of the folder containing MP3 files: ")
    
    # Validate input folder
    if not os.path.isdir(input_folder):
        print("Error: The specified folder does not exist.")
    else:
        batch_convert_mp3_to_wav(input_folder)