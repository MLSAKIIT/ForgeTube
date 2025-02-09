<a>
  <h1 align="center"> MLSA Project Wing: ML </h1>
</a>
<p align="center"> <img src="https://avatars.githubusercontent.com/u/79008924?s=280&v=4">
</p>


# ForgeTube Video Assembler
The current video assembler, built using **`MoviePy`** (which relies on **`FFmpeg`** for video processing), takes all images from the ***Images*** folder and all audio files from the** *Audio*** folder and combines them into a single video. Each image is displayed for the exact duration of its corresponding audio file, ensuring perfect synchronisation between visuals and sound.  

Both images and audio files are sorted alphabetically before being compiled in sequence. To maintain the correct order, it is recommended to name the files numerically (e.g., `01.jpg`, `01.mp3`, `02.jpg`, `02.mp3`, etc.).

## Get started 
Install MoviePy via `pip install moviepy`.

Install FFmpeg from [here](https://www.ffmpeg.org/download.html)


## Project Structure
```
├───Moviepy Showcase : Contains a simple script showcasing different features of moviepy and how it works
│   └───resources
│       └───font
├───Samples : Contains various different media for testing
│   ├───Audio
│   │   ├───.mp4
│   │   └───.wav
│   ├───font
│   ├───Images
│   ├───raw
│   ├───Subtitles
│   ├───templates : Contains Mock scripts for testing
│   └───videos
└───Video Assembly : Contains the custom video assembler script
```


> [!IMPORTANT]
> Replace the following folders with your own folders for testing

```py
image_folder = "samples/Images/"  
audio_folder = "samples/Audio/.wav/"
output_file = "samples/video/Cats.mp4" 
```

## Features Coming Soon
- Subtitles
- Transition effects clip to clip
- Intro and Outro sequence
- Multiple images for the same audio stream
- Testing and Optimizing the runtime
