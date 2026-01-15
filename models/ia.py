from google import genai
from google.api_core import retry
from google.genai import types

# retry: https://github.com/google-gemini/cookbook/blob/main/quickstarts/Error_handling.ipynb


@retry.Retry(predicate=retry.if_transient_error, timeout=120)
def call(user_prompt: dict, config: dict):
    try:
        client = genai.Client(http_options={"api_version": "v1"})

        response = client.models.generate_content(
            model=config["model"],
            contents=user_prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                system_instruction=config["system_prompt"],
                temperature=2.0,
                response_json_schema=config["response_json_schema"],
            ),
        )

        return response.parsed

    finally:
        client.close()
