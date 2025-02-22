''' 
README : The video assembler takes all the images in the Images folder and all the audio files in the Audio folder and the text-to-script from json file and concatenates 
them into a video. The duration of the picture displayed is same as the duration of the audio for that image. The Images and
Audio files sorted alphabetically and then compiled in that order. It is recommended to store the Audio and Image files by 
numbering them.
'''
''' MAIN THINGS TODO
1. TODO: Main Video Assembly Engine (Done by Souryabrata)
2. TODO: Implement Subtitles, via video embedding and .srt file generation. (Done by Souryabrata)
3. TODO: Read json and extract important parameters from it. (Done by Rahul)
4. TODO: Add support for video clips as well. (Assigned to Shopno)
5. TODO: Add the ability to compile multiple images (stored in a folder) for the one audio stream into a single clip. (Assigned to Shopno )
6. TODO: Add transition from clip to clip. (Done by Shopno)
7. TODO Add an intro and outro clip. Intro Clip contains : Video title / Short description (Done by Shopno).
Outro Clip contains a text "Made by ForgeTube team", MLSA Logo, Github Link to ForgeTube Main Page.
'''
'''
Additional TODOs
TODO: 1. Add a small delay to ensure smoother transition from clip to clip. (Assigned to Shopno)
TODO: 2. Experiment with adding Title screen, text and transitions, and other effects. (Assigned to Nancy)
TODO  3. Test the script against a large number of images with higher resolutions and audio files, document the performance.
TODO: 4. Test the script with various different audio and video extensions and codecs, find the best combination. 
TODO: 5. Allow the script to automatically assign the proper codec with the respective file extension.
TODO: 6. Run proper tests to document when video compiler corruption happens.
'''
import os
from moviepy import ImageClip, concatenate_videoclips, AudioFileClip,TextClip,CompositeVideoClip,vfx
import pysrt 
import json

def check_file_exists(file_path):
    """Check if a file exists at the specified path."""
    if os.path.isfile(file_path):
        return True
    else:
        raise FileNotFoundError(f"File not found: {file_path}")
    
def check_folder_exists(folder_path):
    '''Checks if a folder path is valid. '''
    if os.path.isdir(folder_path):
        return True
    else:
        raise FileNotFoundError(f"Folder not found at {folder_path}")
    
def get_files(folder, extensions):
    """
    Retrieves files with specified extensions from a folder.
    Parameters:
        folder (str): Path to the folder.
        extensions (tuple): File extensions to include (e.g., ('.jpg', '.png')).
    Returns:
        list: List of file paths.
    """
    if os.path.isdir(folder):
        return [
            os.path.join(folder, file)
            # Files are numbered , so that after sorting they are compiled into the video in that order.
            for file in sorted(os.listdir(folder),key=lambda x: int(x.split('_')[1].split('.')[0]))  
            if file.lower().endswith(extensions)
        ]
    else:
        raise OSError(f"{folder} not found.")


'''
FIXME Subtitles timings are same and not correct.
FIX Create a single srt file with the correct duration of all the subtitles paired with the respective audio file.
'''
def create_srt(text :str,
            audio_file : AudioFileClip, 
            outfile_name:str,
            duration:int,
            chunk_size=5):
    '''
    Function is deprecated, will rename the create_complete_srt into create srt
    Original task was to take a .txt file, read the text , split the text into the specified chunk_size
    Create a srt file with the given text chunks and the appropriate duration of the text.
    WARNING: Caused problems after json extract was implemented.
    '''
    # with open(text_file, "r") as file:
    #     words = file.read().split()
    words = text.split()
    chars = " ".join(words)
    chars_count = len(chars)
    word_count = len(words)
    # word_duration = audio_file.duration / word_count #seconds per word
    char_duration = audio_file.duration / chars_count #seconds per character
    # Generate subtitle file
    subs = pysrt.SubRipFile()
    start_time = duration 
    # Automatic chunk_size calculation
    # target_duration = 2 # Number of seconds the subtitle is displayed on the screen
    # chunk_size = round(target_duration/word_duration)
    
    

    for i in range(0, word_count, chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        end_time = start_time + (len(chunk) * char_duration)  

        subtitle = pysrt.SubRipItem(index=len(subs) + 1,
                                    start=pysrt.SubRipTime(seconds=start_time),
                                    end=pysrt.SubRipTime(seconds=end_time),
                                    text=chunk)

        subs.append(subtitle)
        start_time = end_time  

    out = f"samples/subtitles/.srt/{outfile_name}.srt"
    subs.save(out)
    return out


def extract_topic_from_json(file_path):
    '''
    extract_topic_from_json extract() takes json file path as input.
    - Opens the file as read-only and loads the JSON data from it.
    - Extracts the topic from the JSON data.

    On success, it returns the topic of the video.
    '''
    try:
        # Open the JSON file
        with open(file_path, 'r') as file:
            # Load JSON data from the file
            data = json.load(file)
            
            # Extract the topic, and audio_script from the JSON data
            topic = data.get('topic', 'No topic found')
            
            return topic
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} contains invalid JSON.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def extract_audio_from_json(file_path):
    '''
    extract_audio_topic_from_json() takes json file path as input.
    - Opens the file as read-only and loads the JSON data from it.
    - Extracts the audio_script from the JSON data.

    On success, it returns audio_script.
    '''
    try:
        # Open the JSON file
        with open(file_path, 'r') as file:
            # Load JSON data from the file
            data = json.load(file)
            
            # Extract the topic, audio_script and visual_script
            topic = data.get('topic', 'No topic found')
            audio_script = data.get('audio_script', [])
            # visual_script = data.get('visual_script', [])

            return audio_script
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} contains invalid JSON.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def json_extract(json_path):
    '''
    json_extract() takes json file path as input.
    - Calls the extract_audio_from_json() to extract the text-to-speech / subtitles from the json file,
    and the topic of the video.

    On success, it returns the subtitles in list format, and the topic.
    '''
    
    # Extract parameters from json file
    audio_script = extract_audio_from_json(json_path)
    if audio_script:
        # print("Extracted Audio Parameters:")
        audio_data = []
        for item in audio_script:
            if 'text' in item:
                text = item['text']
                audio_data.append(text)
        return audio_data
    else:
        raise FileNotFoundError("No audio script found in the JSON file.")
    

def add_effects(clip):
    """
    Adds a effect from a curated list to the video clip.
    Parameters:
        clip (VideoClip): Video clip to which effects are to be added.
    Returns:
        VideoClip: Video clip with one effect applied.
    """
    random_effect =[vfx.FadeIn(duration=1),vfx.FadeOut(duration=1)]    
    # print(random_effect)
    return clip.with_effects(random_effect)


def create_intro_clip(background_image_path, 
                    duration, 
                    topic,
                    font_path):
    """
    Create an intro video clip with a background image and centered text.

    Parameters:
        background_image_path (str): Path to the background image.
        duration (int or float): Duration of the clip in seconds.
        topic (str): The text to display. Defaults to "Welcome to My Video!".
        font_path (str): Path to the TrueType font file.
        font_size (int): Size of the text font.
        text_color (str): Color of the text.

    Returns:
        VideoClip: A composite video clip with the background and centered text.
    """
    check_file_exists(background_image_path)
    # Create an ImageClip for the background image
    background = ImageClip(background_image_path, duration=duration)

    # Create a TextClip for the intro text
    text_clip = TextClip(text=topic,
                        size=(900, 90),
                        method='caption',
                        color="white",
                        font=font_path)

    # Position the text in the center and set its duration to match the background
    text_clip = text_clip.with_position("center").with_duration(duration)

    # Overlay the text clip on top of the background image
    final_clip = CompositeVideoClip([background, text_clip])
    
    return final_clip


def create_video(image_folder :str, 
                audio_folder : str,
                script_path : str,
                font_path : str ,
                output_file : str,
                with_subtitles :bool = False):
    """
    Main function that creates the video. The function works in 3 parts:
    1. Checks if the given parameters are correct.
    2. if `with_subtitle` flags is set to `False`, creates a video with the images and audio in the given folders.
    Each image is displayed with the same duration as the corresponding audio file.
    3. if the `with_subtitle` flag is set to `True` embeds subtitles within the video itself, cannot be turned off in video players.
    
    Video is compiled using the `compose` method so that if the images are of different aspect ratios /resolutions then the video takes 
    the image with the largest resolution or aspect ratio as the default one and puts black bars with the rest of the non-fitting images
    Args:
        image_folder (str) : Path to the folder containing images.
        audio_folder (str) : Path to the folder containing audio files.
        script_path (str)   : Path to the file containing the script.
        font_path (str)    : Path to of the Font File, must be a True type or an Open Type Font
        output_file (str)  : Name of the output video file, a path can also be given.
        with_subtitles (bool) : When set to `true` embeds the subtitles in the video.
    Raises:
        FileNotFoundError: If images, audio or subtitles are not detected.
    """
    check_folder_exists(image_folder)
    check_folder_exists(audio_folder)
    check_file_exists(script_path)
    check_file_exists(font_path)
    
    images = get_files(image_folder, ('.jpg', '.png'))
    audio_files = get_files(audio_folder, ('.mp3', '.wav'))
    subtitles = json_extract(script_path)
    raw_clips = []
    audio_durations = []
    Start_duration = 0
    
    # Creating the intro clip and appending it to raw clips
    
    path_to_background = "resources/Intro/intro.jpg"
    check_file_exists(path_to_background)
    check_file_exists(font_path)
    topic = extract_topic_from_json(script_path)
    intro_clip = create_intro_clip(path_to_background, duration=5, topic=topic, font_path=font_path)
    raw_clips.append(intro_clip)
    
    # Create different clips with audio
    for img, audio in zip(images,audio_files):
        audio_clip = AudioFileClip(audio)
        image_clip = ImageClip(img).with_duration(audio_clip.duration).with_audio(audio_clip)
        # Debug Text for subtitle synchronisation:
        # print(f"Start : {Start_duration}")
        # print(f"End : {audio_clip.duration+Start_duration}")
        audio_durations.append(audio_clip.duration)
        print(f"Video Clip no. {images.index(img)+1} successfully created")
        Start_duration += audio_clip.duration
        image_clip = add_effects(image_clip)
        raw_clips.append(image_clip)            
    
    #creating the outro clip appending it to raw clips  
    outro_text = "Thank you for watching! Made by ForgeTube team."
    outro_clip = create_intro_clip(path_to_background, duration=5, topic=outro_text, font_path=font_path)
    raw_clips.append(outro_clip)
    #     Store individual clips without subtitles for preview / debug 
    #     clip = None
    #     clip = CompositeVideoClip(img)
    #     clip.write_videofile(f"samples/raw/{raw_clips.index(image_clip)+1}.mp4",fps = 1,threads = os.cpu_count())
    
    video = concatenate_videoclips(raw_clips, method="compose")
    
    '''
    The following part of the code fixes all the below mentioned issues and their following fixes :
    FIXME: 1. Subtitles are not properly synchronised with the audio.
    FIX: Each subtitle text is paired with the corresponding audio. Duration of the text is kept same as the duration of the audio.
    FIXME: 2. If the entire text is shown at once, then it doesn't fit.
    FIX: Allows a maximum number of 10 words to be shown at once, rest of the text is divided into chunks, each chunk is set to an
    equivalent duration.
    Where duration of the chunk = Total duration of the audio * (Chunk_Size / Total Number of words)
    WARNING: Due to some rounding errors and division errors with floats, some chunks are not perfectly synchronised.         
    FIXME 3. Subtitles do not appear at the right position in the video. Preferable position is Vertical : bottom, Horizontal = Center,
    FIX : `SubtitleClip` was causing problems so, used `TextClip` instead.
    FIXME 4. When subtitles were added to each clip one by one, and all clips later concatenated, an error occurred if images were 
    of different dimensions, where the aspect ratio of the final video was messed up.
    FIX: Make it such that concatenation is done only on the image clips and composite video clip is added later on with the 
    '''
    if with_subtitles == True:
        Start_duration = 5
        subtitle_clips = []
        chunk = ''
        chunks = []
        chunk_duration = 0
        chunk_durations = []
        chunk_size = 10
        for text,duration in zip(subtitles,audio_durations):
            words = text.split()
            if len(words) > chunk_size:
                for i in range(0,len(words),chunk_size):
                    chunk = " ".join(words[i : (i+chunk_size if i < len(words)-1 else len(words)-1)])
                    chunks.append(chunk)
                    chunk_duration = duration * (len(chunk.split())/len(words))
                    chunk_durations.append(chunk_duration)
            else:
                chunks.append(text)
                chunk_durations.append(duration)
        # For Debugging:
        # for i in chunks:
            # print(f"Index :{chunks.index(i)}, Text: {i}, Word Count: {len(i.split())}")
        # print(chunk_durations)
        for subtitle,duration in zip(chunks,chunk_durations):
            subtitle_clip=TextClip(text=subtitle,
                                    font=font_path, 
                                    color='white', 
                                    bg_color='black', 
                                    size=(1000, 100),
                                    method='caption',
                                    text_align = "center",
                                    horizontal_align = "center"
                                    ).with_duration(duration).with_start(Start_duration).with_position('bottom')
            subtitle_clips.append(subtitle_clip)
            # For Debugging :
            # print(f"Subtitle Clip no. {chunks.index(subtitle)+1} successfully created")
            Start_duration += duration
        subtitle_clips.insert(0,video)
        final_video = CompositeVideoClip(subtitle_clips)
    else:
        final_video = video
    final_video.write_videofile(output_file, fps=24,threads = os.cpu_count())
    print(f"Video created successfully: {output_file}")
        
    # except FileNotFoundError:
    #     if not images:
    #         raise FileNotFoundError("No images found in the specified folder.")
    #     if not audio_files:
    #         raise FileNotFoundError("No audio files found in the specified folder.")
    #     if not subtitles:
    #         raise FileNotFoundError("No subtitles found in the specified json. ")
        
        
def create_complete_srt(script_folder :str, 
            audio_file_folder : str, 
            outfile_path:str,
            chunk_size=10):
    """
    Creates an SRT file by extracting subtitles from the script_folder using `json_extract` function and audio files 
    from the `audio_file` folder. Segments the subtitles into the specified chunk size and maps the duration of the chunk to the 
    proportion of the length of the chunk.
    Parameters:
    script_folder (str): Path to the folder containing script json file.
    audio_file_folder (str): Path to the folder containing audio files.
    outfile_path (str): Path or Name of the SRT file given in output.
    chunk_size (str): Number of words per subtitle chunk.
    """
    
    script = json_extract(script_folder)
    audio_files = get_files(audio_file_folder,(".wav",".mp3"))
    audio_clips = []
    [audio_clips.append(AudioFileClip(x)) for x in audio_files]
    subs = pysrt.SubRipFile()
    start_time = 5 
    chunk = ''
    chunk_duration = 0
    end_time = 5
    n = 1
    for text,audio_clip in zip(script,audio_clips):
        duration = audio_clip.duration
        words = text.split()
        if len(words) > chunk_size:
            for i in range(0,len(words),chunk_size):
                chunk = " ".join(words[i : (i+chunk_size if i < len(words)-1 else len(words)-1)])
                chunk_duration = duration * (len(chunk.split())/len(words))
                end_time += chunk_duration
                subtitle = pysrt.SubRipItem(
                    index=n,
                    start=pysrt.SubRipTime(seconds=start_time),
                    end=pysrt.SubRipTime(seconds=end_time),
                    text=chunk
                )
                subs.append(subtitle)
                # For Debugging:
                # print(f"Subtitle no. {n} added successfully.")
                # print(f"Start : {start_time}")
                # print(f"End : {end_time}")
                start_time = end_time
                n+=1
        else:
            chunk = text
            chunk_duration = duration
            end_time += chunk_duration
            subtitle = pysrt.SubRipItem(
                index=len(subs) + 1,
                start=pysrt.SubRipTime(seconds=start_time),
                end=pysrt.SubRipTime(seconds=end_time),
                text=chunk
            )
            subs.append(subtitle)
            # For Debugging:
            # print(f"Subtitle no. {n} added successfully.")
            # print(f"Start : {start_time}")
            # print(f"End : {end_time}")
            start_time = end_time
            n+=1
            
    subs.save(outfile_path)
    print(f"File saved successfully at {outfile_path}")

        
if __name__ == "__main__":
    image_folder = "resources/images/"  
    audio_folder = "resources/Audio/"  
    script_path = "resources/scripts/script.json" 
    font_path = "resources/font/font.ttf"
    sub_output_file = "The.srt"
    topic = extract_topic_from_json(script_path)
    output_file = f"The.mp4"
    
    create_complete_srt(script_folder=script_path,
                        audio_file_folder=audio_folder,
                        outfile_path=sub_output_file,
                        chunk_size = 10)
    
    create_video(image_folder, audio_folder,script_path,font_path, output_file,with_subtitles=True)
    
