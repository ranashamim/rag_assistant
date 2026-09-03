from openai import OpenAI

client = OpenAI(base_url="https://api.gapgpt.app/v1", api_key="sk-768E5nQEZXgTdFS9UfdtCh1UQuyB1jvuhxKS3aw4GQPt3Vql")

response = client.chat.completions.create(
    model="deepseek-v4-flash",
    messages=[{"role": "user", "content": "سلام!"}]
)
print(response.choices[0].message.content)