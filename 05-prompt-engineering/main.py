
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

#now we are making a function jismai hum prompt pass krenge and uske according output milega
#llm function
def llm_ans(prompt):
    messages = {
        "role": "user",
        "content": prompt
    }

    messages = [messages]

    response = client.chat.completions.create(
        model=model,      # Fixed: model1 -> model
        messages=messages
    )

    ans = response.choices[0].message.content
    return ans

good_prompt="""

#role:

you are a support assistant at a mobile/laptop company

#task

u have to classify this category

#constraint

u have to classify the isssue one of three categories namely billing,techincal,return
#output format

your answer should be in 5 lines

this is a user complaint:

my laptop is not working

"""



#bad_prompt = """
#this is a user complaint:
#my laptop is not working
##classify this


print(llm_ans(good_prompt))

