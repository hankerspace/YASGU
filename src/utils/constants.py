"""
This file contains all the constants used in the program.
"""
import g4f

# YouTube Section
YOUTUBE_TEXTBOX_ID = "textbox"
YOUTUBE_MADE_FOR_KIDS_NAME = "VIDEO_MADE_FOR_KIDS_MFK"
YOUTUBE_NOT_MADE_FOR_KIDS_NAME = "VIDEO_MADE_FOR_KIDS_NOT_MFK"
YOUTUBE_NEXT_BUTTON_ID = "next-button"
YOUTUBE_RADIO_BUTTON_XPATH = "//*[@id=\"radioLabel\"]"
YOUTUBE_DONE_BUTTON_ID = "done-button"

def build_generate_topic_prompt(subject: str) -> str:
    return (f"Please generate a specific video idea that takes about the following topic: {subject}. "
            f"Make it exactly one sentence. "
            f"Be creative! Find a unique angle or perspective on the topic."
            f"Only return the topic, nothing else.")

def build_generate_script_prompt(topic: str, language: str) -> str:
    return (f"""
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

        Subject: {topic}
        Language: {language}
        """)

def build_generate_title_prompt(subject: str, language: str) -> str:
    return (f"Please generate a YouTube Short Video Title for the following subject, including hashtags: {subject}. "
    f"Only return the title, nothing else. "
    f"Limit the title under 80 characters. "
    f"YOU MUST WRITE THE TITLE IN THE {language} LANGUAGE.")

def build_generate_description_prompt(script: str, language: str) -> str:
    return (f"Please generate a YouTube Short Video Description for the following script: {script}. "
            f"Only return the description, nothing else."
             f"Limit the description under 300 characters. "
            f"YOU MUST WRITE THE DESCRIPTION IN THE {language} LANGUAGE.")

def build_generate_image_prompts(script: str, subject: str, n_prompts) -> str:
    return (f"""
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
        """)

def parse_model(model_name: str) -> any:
    if model_name == "gpt4":
        return g4f.models.gpt_4
    elif model_name == "gpt35_turbo":
        return g4f.models.gpt_35_turbo
    elif model_name == "llama2_7b":
        return g4f.models.llama2_7b
    elif model_name == "llama2_13b":
        return g4f.models.llama2_13b
    elif model_name == "llama2_70b":
        return g4f.models.llama2_70b
    elif model_name == "mixtral_8x7b":
        return g4f.models.mixtral_8x7b
    elif model_name == "dolphin_mixtral_8x7b":
        return g4f.models.dolphin_mixtral_8x7b
    elif model_name == "airoboros_70b":
        return g4f.models.airoboros_70b
    elif model_name == "airoboros_l2_70b":
        return g4f.models.airoboros_l2_70b
    elif model_name == "gemini":
        return g4f.models.gemini
    elif model_name == "claude_v2":
        return g4f.models.claude_v2
    elif model_name == "claude_3_sonnet":
        return g4f.models.claude_3_sonnet
    elif model_name == "claude_3_opus":
        return g4f.models.claude_3_opus
    else:
        # Default model is gpt3.5-turbo
        return g4f.models.gpt_35_turbo
