import json
import os
import sys

from termcolor import colored

ROOT_DIR = os.path.dirname(sys.path[0])


def assert_folder_structure() -> None:
    """
    Make sure that the necessary folder structure is present.

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


def get_headless() -> bool:
    """
    Gets the headless flag from the config file.

    Returns:
        headless (bool): The headless flag
    """
    with open(os.path.join(ROOT_DIR, "config/config.json"), "r") as file:
        return json.load(file)["headless"]


def get_generators() -> list:
    """
    Gets the list of generators from the config file.

    Returns:
        generators (list): The list of generators
    """
    with open(os.path.join(ROOT_DIR, "config/config.json"), "r") as file:
        return json.load(file)["generators"]


def get_threads() -> int:
    """
    Gets the amount of threads to use for example when writing to a file with MoviePy.

    Returns:
        threads (int): Amount of threads
    """
    with open(os.path.join(ROOT_DIR, "config/config.json"), "r") as file:
        return json.load(file)["threads"]


def get_assemblyai_api_key() -> str:
    """
    Gets the AssemblyAI API key.

    Returns:
        key (str): The AssemblyAI API key
    """
    with open(os.path.join(ROOT_DIR, "config/config.json"), "r") as file:
        return json.load(file)["assembly_ai_api_key"]


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
