
from pydub import AudioSegment
import json
import io
import soundfile as sf
import os
from kokoro.pipeline import KPipeline

def generate_audio(script_data):
    pipeline = KPipeline(lang_code="b")
        
    all_audio = []
    for segment in script_data["audio_script"]:
        speaker_id = "am_adam" if segment["speaker"] in ["default", "narrator_male"] else "af_heart"
        audio = pipeline(text=segment["text"], voice=speaker_id, speed=segment["speed"])
        
        # Collect audio chunks
        buffer = io.BytesIO()
        for _, _, chunk in audio:
            sf.write(buffer, chunk, 24000, format='WAV')
        buffer.seek(0)
        all_audio.append(buffer.read())
    
    return all_audio

def merge_audio(audio_path,audio_bytes_list):
    # Create output directory
    # os.makedirs("output_audio", exist_ok=True)
    
    # Save segments locally
    audio_files = []
    for idx, audio_bytes in enumerate(audio_bytes_list):
        output_path = f"{audio_path}/segment_{idx}.wav"
        with open(output_path, "wb") as f:
            f.write(audio_bytes)
        audio_files.append(output_path)
        print(f"Audio file: {idx} successfully saved at : {output_path}")
    
    # Merge audio files (not really needed)
    # master_audio = AudioSegment.empty()
    # for file in audio_files:
    #     master_audio += AudioSegment.from_wav(file)
    
    # Export final file
    # master_output_path = f"{audio_path}/master_output.wav"
    # master_audio.export(master_output_path, format="wav")
    # return master_output_path

def main_generate_audio(script_path,audio_path):
    # Load script data
    with open(script_path) as f:
        script_data = json.load(f)
    
    # Generate audio
    audio_bytes_list = generate_audio(script_data)
    
    # Merge and save final audio
    final_path = merge_audio(audio_path,audio_bytes_list)
    
    print(f"Audio generation complete! Saved as {final_path}")

# if __name__ == "__main__":
#     main_generate_audio(script_path="resources/scripts/script.json",audio_path="resources/audio")