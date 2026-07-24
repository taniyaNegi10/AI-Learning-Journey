import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from the .env file
load_dotenv()

# Read the Groq API key from the .env file
my_api_key = os.getenv("GROQ_API_KEY")

# Check whether the API key exists
if not my_api_key:
    raise ValueError("❌ API key not found! Please check your .env file.")

# Create the Groq client
client = Groq(api_key=my_api_key)

# Send a prompt to the LLM
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explain Large Language Models in simple terms."
        }
    ],
    model="llama-3.3-70b-versatile",
    temperature=0.7
)

# Print the AI response
print(chat_completion.choices[0].message.content)