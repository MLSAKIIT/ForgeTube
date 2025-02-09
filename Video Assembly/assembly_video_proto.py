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
import random #for random effects
from moviepy import ImageClip, concatenate_videoclips, AudioFileClip, vfx, afx



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

def create_slideshow_clip(images, audio_clip): #needs testing
    """
    Creates a MoviePy clip by concatenating multiple images with a single audio file.
    
    Each image is shown for an equal duration determined by the total length of the audio.
    
    Parameters:
        images (list): List of image file paths.
        audio_clip (str): clip of the audio
    
    Returns:
        final_clip: Video clip with the concatenated images and audio.
    """
    
    # Determine the duration for each image so that they fill the audio duration equally
    duration_per_image = audio_clip.duration / len(images)
    
    # Create an ImageClip for each image, setting its duration accordingly and concatenate them
    image_clips = [ImageClip(img).set_duration(duration_per_image) for img in images]
    video_clip = concatenate_videoclips(image_clips, method="compose")
    final_clip = video_clip.set_audio(audio_clip)
    
    return final_clip
    
def add_effects(clip):
    """
    Adds a random effect from a curated list to the video clip.
    Parameters:
        clip (VideoClip): Video clip to which effects are to be added.
    Returns:
        VideoClip: Video clip with one random effect applied.
    """
    list_of_effects = [
        # Serious
        [
            vfx.FadeIn(duration=1),
            vfx.FadeOut(duration=1, final_color=(0, 0, 0))
        ],
        # Dramatic
        [
            vfx.CrossFadeIn(duration=1),
            vfx.CrossFadeOut(duration=1)
        ],
        # Smooth transitions
        [
            vfx.SlideIn(duration=1, side="left"),
            vfx.SlideOut(duration=1, side="right")
        ]
    ]
    
    # Choose a random effect from a random category
    random_effect = random.choice(random.choice(list_of_effects))
    return clip.with_effects([random_effect])

def create_video(image_folder, audio_folder,output_file):
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
        clips = []
        
        # Create video clips with image and audio.
        for img, audio in zip(images,audio_files):
            audio_clip = AudioFileClip(audio)
            image_clip = ImageClip(img).with_duration(audio_clip.duration).with_audio(audio_clip)
            image_clip = add_effects(image_clip)
            clips.append(image_clip)
            
        video = concatenate_videoclips(clips, method="compose")
        video.write_videofile(output_file, fps=1)
        print(f"Video created successfully: {output_file}")
        
    except FileNotFoundError:
        if not images:
            raise FileNotFoundError("No images found in the specified folder.")
        if not audio_files:
            raise FileNotFoundError("No audio files found in the specified folder.")
        
        
if __name__ == "__main__":
    image_folder = "Samples/Images/"  
    audio_folder = "Samples/Audio/.wav/"
    # mp4 or .mkv
    output_file = "Samples/Videos/Cats.mp4"
    create_video(image_folder, audio_folder, output_file)
