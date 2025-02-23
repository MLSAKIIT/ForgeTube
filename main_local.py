from diffusion.scripts.generate_script import VideoScriptGenerator
import json
from diffusion.scripts.generate_image_local import main_generate_image
from tts.scripts.generate_audio import main_generate_audio
from assembly.scripts.assembly_video import create_video,create_complete_srt,extract_topic_from_json
import os
'''
TODO: 1. Make a main.py where all pipelines are invoked at once.
TODO: 2. Take the prompt for the video as user input. 
TODO: 3. Run Tests with various different prompts. 
TODO: 4. All gpu related tasks must be performed on modal. Works
'''
if __name__ == "__main__":
    script_path = "resources/scripts/" # creates the folders if not made already
    images_path = "resources/images/"
    audio_path = "resources/audio/"
    font_path = "resources/font/font.ttf"
    
    def create_or_check_folder(folder_path):
        """
        Creates a folder if it doesn't exist.
        If folder exists, checks for files and raises FileExistsError if any are found.
        
        Args:
            folder_path (str): Path to the folder
        
        Raises:
            FileExistsError: If folder exists and contains files
        """
        # If folder doesn't exist, create it
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Created Folder: {folder_path}")
        else:
            # Check if folder has any contents
            if any(os.listdir(folder_path)):
                raise FileExistsError(f"Folder : '{folder_path}' already exists and contains files. Please remove them or make a new folder")
            # print(f"folder '{folder_path}' exists but is empty")
    
    create_or_check_folder(images_path)
    create_or_check_folder(audio_path)
    create_or_check_folder(script_path)
    
    # 1. Generate the Script
    gem_api = "Enter your Gemini API Key here"
    serp_api = "Enter your Serp API key here"
    if (not gem_api) or (not serp_api):
        raise ValueError("API Key not provided !\n Please Create your api key at : \n Serp APi : https://serpapi.com \n Gemini API : https://aistudio.google.com/apikey")
    generator = VideoScriptGenerator(api_key=gem_api,serp_api_key=serp_api)
    
    try:
        topic = input("Enter the topic of the video : "),
        duration=int(input("Enter the video duration in seconds : "))
        input_string = input("Enter a list of key points separated by commas : ")
        key_points = input_string.split(",") 
        key_points = [word.strip() for word in key_points]
        print("Starting Script Generation ... ")
        script = generator.generate_script(
            # topic="Neural Networks in Medical Imaging",
            # duration=90,
            # key_points=["Diagnosis accuracy", "Pattern recognition", "Case studies"]
            topic,duration,key_points
        )
        print("Initial Script: ")
        print(json.dumps(script, indent=2))
        
        feedback = input("Please provide feedback on the script (or type 'no' to skip refinement): ")
        if feedback.lower() != "no":
            refined_script = generator.refine_script(script, feedback)
            print("\nRefined Script:")
            print(json.dumps(refined_script, indent=2))
            generator.save_script(refined_script, script_path)
        else:
            generator.save_script(script, script_path)
            print("Script Generation Done.")
    except Exception as e:
        print(f"Script generation failed: {str(e)}")
        
    # 2. Generate the images
    print("Staring Image Generation ...")
    main_generate_image(script_path,images_path)
    print("Image Generation Done.")
    
    # 3. Generate the audio 
    print("Starting Audio Generation ...")
    main_generate_audio(script_path,audio_path)
    print("Audio Generation Done.")
    # Video Assembly
    topic = extract_topic_from_json(script_path)
    topic = "_".join(topic.split(' ')[:1])
    sub_output_file = f"{topic}.srt"
    video_file = f"{topic}.mp4"
    
    # 5. Create subtitles in a .srt file
    print("Creating .srt subtitle file")
    create_complete_srt(script_folder = script_path,
                        audio_file_folder = audio_path,
                        outfile_path = sub_output_file,
                        chunk_size = 10)
    
    # 6. Start Video Assembly
    print("Starting video assembly ...")
    create_video(images_path, audio_path, script_path, font_path, video_file, with_subtitles=True)
