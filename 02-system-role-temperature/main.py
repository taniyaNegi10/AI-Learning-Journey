
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Read API key
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key not found!")

# Create Groq client
client = Groq(api_key=my_api_key)

# Model
model = "llama-3.3-70b-versatile"

messages = [
    {
        "role": "system",
        "content": "You are  a  software engineer at google."
    },
    {
        "role": "user",
        "content": "guide me."
    }
]

#generate response by temperature


response = client.chat.completions.create(
    model=model,
    messages=messages,
    temperature=1
)
#print ai response
print(response.choices[0].message.content)