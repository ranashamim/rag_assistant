from groq import Groq

from app.config.settings import settings

from openai import OpenAI

client = OpenAI(base_url="https://api.gapgpt.app/v1", api_key=settings.gap_api_key)


def generate_response(prompt: str):
    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
    )
    return response.choices[0].message.content