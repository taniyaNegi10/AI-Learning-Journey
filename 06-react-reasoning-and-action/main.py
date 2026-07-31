

import os  #python bring the library 
import re # regular expression
from time import sleep #this pauses the program
from dotenv import load_dotenv#read .env file
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

#tools
def get_product_price(product):

    product = product.lower()

    if product == "iphone 17":
        return 1000

    elif product == "iphone 15":
        return 500

    else:
        return 0


def calculator(expression):
    try:
        return eval(expression)
    except:
        return "calc error!"

tools = {
    "get_product_price": get_product_price,
    "calculator": calculator
}

system_prompt = """
you are a shopping assistant

u have these tools:

get_product_price(product)
calculator(expression)

important:

call tools exactly like these examples:

Action: get_product_price("iphone 17")
Action: calculator("5000 - 1000")

Never write:

get_product_price(product="iphone 17")

Never write:

calculator(expression="5000 - 1000")

follow these rules:

1. decide what u need to do next.
2. Call ONLY one tool at a time.
3. after writing an action, stop immediately.
4. Never guess or invent a tool result.
5. wait until you receive an observation.
6. then decide your next action.
7. when the task is complete, give the final answer.

format:

Thought: what you need to do
Action: tool_name(argument)

when finished:

Final Answer: your answer
"""

def run_agent(question):

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": question
        }
    ]

    for step in range(5): #try at most 5 times#allow the agent up to 5 reasoning steps

        print("\n----------------")
        print("Step", step + 1)
        print("----------------")

        response = client.chat.completions.create( #SEND conversation to groq
            model=model,
            messages=messages,
            temperature=0
        )

        answer = response.choices[0].message.content

        print(answer)

        #agent has finished
        if "Final Answer:" in answer:
            break

        #find the action
        match = re.search(
            r'Action:\s*(\w+)\((.*?)\)',
            answer
        )

        if match:

            tool_name = match.group(1)
            tool_input = match.group(2)

            tool_input = tool_input.strip()
            tool_input = tool_input.strip('"')

            #run the tool
            if tool_name in tools:

                tool = tools[tool_name]
                observation = tool(tool_input)

            else:

                observation = "tool not found"

            #add llm response to memory
            messages.append({
                "role": "assistant",
                "content": answer
            })

            messages.append({
                "role": "user",
                "content": f"Observation: {observation}"
            })

        sleep(2)

run_agent("I have 5000 rupees. Can I buy an iPhone 17?")