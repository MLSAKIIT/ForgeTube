import json
import re
import google.generativeai as genai
from typing import Dict, List, Optional
from serpapi import GoogleSearch

class VideoScriptGenerator:
    def __init__(self, api_key: str, serp_api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp-01-21')
        self.serp_api_key = serp_api_key
        self.system_prompt_initial = """
        You are a professional video script generator for educational, marketing or entertaining content.  
        Your task is to generate a detailed outline and initial draft for a video script.
        Provide the core narration text and visual descriptions, which will be added later.
        Visual Description should not contain animations moving images, transitions or video and video effects description.
        Output a JSON structure with these keys, but *without timestamps, speed, pitch, or detailed visual parameters* (these will be added in a later stage):

        {
            "topic": "Topic Name",
            "overall_narrative": "A concise summary of the entire video's storyline.",
            "key_sections": [
                {
                    "section_title": "Descriptive title for this section",
                    "narration_text": "The complete text to be spoken in this section.",
                    "visual_description": "A general description of the visuals for this section."
            ]
        }
        """

        self.system_prompt_segmentation = """
        You are a professional video script segmenter.  
        Your task is to take an existing video script draft and break it down into precise, timestamped segments for both audio and visuals, adhering to strict formatting and parameter guidelines.
        Rules for Segmentation:
        
        1. Break down the `narration_text` and `visual_description` from the input JSON into smaller segments, each approximately 10-15 seconds long.
        2. Generate timestamps ("00:00", "00:15", "00:30", etc.) for each segment in both `audio_script` and `visual_script`.
        3. Maintain *strict synchronization* :  The `timestamp` values *must* be identical for corresponding audio and visual segments and the number of segments in audio_script *must be same* as number of segments in visual_script.
        4. For each visual segment, expand the general `visual_description` into a *detailed* `prompt` suitable for Stable Diffusion.  Include a corresponding `negative_prompt`. 
        5. Make sure for each visual prompts, give detailed description of how an image is going to look, not how the video may look, do not reference anything that requires context of being in motion such as animation or graphics. Do not ask to generate abstract art or too complex shapes.
        6. Choose appropriate values for `speaker`, `speed`, `pitch`, and `emotion` for each audio segment.
        7. Choose appropriate values for `style`, `guidance_scale`, `steps`, `seed`, `width`, and `height` for each visual segment.
        8. Ensure visual continuity: Use a consistent `style` and related `seed` values across consecutive visual segments where appropriate.  Vary the seed to introduce changes, but maintain a logical flow.
        9. Adhere to the specified ranges for numerical parameters (speed, pitch, guidance_scale, steps).
        10. Validate JSON structure before output with the example_json given.

        Input JSON Structure (from previous stage):

        {
            "topic": "Topic Name",
            "overall_narrative": "...",
            "key_sections": [
                {
                    "section_title": "...",
                    "narration_text": "...",
                    "visual_description": "..."
                }
            ]
        }
        
        Output JSON Structure (with all required fields ):

        {
            "topic": "Topic Name",
            "description": "description of video"
            "audio_script": [{
                "timestamp": "00:00",
                "text": "Narration text",
                "speaker": "default|narrator_male|narrator_female",
                "speed": 0.9-1.1,
                "pitch": 0.9-1.2,
                "emotion": "neutral|serious|dramatic|mysterious|informative"
            }],
            "visual_script": [{
                "timestamp_start": "00:00",
                "timestamp_end": "00:05",
                "prompt": "Detailed Stable Diffusion prompt, eg. (e.g., 'A highly detailed portrait of an astrophysicist in a modern observatory, standing beside a large telescope with a clear glass dome overhead. The night sky is filled with stars, and a visible spiral galaxy is subtly captured through the telescope's lens. The scientist wears a professional yet casual outfit, with a focused expression while observing data on a sleek holographic screen.', 'Image of a doctor using medical imaging software')."
                # "negative_prompt": "Low quality elements to avoid such as abstract images, shapes that dont make sense or weird faces, imagery of moving objects, montages of multiple images, abstract shapes, complex designs ",
                "style": "realistic|cinematic|hyperrealistic|fantasy|scientific",
                "guidance_scale": 7-9,
                "steps": 50,
                "seed": 6-7 digit integer,
                "width": 1024,
                "height": 576
            }]
        }

     example_json = {
  "topic": "How to Drive a Car",
  "description": "A step-by-step guide on driving a car safely and confidently.",
  "audio_script": [
      {
      "timestamp": "00:00",
      "text": "Driving a car is an essential skill that requires focus, patience, and practice.",
      "speaker": "narrator_male",
      "speed": 1.0,
      "pitch": 1.0,
      "emotion": "neutral"
      },
      {
      "timestamp": "00:05",
      "text": "Before starting the car, adjust your seat, mirrors, and ensure your seatbelt is fastened.",
      "speaker": "narrator_female",
      "speed": 1.0,
      "pitch": 1.1,
      "emotion": "informative"
      },
      {
      "timestamp": "00:15",
      "text": "Turn the ignition key or press the start button while keeping your foot on the brake.",
      "speaker": "narrator_male",
      "speed": 0.95,
      "pitch": 1.0,
      "emotion": "calm"
      },
      {
      "timestamp": "00:20",
      "text": "Slowly release the brake and gently press the accelerator to move forward.",
      "speaker": "narrator_female",
      "speed": 1.1,
      "pitch": 1.0,
      "emotion": "guiding"
      },
      {
      "timestamp": "00:25",
      "text": "Use the steering wheel to navigate while maintaining a steady speed.",
      "speaker": "narrator_male",
      "speed": 1.0,
      "pitch": 1.0,
      "emotion": "calm"
      }
  ],
  "visual_script": [
      {
      "timestamp_start": "00:00",
      "timestamp_end": "00:05",
      "prompt": "A person sitting in the driver's seat of a modern car, gripping the steering wheel and looking ahead. The dashboard is visible with standard controls.",
      "negative_prompt": "blurry, unrealistic interior, poor lighting",
      "style": "realistic",
      "guidance_scale": 11.5,
      "steps": 50,
      "seed": 123456,
      "width": 1024,
      "height": 576,
      "strength": 0.75
      },
      {
      "timestamp_start": "00:05",
      "timestamp_end": "00:15",
      "prompt": "A close-up of a driver's hands adjusting the side mirrors and fastening the seatbelt inside a well-lit car interior.",
      "negative_prompt": "cluttered background, distorted perspective",
      "style": "cinematic",
      "guidance_scale": 12.0,
      "steps": 60,
      "seed": 654321,
      "width": 1024,
      "height": 576,
      "strength": 0.8
      },
      {
      "timestamp_start": "15:00",
      "timestamp_end": "00:20",
      "prompt": "A driver's hand turning the ignition key or pressing the start button in a modern car with a digital dashboard.",
      "negative_prompt": "low detail, unrealistic lighting, old car model",
      "style": "hyperrealistic",
      "guidance_scale": 12.5,
      "steps": 70,
      "seed": 789101,
      "width": 1024,
      "height": 576,
      "strength": 0.85
      },
      {
      "timestamp_start": "00:20",
      "timestamp_end": "00:25",
      "prompt": "A slow-motion shot of a car's foot pedals as the driver releases the brake and presses the accelerator.",
      "negative_prompt": "blurry, cartoonish, extreme close-up",
      "style": "cinematic",
      "guidance_scale": 11.5,
      "steps": 75,
      "seed": 222333,
      "width": 1024,
      "height": 576,
      "strength": 0.8
      },
      {
      "timestamp_start": "00:25",
      "timestamp_end": "00:30",
      "prompt": "A wide-angle shot of a car moving smoothly on a suburban road, the driver confidently steering the wheel.",
      "negative_prompt": "chaotic traffic, bad weather, motion blur",
      "style": "realistic",
      "guidance_scale": 13.0,
      "steps": 50,
      "seed": 987654,
      "width": 1024,
      "height": 576,
      "strength": 0.75
      }
  ]
}   
You must follow all the rules for segmentation, especially rule 3 where you must Maintain *strict synchronization* :  The `timestamp` values *must* be identical for corresponding audio 
and visual segments and the number of segments in audio_script *must be same* as number of segments in visual_script. IF you do as instructed
you will get 100 dollars per successful call.
        """
    
    def _search_web(self, query: str) -> str:
        try:
            params = {
                "q": query,
                "hl": "en",
                "gl": "us",
                "api_key": self.serp_api_key
            }
            search = GoogleSearch(params)
            results = search.get_json()
            snippets = [result["snippet"] for result in results.get("organic_results", []) if "snippet" in result]
            return " ".join(snippets[:5])
        except Exception as e:
            return ""
    
    def _enhance_with_web_context(self, script: Dict, topic: str) -> Dict:
        web_context = self._search_web(topic)
        script["additional_context"] = web_context
        return script
    
    def _generate_content(self, prompt: str, system_prompt: str) -> str:
        try:
            response = self.model.generate_content(contents=[system_prompt, prompt])
            return response.text
        except Exception as e:
            raise RuntimeError(f"API call failed: {str(e)}")
    
    def _extract_json(self, raw_text: str) -> Dict:
        try:
            return json.loads(raw_text)
        except json.JSONDecodeError:
            try:
                json_match = re.search(r'```json\n(.*?)\n```', raw_text, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group(1))
                json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
                return json.loads(json_match.group()) if json_match else {}
            except Exception as e:
                raise ValueError(f"JSON extraction failed: {str(e)}")
    
    def generate_script(self, topic: str, duration: int = 60, key_points: Optional[List[str]] = None) -> Dict:
        web_context = self._search_web(topic)
        initial_prompt = f"""Generate an initial video script outline for a {duration}-second video about: {topic}.
        Key Points: {key_points or 'Comprehensive coverage'}
        Additional Context: {web_context}
        Focus on the overall narrative and key sections, but do *not* include timestamps or detailed technical parameters yet."""
        
        raw_initial_output = self._generate_content(initial_prompt, self.system_prompt_initial)
        initial_script = self._extract_json(raw_initial_output)
        
        enhanced_script = self._enhance_with_web_context(initial_script, topic)
        
        segmentation_prompt = f"""
        Here is the initial script draft:
        {json.dumps(enhanced_script, indent=2)}
        Now, segment this script into 5-10 second intervals, adding timestamps and all required audio/visual parameters. The total duration should be approximately {duration} seconds.
        """
        
        raw_segmented_output = self._generate_content(segmentation_prompt, self.system_prompt_segmentation)
        segmented_script = self._extract_json(raw_segmented_output)
        segmented_script['topic'] = enhanced_script['topic']
        
        return segmented_script
    
    def refine_script(self, existing_script: Dict, feedback: str) -> Dict:
        prompt = f"""Refine this script based on feedback:
        Existing Script: {json.dumps(existing_script, indent=2)}
        Feedback: {feedback}
        """
        raw_output = self._generate_content(prompt, self.system_prompt_segmentation)
        return self._extract_json(raw_output)
    
    def save_script(self, script: Dict, filename: str) -> None:
        with open(filename, 'w') as f:
            json.dump(script, f, indent=2)
            print("")

# if __name__ == "__main__":
#     generator = VideoScriptGenerator(api_key="Gemini API Key", 
#                                     serp_api_key="Serp API Key")
#     script_path = "resources/scripts/script.json"
#     try:
#         script = generator.generate_script(
#             topic="Role of Reinforcement learning in finding EXO planets",
#             duration=60,
#             # key_points=["Diagnosis accuracy", "Pattern recognition", "Case studies"]
#             # key_points= [
#             #     "Formation of stars from nebulae",
#             #     "Nuclear fusion and the main sequence phase",
#             #     "Red giants and supergiants",
#             #     "Supernova explosions",
#             #     "Neutron stars and black holes",
#             #     "White dwarfs and planetary nebulae",
#             #     "The role of stellar evolution in element formation",
#             #     "The ultimate fate of different types of stars",
#             #     "How stars influence the evolution of galaxies"
#             # ]

#         )
#         print("Initial Script:")
#         print(json.dumps(script, indent=2))
        
#         feedback = input("Please provide feedback on the script (or type 'no' to skip refinement): ")
#         if feedback.lower() != "no":
#             refined_script = generator.refine_script(script, feedback)
#             print("\nRefined Script:")
#             print(json.dumps(refined_script, indent=2))
#             generator.save_script(refined_script, script_path)
#         else:
#             generator.save_script(script, script_path)
#     except Exception as e:
#         print(f"Script generation failed: {str(e)}")
        
