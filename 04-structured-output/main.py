import os  # Read environment variables
import json  # Convert JSON text into a Python dictionary
from dotenv import load_dotenv  # Load .env file
from groq import Groq  # Connect to Groq API
from pydantic import BaseModel  # Creates a schema for validation

# Pydantic Schema

class Student(BaseModel):
    name: str
    age: int
    branch: str
    college: str



# Load API Key

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("API Key not found!")

client = Groq(api_key=api_key)



# Send Prompt to LLM

response = client.chat.completions.create( #api call
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": """
Generate details of a Computer Science student.

Return ONLY valid JSON in this format:

{
    "name": "string",
    "age": integer,
    "branch": "string",
    "college": "string"
}
"""
        }
    ]
)



# Extract AI Response

llm_output = response.choices[0].message.content #llm return text

print("Raw LLM Output:\n")
print(llm_output)



# Convert JSON to Python Dictionary

student_data = json.loads(llm_output)



# Validate using Pydantic

student = Student(**student_data)



# Print Structured Output

print("\nValidated Student Object\n")

print(f"Name     : {student.name}")
print(f"Age      : {student.age}")
print(f"Branch   : {student.branch}")
print(f"College  : {student.college}")