from moviepy import *
import numpy as np
#################
# VIDEO LOADING #
#################
# We load our video
video = VideoFileClip("assembly/Test/resources/bbb.mp4")
#####################
# SCENES EXTRACTION #
#####################
# We extract the scenes we want to use

# First the characters
intro_clip = video.subclipped(1, 11)
bird_clip = video.subclipped(16, 20)
bunny_clip = video.subclipped(37, 55)
rodents_clip = video.subclipped(
    "00:03:34.75", "00:03:56"
)  # we can also use string notation with format HH:MM:SS.uS
rambo_clip = video.subclipped("04:41.5", "04:44.70")
#####################
# SCENES PREVIEWING #
#####################
# Now, lets have a first look at our clips
# Warning: you need ffplay installed for preview to work
# We set a low fps so our machine can render in real time without slowing down
intro_clip.preview(fps=20)
bird_clip.preview(fps=20)
bunny_clip.preview(fps=20)
rodents_clip.preview(fps=20)
rambo_clip.preview(fps=20)
##############################
# CLIPS MODIFICATION CUTTING #
##############################
# Well, looking at the rodent scene it is a bit long isn't?
# Let's see how we modify the clip with one of the many clip manipulation method starting by with_*
# in that case by removing of the clip the part between 00:06:00 to 00:10:00 of the clip, using with_section_cut_out
rodents_clip = rodents_clip.with_section_cut_out(start_time=4, end_time=10)

# Note: You may have noticed that we have reassign rodents_clip, this is because all with_* methods return a modified *copy* of the
# original clip instead of modifying it directly. In MoviePy any function starting by with_* is out-place instead of in-place
# meaning it does not modify the original data, but instead copy it and modify/return the copy

# Lets check the result
rodents_clip.preview(fps=10)

############################
# TEXT/LOGO CLIPS CREATION #
############################
# Lets create the texts to put between our clips
font = "./resources/font/font.ttf"
intro_text = TextClip(
    font=font,
    text="The Blender Foundation and\nPeach Project presents",
    font_size=50,
    color="#fff",
    text_align="center",
)
bird_text = TextClip(font=font, text="An unlucky bird", font_size=50, color="#fff")
bunny_text = TextClip(
    font=font, text="A (slightly overweight) bunny", font_size=50, color="#fff"
)
rodents_text = TextClip(
    font=font, text="And three rodent pests", font_size=50, color="#fff"
)
revenge_text = TextClip(
    font=font, text="Revenge is coming...", font_size=50, color="#fff"
)
made_with_text = TextClip(font=font, text="Made with", font_size=50, color="#fff")

# We will also need the big buck bunny logo, so lets load it and resize it
logo_clip = ImageClip("./resources/logo_bbb.png").resized(width=400)
moviepy_clip = ImageClip("./resources/logo_moviepy.png").resized(width=300)