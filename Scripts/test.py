import os
from dotenv import load_dotenv
from openai import OpenAI

dotenv_path = r"C:\Users\shanb\OneDrive\Desktop\Ads.ai\.env"
load_dotenv(dotenv_path)

print("API key:", os.getenv("OPENAI_API_KEY"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.responses.create(
    model="gpt-4.1",
    input="Write a short bedtime story about a unicorn."
)

print(response.output_text)