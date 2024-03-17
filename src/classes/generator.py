import json
import os
import re
from typing import List
from uuid import uuid4

import g4f
import requests

from src.utils.config import ROOT_DIR, get_verbose
from src.utils.constants import parse_model, build_generate_topic_prompt, build_generate_script_prompt, \
    build_generate_title_prompt, build_generate_description_prompt, build_generate_image_prompts
from src.utils.status import info, error, success
from src.utils.tts import TTS
from src.utils.video import generate_subtitles, generate_video
from src.utils.web_browser import init_browser, upload_video
from utils.utils import close_running_selenium_instances


def generate_script_to_speech(script) -> str:
    """
    Converts the generated script into Speech using CoquiTTS and returns the path to the wav file.

    Args:
        script (str): The script to convert to speech.

    Returns:
        path_to_wav (str): Path to generated audio (WAV Format).
    """
    path = os.path.join(ROOT_DIR, "temp", str(uuid4()) + ".wav")

    # Clean script, remove every character that is not a word character,
    # a space, a period, a question mark, or an exclamation mark.
    script = re.sub(r'[^\w\s.?!]', '', script)

    TTS().synthesize(script, path)

    if get_verbose():
        info(f" => Wrote TTS to \"{path}\"")

    return path


class Generator:
    def __init__(self, config: dict) -> None:
        self.id = config["id"]
        self.language = config["language"]
        self.subject = config["subject"]
        self.llm = config["llm"]
        self.image_prompt_llm = config["image_prompt_llm"]
        self.image_model = config["image_model"]
        self.is_for_kids = config["is_for_kids"]
        self.font = config["font"]
        self.firefox_profile = config["firefox_profile"]
        self.subtitles_max_chars = config["subtitles_max_chars"]
        self.subtitles_font_size = config["subtitles_font_size"]
        self.subtitles_font_color = config["subtitles_font_color"]
        self.subtitles_font_outline_color = config["subtitles_font_outline_color"]
        self.subtitles_font_outline_thickness = config["subtitles_font_outline_thickness"]
        self.audio_song_volume = config["audio_song_volume"]
        self.images_count = config["images_count"]

        if get_verbose():
            success(f"Initialized Generator with ID: {self.id}")

    def generate_video(self):
        done = False
        while not done:
            try:
                if get_verbose():
                    info(f"Generating Video for Subject: {self.subject}")
                topic = self.generate_topic(self.subject)
                if get_verbose():
                    info(f"Generated Topic: {topic}")
                script = self.generate_script(topic, self.language)
                if get_verbose():
                    info(f"Generated Script: {script}")
                metadata = self.generate_metadata(topic, script, self.language)
                if get_verbose():
                    info(f"Generated Metadata: {metadata}")
                image_prompts = self.generate_image_prompts(script, topic, self.images_count)
                if get_verbose():
                    info(f"Generated Image Prompts: {image_prompts}")

                images_files = []
                for prompt in image_prompts:
                    image = self.generate_image(prompt)
                    images_files.append(image)
                    if get_verbose():
                        info(f"Generated Image: {image} for prompt: {prompt}")

                audio_file = generate_script_to_speech(script)
                srt_file = generate_subtitles(audio_file)

                video_file = generate_video(images_files, audio_file, srt_file, self.font, self.subtitles_max_chars,
                                            self.subtitles_font_size, self.subtitles_font_color,
                                            self.subtitles_font_outline_color, self.subtitles_font_outline_thickness,
                                            self.audio_song_volume)

                success(f"Generated Video: {video_file}")
                metadata["video_path"] = video_file
                return metadata
            except Exception as e:
                error(f"Error occurred while generating video: {str(e)}")
                done = False

    def generate_response(self, prompt: str, model: any) -> str:
        """
        Generates an LLM Response based on a prompt and the user-provided model.

        Args:
            prompt (str): The prompt to use in the text generation.
            model (any): The model to use for the generation.

        Returns:
            response (str): The generated AI Repsonse.
        """

        response = ""
        retry = 0
        while not response:
            if retry > 10:
                error("Failed to generate response.")
                return ""
            response = g4f.ChatCompletion.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            retry += 1
        return response

    def generate_topic(self, subject) -> str:
        """
        Generates a topic based on the YouTube Channel niche.

        Args:
            subject (str): The subject of the video.

        Returns:
            topic (str): The generated topic.
        """
        completion = self.generate_response(build_generate_topic_prompt(subject), parse_model(self.llm))

        completion = completion.replace('"', '')

        if not completion:
            error("Failed to generate Topic.")

        return completion

    def generate_script(self, subject, language) -> str:
        """
        Generate a script for a video, depending on the subject of the video, the number of paragraphs, and the AI model.

        Args:
            subject (str): The subject of the video.
            language (str): The language of the video.

        Returns:
            script (str): The script of the video.
        """
        completion = self.generate_response(build_generate_script_prompt(subject, language), parse_model(self.llm))

        # Apply regex to remove *
        completion = re.sub(r"\*", "", completion)

        if not completion:
            error("The generated script is empty.")
            return ""

        return completion

    def generate_metadata(self, subject, script, language) -> dict:
        """
        Generates Video metadata for the to-be-uploaded YouTube Short (Title, Description).

        Args:
            subject (str): The subject of the video.
            script (str): The script of the video.

        Returns:
            metadata (dict): The generated metadata.
        """
        title = self.generate_response(build_generate_title_prompt(subject, language), parse_model(self.llm))
        description = self.generate_response(build_generate_description_prompt(script, language), parse_model(self.llm))

        description = description.replace('"', '')

        metadata = {
            "title": title,
            "description": description
        }

        return metadata

    def generate_image_prompts(self, script, subject, n_prompts) -> List[str]:
        """
        Generates AI Image Prompts based on the provided Video Script.

        Args:
            script (str): The script to generate prompts for.
            subject (str): The subject of the video.
            n_prompts (int): The number of prompts to generate.

        Returns:
            image_prompts (List[str]): Generated List of image prompts.
        """

        prompt = build_generate_image_prompts(script, subject, n_prompts)

        completion = str(self.generate_response(prompt, parse_model(self.image_prompt_llm))) \
            .replace("```json", "") \
            .replace("```", "")

        completion = completion[completion.find("["):]
        completion = completion[:completion.find("]") + 1]

        image_prompts = []

        if "image_prompts" in completion:
            image_prompts = json.loads(completion)["image_prompts"]
        else:
            image_prompts = json.loads(completion)
            if get_verbose():
                info(f" => Generated Image Prompts: {image_prompts}")

        return image_prompts

    def generate_image(self, prompt: str) -> str:
        """
        Generates an AI Image based on the given prompt.

        Args:
            prompt (str): Reference for image generation

        Returns:
            path (str): The path to the generated image.
        """
        ok = False
        while not ok:
            url = f"https://hercai.onrender.com/{self.image_model}/text2image?prompt={prompt}"

            r = requests.get(url)
            parsed = r.json()

            if "url" not in parsed or not parsed.get("url"):
                # Retry
                if get_verbose():
                    info(f" => Failed to generate Image for Prompt: {prompt}. Retrying...")
                ok = False
            else:
                ok = True

                image_url = parsed["url"]
                image_path = os.path.join(ROOT_DIR, "temp", str(uuid4()) + ".png")

                with open(image_path, "wb") as image_file:
                    # Write bytes to file
                    image_r = requests.get(image_url)

                    image_file.write(image_r.content)

                if get_verbose():
                    info(f" => Wrote Image to \"{image_path}\"\n")

                return image_path

    def upload_video(self, video_path, title, description) -> str:
        """

        Args:
            video_path: the path to the video file
            title: the title of the video
            description: the description of the video

        Returns:
            url (str): The URL of the uploaded video.

        """
        info("Uploading video to YouTube...")
        #close_running_selenium_instances()
        browser = init_browser(self.firefox_profile)
        url = upload_video(browser, video_path, title, description, self.is_for_kids)
        success(f"Uploaded Video: {url}")
        return url
