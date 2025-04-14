# ForgeTube Web Frontend

A modern, dark-themed web interface for ForgeTube, an AI-powered video generation system.

## Overview

This Flask application provides an intuitive web interface for interacting with ForgeTube's automated video generation capabilities. It allows users to:

1. Input topics, durations, and key points for video generation
2. Review and refine AI-generated scripts
3. Track the progress of video generation
4. Preview and download the final videos

## Features

- **Modern, Dark UI**: Sleek, minimalistic interface with a dark color scheme
- **Responsive Design**: Works well on desktop and mobile devices
- **Real-time Progress Tracking**: Live updates on video generation status
- **Script Refinement**: Interactive script review and feedback system
- **Secure API Key Management**: User-provided API keys used securely for content generation

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/MLSAKIIT/ForgeTube.git
   cd ForgeTube
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```
   Then edit the `.env` file with your API keys.

## Usage

1. Start the Flask development server:

   ```bash
   flask run
   ```

2. Open your browser and navigate to:

   ```
   http://127.0.0.1:5000/
   ```

3. Follow the on-screen instructions to create your first video.

## Requirements

- Python 3.8 or higher
- Gemini API key (from Google AI Studio)
- SERP API key (from serpapi.com)
- FFmpeg (for video processing)

## Integration with ForgeTube Core

This frontend is designed to work with ForgeTube's core modules:

- `diffusion/scripts/generate_script.py`: For script generation
- `diffusion/scripts/generate_image_local.py`: For image generation
- `tts/scripts/generate_audio.py`: For audio generation
- `assembly/scripts/assembly_video.py`: For final video assembly

## Development

To contribute to this frontend:

1. Create a new branch for your feature or bug fix
2. Make your changes
3. Submit a pull request

## License

This project is licensed under the same terms as the main ForgeTube project.
