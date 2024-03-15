from typing import List
from uuid import uuid4

import assemblyai as aai
from moviepy.config import change_settings
from moviepy.editor import *
from moviepy.video.fx.all import crop
from moviepy.video.tools.subtitles import SubtitlesClip
from termcolor import colored

from src.utils.config import get_fonts_dir, get_assemblyai_api_key, ROOT_DIR, get_imagemagick_path, get_threads, \
    get_verbose
from src.utils.utils import choose_random_song, equalize_subtitles, info, success

# Set ImageMagick Path
change_settings({"IMAGEMAGICK_BINARY": get_imagemagick_path()})


def generate_subtitles(audio_path: str) -> str:
    """
    Generates subtitles for the audio using AssemblyAI.

    Args:
        audio_path (str): The path to the audio file.

    Returns:
        path (str): The path to the generated SRT File.
    """
    # Turn the video into audio
    aai.settings.api_key = get_assemblyai_api_key()
    config = aai.TranscriptionConfig()
    transcriber = aai.Transcriber(config=config)
    transcript = transcriber.transcribe(audio_path)
    subtitles = transcript.export_subtitles_srt()

    srt_path = os.path.join(ROOT_DIR, "temp", str(uuid4()) + ".srt")

    with open(srt_path, "w") as file:
        file.write(subtitles)

    return srt_path


def generate_video(images, tts_path, subtitles_path, font, subtitles_max_chars, subtitles_size, subtitles_color, subtitles_stroke_color, subtitles_stroke_thickness, audio_volume) -> str:
    """
    Combines everything into the final video.

    Args:
        images (List[str]): The list of image paths to combine
        tts_path (str): The path to the TTS file
        subtitles_path (str): The path to the subtitles file
        font (str): The font to use for the subtitles
        subtitles_max_chars (int): The maximum amount of characters in a subtitle
        subtitles_size (int): The size of the subtitles
        subtitles_color (str): The color of the subtitles
        subtitles_stroke_color (str): The stroke color of the subtitles
        subtitles_stroke_thickness (int): The stroke thickness of the subtitles
        audio_volume (float): The volume of the audio

    Returns:
        path (str): The path to the generated MP4 File.
    """
    combined_image_path = os.path.join(ROOT_DIR, "temp", str(uuid4()) + "temp4")
    threads = get_threads()
    tts_clip = AudioFileClip(tts_path)
    max_duration = tts_clip.duration
    req_dur = max_duration / len(images)

    # Make a generator that returns a TextClip when called with consecutive
    generator = lambda txt: TextClip(
        txt,
        font=os.path.join(get_fonts_dir(), font),
        fontsize=subtitles_size,
        color=subtitles_color,
        stroke_color=subtitles_stroke_color,
        stroke_width=subtitles_stroke_thickness,
        size=(1080, 1920),
        method="caption",
    )

    print(colored("[+] Combining images...", "blue"))

    clips = []
    tot_dur = 0
    # Add downloaded clips over and over until the duration of the audio (max_duration) has been reached
    while tot_dur < max_duration:
        for image_path in images:
            clip = ImageClip(image_path)
            clip.duration = req_dur
            clip = clip.set_fps(30)

            # Not all images are same size,
            # so we need to resize them
            if round((clip.w / clip.h), 4) < 0.5625:
                if get_verbose():
                    info(f" => Resizing Image: {image_path} to 1080x1920")
                clip = crop(clip, width=clip.w, height=round(clip.w / 0.5625), \
                            x_center=clip.w / 2, \
                            y_center=clip.h / 2)
            else:
                if get_verbose():
                    info(f" => Resizing Image: {image_path} to 1920x1080")
                clip = crop(clip, width=round(0.5625 * clip.h), height=clip.h, \
                            x_center=clip.w / 2, \
                            y_center=clip.h / 2)
            clip = clip.resize((1080, 1920))

            # FX (Fade In)
            # clip = clip.fadein(2)

            clips.append(clip)
            tot_dur += clip.duration

    final_clip = concatenate_videoclips(clips)
    final_clip = final_clip.set_fps(30)
    random_song = choose_random_song()

    # Equalize srt file
    equalize_subtitles(subtitles_path, subtitles_max_chars)

    # Burn the subtitles into the video
    subtitles = SubtitlesClip(subtitles_path, generator)

    subtitles.set_pos(("center", "center"))
    random_song_clip = AudioFileClip(random_song).set_fps(44300)

    # Turn down volume
    random_song_clip = random_song_clip.fx(afx.volumex, audio_volume)
    comp_audio = CompositeAudioClip([
        tts_clip.set_fps(44300),
        random_song_clip
    ])

    final_clip = final_clip.set_audio(comp_audio)
    final_clip = final_clip.set_duration(tts_clip.duration)

    # Add subtitles
    final_clip = CompositeVideoClip([
        final_clip,
        subtitles
    ])

    final_clip.write_videofile(combined_image_path, threads=threads)

    success(f"Wrote Video to \"{combined_image_path}\"")

    return combined_image_path
