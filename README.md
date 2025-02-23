<a>
  <h1 align="center"> MLSA Project Wing: ML </h1>
</a>
<p align="center"> <img src="https://avatars.githubusercontent.com/u/79008924?s=280&v=4">
</p>

<a>
  <h1 align="center"> ForgeTube </h1>
</a>

[![GitHub](https://img.shields.io/badge/GitHub-MLSAKIIT-181717?style=for-the-badge&logo=github)](https://github.com/MLSAKIIT)
[![ForgeTube](https://img.shields.io/badge/ForgeTube-Repository-181717?style=for-the-badge&logo=github)](https://github.com/MLSAKIIT/ForgeTube)
[![YouTube](https://img.shields.io/badge/YouTube-ForgeTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/channel/UCVgzYqxxY6wCIto-Nzx68Uw)
[![X](https://img.shields.io/badge/X-mlsakiit-1DA1F2?style=for-the-badge&logo=X&logoColor=white)](https://x.com/mlsakiit)
[![Instagram](https://img.shields.io/badge/Instagram-mlsakiit-E4405F?style=for-the-badge&logo=instagram)](https://www.instagram.com/mlsakiit/)
[![Discord](https://img.shields.io/badge/Discord-Join%20Us-5865F2?style=for-the-badge&logo=discord)](https://discord.com/invite/P6VCP2Ry3q)


## 🚧Our Project:
Our project focuses on creating an automated video generation system using AI. It transforms text prompts into fully narrated videos by leveraging **large language models** for script generation, **diffusion models** for image creation, and **text to speech systems** for narration. The system processes inputs through multiple stages, from script generation to final video assembly, creating cohesive, engaging content automatically.

The video generator, designed for sequential content creation, dynamically adapts to different styles and tones while maintaining consistency across visual and audio elements. It also has the ability to add **subtiles** either embedded or through the use of an **srt** file.

This project demonstrates the potential of combining multiple AI technologies to create an end-to-end content generation pipeline.

## 🖥️Project Stack:
   `Python 3.11`: Core programming language for the project.

- **Content Generation:**
   
   `Gemini API`: To generate the script using `Gemini 2.0 Flash Thinking` model and store it in a `JSON` format with proper audio and visual prompts and respective parameters.
   
   `Stable Diffusion XL Base 1.0`: For image generation using diffusion models to run either `locally` or hosted on `Modal`.

   `Kokoro`: An open weight tts model to convert audio prompts into audio.

- **Video Processing**
    `MoviePy` : For adding text, intro, outro, transition effects, subtitles, audio processing, video processing and Final_Assembly by using  `FFmpeg` under the hood.

- **ML Frameworks:**
    
    `PyTorch`: Deep learning framework for model inferencing.

    `Diffusers with SDXL Base 1.0` : Utilize Hugging Face's Diffusers to generate stunning images using the SDXL Base 1.0 model. Enhance your creative projects with state-of-the-art diffusion techniques.

- **Development Tools:**
    
    `Jupyter Notebooks`: For development and testing.

    `Google Colab` : For free cloud GPU infrastructure for development and Testing.
    
    `Git`: For version control

    `Modal` : For low cost high performance cloud GPU infrastructure.

- **Package Management:**

    `UV`: For fast and efficient dependency management and project setup

## Features

- **Multi-Modal Content Generation**: Seamlessly combines text, image, and audio generation
- **Style Customization**: Supports different content styles and tones
- **Modular Architecture**: Each component can be tested and improved independently
- **Content Segmentation**: Automatically breaks down content into manageable segments
- **Custom Voice Options**: Multiple TTS voices and emotional tones
- **Format Flexibility**: Supports different video durations and formats (.mp4 and .mkv)
- **Performance Metrics**: Tracks generation quality and consistency
- **Error Handling**: Robust error management across the pipeline
- **Resource Optimization**: Efficient resource usage during generation


## Steps for deployment :
### 1. Using UV for Python Package Management

For more information, visit the [UV Documentation](https://docs.astral.sh/uv/).

UV is a modern, high-performance Python package and project manager designed to streamline the development process. 

Here’s how you can use UV in this project:

1. Install `uv`.

```bash
pip install uv
```
2. Download `Python 3.11`
```bash
uv python install 3.11
```
3. Create a virtual environment 
```bash
uv venv .venv
```
4. Activate your virtual environment
```bash
.venv\scripts\activate.ps1
```
5. Install all dependencies 
```bash
uv sync
```
### 2. Setting up Modal
For more information visit the [Modal documentation](https://modal.com/docs/guide).

Modal is a cloud function platform that lets you Attach high performance GPUs with a single line of code.

The nicest thing about all of this is that you don’t have to set up any infrastructure. Just:

1. Create an account at [modal.com](modal.com)
2. Run `pip install modal` to install the modal Python package
3. Run `modal setup` to authenticate (if this doesn’t work, try `python -m modal setup`)

### 3. Get your Gemini-API Key :
To obtain a Gemini API key from Google AI Studio, follow these detailed steps:

**Step 1: Sign In to Google AI Studio**

Navigate to [Google AI Studio](https://aistudio.google.com/). Once
 signed in, locate and click on the "Gemini API" tab. This can typically be found in the main navigation menu or directly on the dashboard. On the Gemini API page, look for a button labeled "Get API key in Google AI Studio" and click on it.

**Step 2: Review and Accept Terms of Service**

1. **Review Terms**: A dialog box will appear presenting the Google APIs Terms of Service and the Gemini API Additional Terms of Service. It's essential to read and understand these terms before proceeding.
2. **Provide Consent**: Check the box indicating your agreement to the terms. Optionally, you can also opt-in to receive updates and participate in research studies related to Google AI.
3. **Proceed**: Click the "Continue" button to move forward.

**Step 3: Create and Secure Your API Key**

1. **Generate API Key**: Click on the "Create API key" button. You'll be prompted to choose between creating a new project or selecting an existing one. Make your selection accordingly.
2. **Retrieve the Key**: Once generated, your unique API key will be displayed. Ensure you copy and store it in a secure location.

**Step 4: Add your Key in `main.py` or `local_main.py`**
```python
# 1. Generate the Script
gem_api = "Enter your Gemini API Key here"
serp_api = "Enter your Serp API key here"
```

> [!IMPORTANT]  
> Always keep your API key confidential. Avoid sharing it publicly or embedding it directly into client-side code to prevent unauthorized access.

### 4. Setting up Serp-Api
Serp is used for web scraping google search results on the video topic and gathering additional context to implement Retrieval Augmented Generation (RAG)
1. Visit [serpapi.com/](https://serpapi.com/) and create an account.
2. Go to the [dashboard](https://serpapi.com/dashboard), on the top left select Api key.
3. Copy the API Key and add your Key in `main.py` or `local_main.py`
```py
# 1. Generate the Script
gem_api = "Enter your Gemini API Key here"
serp_api = "Enter your Serp API key here"
```
### 5. `Kokoro` 
Run the following commands :
```bash
python -m pip install spacy # If not insatlled for some reason
python -m spacy download en_core_web_sm
```
### 6. Download and setup FFmpeg
1. Visit : https://github.com/BtbN/FFmpeg-Builds/releases
2. Download the setup file for your OS.
3. On windows download the win64 version, and extract the files.
4. Make a directory at `C:\Program Files\FFmpeg`.
5. Copy all the files in the directory.
6. Add `C:\Program Files\FFmpeg\bin` to your `PATH` environment variable.
7. 
### 7. Start Generating :
Use `main.py` for running the image generation on Modal or use `main_local.py` to run Stable diffusion XL Locally.

## Troubleshooting
1. Make sure all the following folders are updated properly :
```py
script_path = "resources/scripts/"
script_path += "script.json" # Name of the script file
images_path = "resources/images/"
audio_path = "resources/audio/"
font_path = "resources/font/font.ttf" # Not recommended to change
```
Name of video file is automatically grabbed from video topic in script. However you may change the following variables to have custom names, if files names are very long then video file wont be generated, so do manually change it in such cases.

```py
sub_output_file = f"resources/subtitles/name of the subtitle file.srt"
video_file = "name of the video.mp4 or .mkv"
```

2. If you get a `no module named pip found` error try running the following :
```bash
python -m pip install spacy pydub kokoro soundfile torch
python -m spacy download en_core_web_sm
```
3. Serp API not returning any search results.
This is a known issue and is being investigated.


> [!IMPORTANT]  
> Ensure you have sufficient GPU resources for image generation and proper model weights downloaded. It is recommend to use an **NVDIA** GPU with at least **24 GB or more of VRAM** for locally running the image generation and a high single core performance CPU for video assembly.

> [!NOTE]
> Video generation times may vary based on content length , complexity and hardware used.

## Contributors

| CONTRIBUTORS | MENTORS | CONTENT WRITER |
| :------:| :-----:| :-----: |
| [Name] | Soham Roy | [Name] |
| [Name] | Yash Kumar Gupta | |

## Version
| Version | Date | Comments |
| ------- | ---- | -------- |
| 1.0     | 23/02/2025 | Initial release |

## Future Roadmap

### Part 1: Baseline
- [x] Pipeline foundations
- [x] LLM Agent Handing
- [x] Diffusion Agent Handing
- [x] TTS Handing
- [x] Video Assembly Engine
- [x] Initial Deployment

### Part 2: Advanced
- [ ] Advanced style transfer capabilities
- [ ] In-Context Generation for Diffusion Model
- [ ] Real time generation monitoring
- [x] Enhanced video transitions
- [ ] Better quality metrics
- [ ] Multi language support
- [ ] Custom character consistency
- [ ] Animation effects

## Acknowledgements
- Hugging Face Transformers - https://huggingface.co/transformers
- Hugging Face Diffusers - https://huggingface.co/diffusers
- FFmpeg - https://ffmpeg.org/
- UV - https://docs.astral.sh/uv/
- MoviePy - https://zulko.github.io/moviepy/getting_started/index.html
## Project References
### 1. Large Language Models (LLMs) & Transformers

* [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) - A visual, beginner-friendly introduction to transformer architecture.
* [Attention Is All You Need](https://arxiv.org/abs/1706.03762) - The seminal paper on transformer architecture.
* [Gemini 2.0 Flash Thinking](https://ai.google.dev/gemini-api/docs/thinking)
---
### 2. Multi-Agent Systems  
  * [Introduction to Multi-Agent Systems](https://www.geeksforgeeks.org/what-is-a-multi-agent-system-in-ai/) - Fundamental concepts and principles.
  * [ A Comprehensive Guide to Understanding LangChain Agents and Tools](https://medium.com/@piyushkashyap045/a-comprehensive-guide-to-understanding-langchain-agents-and-tools-43a187414f4c) - Practical implementation guide.
* [kokoro](https://github.com/hexgrad/kokoro?tab=readme-ov-file#kokoro)
  
### 2. Image Generation & Processing
* [Stable Diffusion XL Turbo 1.0 Base](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0)
* [Stable Diffusion: A Comprehensive End-to-End Guide with Examples](https://medium.com/@jagadeesan.ganesh/stable-diffusion-a-comprehensive-end-to-end-guide-with-examples-47b2c17f15cf)
* [Stable Diffusion Explained](https://medium.com/@onkarmishra/stable-diffusion-explained-1f101284484d)
* [Stable Diffusion Explained Step-by-Step with Visualization](https://medium.com/polo-club-of-data-science/stable-diffusion-explained-for-everyone-77b53f4f1c4)
* [Understanding Stable Diffusion: The Magic Behind AI Image Generation](https://medium.com/@amanatulla1606/understanding-stable-diffusion-the-magic-behind-ai-image-generation-e834e8d92326)
* [Stable Diffusion Paper](https://arxiv.org/pdf/2403.03206)

---
### 3. RAG
* [Retrieval Augmented Generation](https://aiplanet.com/learn/llm-bootcamp/module-13/2380/retrieval-augmented-generation)

---
