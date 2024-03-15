import re
from typing import List
from uuid import uuid4

import requests

from config import *
from constants import *
from status import *
from tts import TTS


def generate_response(prompt: str, model: any) -> str:
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

def generate_topic(subject) -> str:
    """
    Generates a topic based on the YouTube Channel niche.

    Args:
        subject (str): The subject of the video.

    Returns:
        topic (str): The generated topic.
    """
    completion = generate_response(
        f"Please generate a specific video idea that takes about the following topic: {subject}. "
        f"Make it exactly one sentence. "
        f"Be creative! Find a unique angle or perspective on the topic."
        f"Only return the topic, nothing else.", parse_model(get_model()))

    if "Title: " in completion:
        completion = completion[completion.find("Title: ") + 7:]
    completion = completion.replace('"', '')
    if "\n\n" in completion:
        completion = completion[completion.find("\n\n") + 2:]

    if not completion:
        error("Failed to generate Topic.")

    return completion


def generate_script(subject, language) -> str:
    """
    Generate a script for a video, depending on the subject of the video, the number of paragraphs, and the AI model.

    Args:
        subject (str): The subject of the video.
        language (str): The language of the video.

    Returns:
        script (str): The script of the video.
    """
    prompt = f"""
    Generate a script for a video in 4 sentences, depending on the subject of the video.

    The script is to be returned as a string with the specified number of paragraphs.

    Here is an example of a string:
    "This is an example string."

    Do not under any circumstance reference this prompt in your response.

    Get straight to the point, don't start with unnecessary things like, "welcome to this video" or "Sure here is a script".

    Obviously, the script should be related to the subject of the video.

    YOU MUST NOT EXCEED THE 4 SENTENCES LIMIT. MAKE SURE THE 4 SENTENCES ARE SHORT. LESS THAN 5000 CHARACTER IN TOTAL BUT MORE THAN 2000 CHARACTERS IN TOTAL.
    YOU MUST NOT INCLUDE ANY TYPE OF MARKDOWN OR FORMATTING IN THE SCRIPT, NEVER USE A TITLE.
    YOU MUST WRITE THE SCRIPT IN THE LANGUAGE SPECIFIED IN [LANGUAGE].
    ONLY RETURN THE RAW CONTENT OF THE SCRIPT. DO NOT INCLUDE "VOICEOVER", "NARRATOR" OR SIMILAR INDICATORS OF WHAT SHOULD BE SPOKEN AT THE BEGINNING OF EACH PARAGRAPH OR LINE. YOU MUST NOT MENTION THE PROMPT, OR ANYTHING ABOUT THE SCRIPT ITSELF. ALSO, NEVER TALK ABOUT THE AMOUNT OF PARAGRAPHS OR LINES. JUST WRITE THE SCRIPT

    Subject: {subject}
    Language: {language}
    """
    completion = generate_response(prompt, parse_model(get_model()))

    # Apply regex to remove *
    completion = re.sub(r"\*", "", completion)

    if not completion:
        error("The generated script is empty.")
        return ""

    if "\n\n" in completion:
        completion = completion[completion.find("\n\n") + 2:]

    return completion


def generate_metadata(subject, script, language) -> dict:
    """
    Generates Video metadata for the to-be-uploaded YouTube Short (Title, Description).

    Args:
        subject (str): The subject of the video.
        script (str): The script of the video.

    Returns:
        metadata (dict): The generated metadata.
    """
    title = generate_response(
        f"Please generate a YouTube Short Video Title for the following subject, including hashtags: {subject}. "
        f"Only return the title, nothing else. "
        f"Limit the title under 100 characters. "
        f"YOU MUST WRITE THE TITLE IN THE {language} LANGUAGE.", parse_model(get_model()))
    title = title.replace('"', '')
    title = title.replace('\n\n', '')

    description = generate_response(
        f"Please generate a YouTube Short Video Description for the following script: {script}. "
        f"Only return the description, nothing else."
        f"YOU MUST WRITE THE DESCRIPTION IN THE {language} LANGUAGE.", parse_model(get_model())
    )

    description = description.replace('"', '')
    if "\n\n" in description:
        description = description[description.find("\n\n") + 2:]

    metadata = {
        "title": title,
        "description": description
    }

    return metadata


def generate_image_prompts(script, subject, n_prompts) -> List[str]:
    """
    Generates AI Image Prompts based on the provided Video Script.

    Args:
        script (str): The script to generate prompts for.
        subject (str): The subject of the video.

    Returns:
        image_prompts (List[str]): Generated List of image prompts.
    """

    prompt = f"""
    Generate {n_prompts} Image Prompts for AI Image Generation,
    depending on the subject of a video.
    Subject: {subject}

    The image prompts are to be returned as
    a JSON-Array of strings.

    Each search term should consist of a full sentence,
    always add the main subject of the video.

    Be emotional and use interesting adjectives to make the
    Image Prompt as detailed as possible.

    YOU MUST ONLY RETURN THE JSON-ARRAY OF STRINGS.
    YOU MUST NOT RETURN ANYTHING ELSE. 
    YOU MUST NOT RETURN THE SCRIPT.

    The search terms must be related to the subject of the video.
    Here is an example of a JSON-Array of strings:
    ["image prompt 1", "image prompt 2", "image prompt 3"]

    For context, here is the full text:
    {script}
    """

    completion = str(generate_response(prompt, parse_model(get_image_prompt_llm()))) \
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

    success(f"Generated {len(image_prompts)} Image Prompts.")

    return image_prompts


def generate_image(prompt: str) -> str:
    """
    Generates an AI Image based on the given prompt.

    Args:
        prompt (str): Reference for image generation

    Returns:
        path (str): The path to the generated image.
    """
    ok = False
    while not ok:
        url = f"https://hercai.onrender.com/{get_image_model()}/text2image?prompt={prompt}"

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

            if get_verbose():
                info(f" => Generated Image: {image_url}")

            image_path = os.path.join(ROOT_DIR, "temp", str(uuid4()) + ".png")

            with open(image_path, "wb") as image_file:
                # Write bytes to file
                image_r = requests.get(image_url)

                image_file.write(image_r.content)

            if get_verbose():
                info(f" => Wrote Image to \"{image_path}\"\n")

            return image_path


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
