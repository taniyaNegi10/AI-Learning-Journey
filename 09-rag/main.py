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


model = "openai/gpt-oss-20b"



# Our small knowledge base
knowledge_base = """
Shraddha Khapra is a co-founder of Apna College.

Apna College is an online educational platform that provides courses
related to programming, computer science, and technology.

RAG stands for Retrieval-Augmented Generation.

RAG retrieves relevant information before sending the context to an LLM.

RAG helps an LLM answer questions using external or private information.
"""


# Function to retrieve relevant information
def retrieve_information(question):

    question_words = question.lower().split()
    relevant_information = []

    for line in knowledge_base.split("\n"):

        for word in question_words:

            if word in line.lower():
                if line not in relevant_information:
                      relevant_information.append(line)
  
                

    return "\n".join(relevant_information)


# Function to ask the LLM
def ask_llm(question):

    # Retrieve relevant information
    context = retrieve_information(question)

    system_message = {
        "role": "system",
        "content": f"""
You are a helpful AI assistant.

Use the following retrieved context to answer the user's question.

Context:
{context}

If the answer is not available in the context,
say that the information is not available.
"""
    }

    user_message = {
        "role": "user",
        "content": question
    }

    messages = [system_message, user_message]

    response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    answer = response.choices[0].message.content

    return answer


question = "Who is Shraddha Khapra?"

print("Question:")
print(question)

print("\nRetrieved Information:")
print(retrieve_information(question))

print("\nAI Response:")
print(ask_llm(question))



