import os
from uuid import uuid4

import requests

from utils.config import get_verbose
from utils.status import info


def generate_image(prompt: str, image_model: str, generation_path: str) -> str:
    """
    Generates an AI Image based on the given prompt.

    Args:
        prompt (str): Reference for image generation

    Returns:
        path (str): The path to the generated image.
    """
    ok = False
    while not ok:
        url = f"https://hercai.onrender.com/{image_model}/text2image?prompt={prompt}"

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
            image_path = os.path.join(generation_path, str(uuid4()) + ".png")

            with open(image_path, "wb") as image_file:
                # Write bytes to file
                image_r = requests.get(image_url)

                image_file.write(image_r.content)

            if get_verbose():
                info(f" => Wrote Image to \"{image_path}\"\n")

            return image_path