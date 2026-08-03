# Streaming refers to the practice of generating AI responses
# incrementally in real time (token streaming),
# rather than waiting for the full answer.
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

model = "llama-3.3-70b-versatile"
prompt = "explain how internet works."
message={
    "role" : "user",
    "content" : prompt
}
messages = [message]

stream=client.chat.completions.create(
    model=model,
    messages=messages,
    stream=True)


for chunk in stream:#answers come in the form of chunks not at once
    content = chunk.choices[0].delta.content#from chunks answer 
    if content:
        print(content,end="",flush=True)#suddenly print with chunks


