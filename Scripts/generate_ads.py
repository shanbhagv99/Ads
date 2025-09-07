import openai
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Example product
product = "Wireless Noise-Cancelling Headphones"

prompt = f"""
Generate 3 variations of ad copy for {product}. 
Each should be short, engaging, and optimized for conversions.
Provide outputs as a bullet list.
"""

response = openai.chat.completions.create(
    model="gpt-4.1",
    messages=[{"role": "system", "content": "You are a digital marketing expert."},
              {"role": "user", "content": prompt}],
    temperature=0.7
)

print("Generated Ad Copy:\n", response.choices[0].message.content)
