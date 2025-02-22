# import modal
import json
import os
import time
from io import BytesIO

# image = modal.Image.debian_slim().pip_install(
#     "diffusers",
#     "torch",
#     "transformers",
#     "accelerate"
# )

# app = modal.App(name="finalgen_app")

# @app.function(image=image, gpu="A10G")
def generate_image(prompt, negative_prompt="", steps=50, guidance_scale=9, width=1920, height=1080, seed=None):
    import torch
    # from diffusers import StableDiffusionPipeline
    from diffusers import DiffusionPipeline


# LOADS THE DIFFUSION PIPELINE

    # pipe = StableDiffusionPipeline.from_pretrained("runwayml/stab", torch_dtype=torch.float16)
    pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", 
                                            torch_dtype=torch.float16,
                                            use_safetensors=True, 
                                            variant="fp16")
    
    pipe.to("cuda" if torch.cuda.is_available() else "cpu")

    generator = torch.Generator(device="cuda" if torch.cuda.is_available() else "cpu").manual_seed(seed) if seed else None

    image = pipe(
        prompt,
        negative_prompt=negative_prompt,
        num_inference_steps=steps,
        guidance_scale=guidance_scale,
        width=width,
        height=height,
        generator=generator
    ).images[0]

    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)

    return img_byte_arr.getvalue()


# PATH TO JSON FILE

script_path = "resources/scripts/script.json"
images_output_path = "resources/images/"
# os.makedirs(output_path, exist_ok=True)


# PROVIDE SOURCE TEXT OR PROMPT IN JSON FILE

def main_generate_image(script_path,images_output_path):
    # JSON Decoding Error Handling
    with open(script_path, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            print("Error reading JSON file.")
            return
    # JSON Key Error Handling
    if "visual_script" not in data:
        print("Missing key in JSON.")
        return
    

# GENERATING THE IMAGES 
    
    # Looping Through the Scenes
    for idx, scene in enumerate(data["visual_script"]):
        try:
            prompt = scene["prompt"]
            timestamp = scene.get("timestamp", f"{idx:03d}")
            negative_prompt = scene.get("negative_prompt", "")
            steps = scene.get("steps", 50)
            # guidance_scale = scene.get("guidance_scale", 12)
            guidance_scale = 9
            # width = scene.get("width", 1024)
            width = 1920
            # height = scene.get("height", 576)
            height = 1080
            seed = scene.get("seed", None)

            scene_id = timestamp.replace(":", "-")

            image_data = generate_image(prompt, negative_prompt, steps, guidance_scale, width, height, seed)


    # SAVING THE IMAGES IN THE OUTPUT DIRECTORY

            file_path = os.path.join(images_output_path, f"scene_{scene_id}.png")
            with open(file_path, "wb") as f:
                f.write(image_data)

            print(f"Saved: {file_path}")

            time.sleep(2)

        except Exception as e:
            print(f"Error processing scene {idx}: {e}")

        print("Image Generation is Done.")

# if __name__ == "__main__":
#     main_generate_image(script_path=script_path,images_output_path=images_output_path)
