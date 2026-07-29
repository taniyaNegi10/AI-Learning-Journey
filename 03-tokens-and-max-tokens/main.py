
import os
from dotenv import load_dotenv
from groq import Groq

# Load API key
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("API Key not found!")

client = Groq(api_key=api_key)

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": "Explain Artificial Intelligence in simple terms."
        }
    ],
    max_completion_tokens=200
)

print(response.choices[0].message.content)

#max completion = how long should the answer be
#IT TELLS the model that u are not allowed to generate more than this many tokens.