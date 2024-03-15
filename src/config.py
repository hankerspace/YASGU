import os
import sys
import json
import srt_equalizer

from termcolor import colored

ROOT_DIR = os.path.dirname(sys.path[0])

def assert_folder_structure() -> None:
    """
    Make sure that the nessecary folder structure is present.

    Returns:
        None
    """
    # Create the temp folder
    if not os.path.exists(os.path.join(ROOT_DIR, "temp")):
        if get_verbose():
            print(colored(f"=> Creating temp folder at {os.path.join(ROOT_DIR, 'temp')}", "green"))
        os.makedirs(os.path.join(ROOT_DIR, "temp"))

def get_first_time_running() -> bool:
    """
    Checks if the program is running for the first time by checking if temp folder exists.

    Returns:
        exists (bool): True if the program is running for the first time, False otherwise
    """
    return not os.path.exists(os.path.join(ROOT_DIR, "temp"))

def get_verbose() -> bool:
    """
    Gets the verbose flag from the config file.

    Returns:
        verbose (bool): The verbose flag
    """
    with open(os.path.join(ROOT_DIR, "config/config.json"), "r") as file:
        return json.load(file)["verbose"]

def get_firefox_profile_path() -> str:
    """
    Gets the path to the Firefox profile.

    Returns:
        path (str): The path to the Firefox profile
    """
    with open(os.path.join(ROOT_DIR, "config/config.json"), "r") as file:
        return json.load(file)["firefox_profile"]

def get_headless() -> bool:
    """
    Gets the headless flag from the config file.

    Returns:
        headless (bool): The headless flag
    """
    with open(os.path.join(ROOT_DIR, "config/config.json"), "r") as file:
        return json.load(file)["headless"]

def get_model() -> str:
    """
    Gets the model from the config file.

    Returns:
        model (str): The model
    """
    with open(os.path.join(ROOT_DIR, "config/config.json"), "r") as file:
        return json.load(file)["llm"]

def get_twitter_language() -> str:
    """
    Gets the Twitter language from the config file.

    Returns:
        language (str): The Twitter language
    """
    with open(os.path.join(ROOT_DIR, "config/config.json"), "r") as file:
        return json.load(file)["twitter_language"]

def get_image_model() -> str:
    """
    Gets the Image MOdel from the config file.

    Returns:
        model (str): The image model
    """
    with open(os.path.join(ROOT_DIR, "config/config.json"), "r") as file:
        return json.load(file)["image_model"]

def get_threads() -> int:
    """
    Gets the amount of threads to use for example when writing to a file with MoviePy.

    Returns:
        threads (int): Amount of threads
    """
    with open(os.path.join(ROOT_DIR, "config/config.json"), "r") as file:
        return json.load(file)["threads"]
    
def get_image_prompt_llm() -> str:
    """
    Gets the image prompt for LLM from the config file.

    Returns:
        prompt (str): The image prompt
    """
    with open(os.path.join(ROOT_DIR, "config/config.json"), "r") as file:
        return json.load(file)["image_prompt_llm"]

def get_is_for_kids() -> bool:
    """
    Gets the is for kids flag from the config file.

    Returns:
        is_for_kids (bool): The is for kids flag
    """
    with open(os.path.join(ROOT_DIR, "config/config.json"), "r") as file:
        return json.load(file)["is_for_kids"]

def get_assemblyai_api_key() -> str:
    """
    Gets the AssemblyAI API key.

    Returns:
        key (str): The AssemblyAI API key
    """
    with open(os.path.join(ROOT_DIR, "config/config.json"), "r") as file:
        return json.load(file)["assembly_ai_api_key"]
    
def equalize_subtitles(srt_path: str, max_chars: int = 10) -> None:
    """
    Equalizes the subtitles in a SRT file.

    Args:
        srt_path (str): The path to the SRT file
        max_chars (int): The maximum amount of characters in a subtitle

    Returns:
        None
    """
    srt_equalizer.equalize_srt_file(srt_path, srt_path, max_chars)
    
def get_font() -> str:
    """
    Gets the font from the config file.

    Returns:
        font (str): The font
    """
    with open(os.path.join(ROOT_DIR, "config/config.json"), "r") as file:
        return json.load(file)["font"]

def get_fonts_dir() -> str:
    """
    Gets the fonts directory.

    Returns:
        dir (str): The fonts directory
    """
    return os.path.join(ROOT_DIR, "assets/fonts")

def get_imagemagick_path() -> str:
    """
    Gets the path to ImageMagick.

    Returns:
        path (str): The path to ImageMagick
    """
    with open(os.path.join(ROOT_DIR, "config/config.json"), "r") as file:
        return json.load(file)["imagemagick_path"]
