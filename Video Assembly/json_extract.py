import json
from datetime import datetime, timedelta

# Function to read audio and JSON from a file and extract important parameters
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
        
def json_extract(json_path):
    
    # Extract parameters from json file
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
        return audio_data
    else:
        return "No audio parameters found in the JSON file."