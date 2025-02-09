''' 
README : The video assembler takes all the images in the Images folder and all the audio files in the Audio folder and concatenates 
them into a video. The duration of the picture displayed is same as the duration of the audio for that image. The Images and
Audio files sorted alphabetically and then compiled in that order. It is recommended to store the Audio and Image files by 
numbering them.

Moviepy also supports addition of video clips, so if in future if we have access to video generation it will be useful.

'''
''' MAIN TODO
1. TODO: Implement Subtitles.
2. TODO: Read json and extract important parameters from it. 
3. TODO: Add support for video clips as well. 
4. TODO: Add the ability to compile multiple images (stored in a folder) for the one audio stream into a single clip. (Shopno )
5. TODO: Add transition from clip to clip.
'''
'''
Additional TODOs
# TODO: 1. Add a small delay to ensure smoother transition from clip to clip.
# TODO: 2. Experiment with adding Title screen, text and transitions, and other effects.
# TODO  3. Test the script against a large number of images with higher resolutions and audio files, document the performance.
# TODO: 4. Test the script with various different audio and video extensions and codecs, find the best combination.
# WARNING: No testing has been done with .png and .wav audio file formats.
# TODO: 5. Allow the script to automatically assign the proper codec with the respective file extension.
# TODO: 6. Run proper tests to document when video compiler corruption happens.
'''
import os
from moviepy import ImageClip, concatenate_videoclips, AudioFileClip,TextClip,CompositeVideoClip

import json
from datetime import datetime, timedelta

# Function to Read all the files from a folder.
def get_files(folder, extensions):
    """
    Retrieves files with specified extensions from a folder.
    Parameters:
        folder (str): Path to the folder.
        extensions (tuple): File extensions to include (e.g., ('.jpg', '.png')).
    Returns:
        list: List of file paths.
    """
    return [
        os.path.join(folder, file)
        # Files are numbered , so that after sorting they are compiled into the video in that order.
        for file in sorted(os.listdir(folder))  
        if file.lower().endswith(extensions)
    ]

def create_video(image_folder, audio_folder,sub_folder,font_path ,output_file):
    """
    Combines images from a folder and audio files from another folder into a video.
    Parameters:
        image_folder (str): Path to the folder containing images.
        audio_folder (str): Path to the folder containing audio files.
        output_file (str): Name of the output video file.
    """
    try:
        images = get_files(image_folder, ('.jpg', '.png'))
        audio_files = get_files(audio_folder, ('.mp3', '.wav'))
        sub_files = get_files(sub_folder,(".txt"))
        vid_clips = []
        for img, audio in zip(images, audio_files):
            audio_clip = AudioFileClip(audio)
            image_clip = ImageClip(img).with_duration(audio_clip.duration).with_audio(audio_clip)
            vid_clips.append(image_clip)
        # Compose method automatically resizes images by adding the image with the largest dimension as the default and 
        # adding black bars to fill to fil the rest of the images.
        

# Subtitles 
        subtitles = []
        sub_duration = audio_clip.duration / len(sub_files) if sub_files else 2  # Adjust timing

        for i, text_file in enumerate(sub_files):
            with open(text_file, "r") as f:
                subtitle = f.read().strip()
            subtitle_clip = TextClip(text=subtitle,font=font_path, font_size=50, color='white', bg_color='black', size=(800, 100))
            subtitle_clip = subtitle_clip.with_position(("center", "bottom")).with_duration(sub_duration).with_start(i * sub_duration)
            subtitles.append(subtitle_clip)
        # video = concatenate_videoclips(vid_clips, method="compose")
        clips = []
        for i in range(len(vid_clips)):
            if i ==  0:
                clips.append(vid_clips[i].with_start(vid_clips[i].start).with_end(vid_clips[i].end))
                clips.append(subtitles[i].with_start(vid_clips[i].start).with_end(vid_clips[i].end))
            else:
                clips.append(vid_clips[i])
                clips.append(subtitles[i].with_start(vid_clips[i-1].end).with_end(vid_clips[i].start))
        video = CompositeVideoClip(clips)
        # video = concatenate_videoclips(clips)            
        video.write_videofile(output_file, fps=24)
        print(f"Video created successfully: {output_file}")
        
    except FileNotFoundError:
        if not images:
            print("No images found in the specified folder.")
        if not audio_files:
            raise FileNotFoundError("No audio files found in the specified folder.")
        if not subtitles:
            raise FileNotFoundError("No subtile found in the specified folder. ")
        
# Function to read JSON from a file and extract important parameters
def extract_audio_visual_from_json(file_path):
    try:
        # Open the JSON file
        with open(file_path, 'r') as file:
            # Load JSON data from the file
            data = json.load(file)
            
            # Extract the audio_script and visual_script
            audio_script = data.get('audio_script', [])
            visual_script = data.get('visual_script', [])
            
            return audio_script, visual_script
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} contains invalid JSON.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Calculating the end timestamp of the subtitle
def calculate_endtimestamp(start_time, duration):
    start_dt = datetime.strptime(start_time, "%M:%S")
    end_dt = start_dt + timedelta(seconds=duration)
    return end_dt.strftime("%M:%S")

# Calculating the duration of the subtitle
def calculate_duration(text, speed):
    words_per_minute = 150  # Average speaking rate
    words = len(text.split())
    duration = (words / words_per_minute) * 60 / speed
    return duration
        
if __name__ == "__main__":
    image_folder = "samples/Images"  
    audio_folder = "samples/Audio/.wav"  
    sub_folder = "samples/subtitles"
    font_path = "Samples/font/font.ttf"
    # mp4 or .mkv
    output_file = "samples/Cats.mp4"
    # create_video(image_folder, audio_folder,sub_folder,font_path, output_file)

    # Extract parameters from json file
    json_path = "samples/templates/mock_script.json"
    audio_script, visual_script = extract_audio_visual_from_json(json_path)

    if audio_script:
        # print("Extracted Audio Parameters:")
        audio_data = []
        for item in audio_script:
            if 'text' in item and 'timestamp' in item:
                text = item['text']
                timestamp = item['timestamp']
                speed = item['speed']
                duration = calculate_duration(text, speed)
                endtimestamp = calculate_endtimestamp(timestamp, duration)
                audio_data.append([text, timestamp, endtimestamp])
                # print(f"Text: {text}, Start: {timestamp}, End: {endtimestamp}")

        # Print the 2D array
        print("2D Array of Audio Data:")
        for row in audio_data:
            print(row)
    
    else:
        print("No audio parameters found in the JSON file.")