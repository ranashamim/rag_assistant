from groq import Groq

from app.config.settings import settings


client = Groq(api_key=settings.groq_api_key)


def generate_response(prompt: str):

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content

