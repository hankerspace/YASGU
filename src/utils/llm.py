import g4f

from utils.status import error

def generate_response(prompt: str, model: any, max_retry = 10) -> str:
    """
    Generates an LLM Response based on a prompt and the user-provided model.

    Args:
        prompt (str): The prompt to use in the text generation.
        model (any): The model to use for the generation.
        max_retry (int): The maximum amount of retries to generate the response.

    Returns:
        response (str): The generated AI Response.
    """

    response = ""
    retry = 0
    while not response:
        if retry > max_retry:
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
