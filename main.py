from diffusion.scripts.generate_script import VideoScriptGenerator
import json
from diffusion.scripts.generate_image import main_generate_image
from tts.scripts.generate_audio import main_generate_audio
from assembly.scripts.assembly_video import create_video,create_complete_srt,extract_topic_from_json
'''
TODO: 1. Make a main.py where all pipelines are invoked at once.
TODO: 2. Take the prompt for the video as user input.
TODO: 3. Run Tests with various different prompts.
TODO: 4. All gpu related tasks must be performed on modal.
'''
if __name__ == "__main__":
    # Update folder paths as needed.
    script_path = "resources/scripts/script.json"
    images_path = "resources/images/"
    audio_path = "resources/audio/"
    font_path = "Samples/font/font.ttf"
    
    # 1. Generate the Script
    generator = VideoScriptGenerator(api_key="Enter your gemini api key", serp_api_key="enter your serp api key")
    
    try:
        topic = input("Enter the topic of the video : "),
        duration=int(input("Enter the video duration in seconds : "))
        input_string = input("Enter a list of key points separated by commas : ")
        key_points = input_string.split(",") 
        # Remove leading/trailing whitespace from each word (important!)
        key_points = [word.strip() for word in key_points]
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
    except Exception as e:
        print(f"Script generation failed: {str(e)}")
        
    # 2. Generate the images
    main_generate_image(script_path,images_path)
    
    # 3. Generate the audio 
    main_generate_audio(script_path)
    
    # 4. Video Assembly
    topic = extract_topic_from_json(script_path)
    sub_output_file = f"resources/subtitles/{topic}.srt"
    video_file = f"resources/Videos/{topic}.mp4"
    
    create_complete_srt(script_folder = script_path,
                        audio_file_folder = audio_path,
                        outfile_path = sub_output_file,
                        chunk_size = 10)
    
    create_video(images_path, audio_path, script_path, font_path, video_file, with_subtitles=True)
