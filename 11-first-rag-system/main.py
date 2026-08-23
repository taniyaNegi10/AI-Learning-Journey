

import os

from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Load environment variables
load_dotenv()


# Read Groq API key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found!")


# Create Groq client
client = Groq(api_key=api_key)


# LLM model
model = "openai/gpt-oss-20b"


# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


# Knowledge Base
knowledge_base = [
    "Machine Learning is a branch of artificial intelligence that enables computers to learn patterns from data.",

    "Deep Learning is a subset of machine learning that uses neural networks with multiple layers.",

    "Natural Language Processing, also known as NLP, enables computers to understand and process human language.",

    "RAG stands for Retrieval-Augmented Generation and combines information retrieval with large language models.",

    "Embeddings convert text into numerical vectors that capture semantic meaning.",

    "Cosine similarity measures how similar two embedding vectors are.",

    "Python is one of the most commonly used programming languages in artificial intelligence and machine learning.",

    "A vector database stores and searches embedding vectors efficiently."
]


# Create embeddings for the knowledge base
document_embeddings = embedding_model.encode(knowledge_base)


# Retrieve the most relevant information
def retrieve_information(question):

    # Convert the user's question into an embedding
    question_embedding = embedding_model.encode(question)

    # Compare question embedding with all document embeddings
    similarity_scores = cosine_similarity(
        [question_embedding],
        document_embeddings
    )[0]

    # Find the index of the highest similarity score
    most_relevant_index = similarity_scores.argmax()

    # Retrieve the most relevant document
    most_relevant_document = knowledge_base[most_relevant_index]

    return most_relevant_document


# Send the question and retrieved context to the LLM
def ask_llm(question, context):

    system_message = {
        "role": "system",
        "content": f"""
You are a helpful AI assistant.

Answer the user's question using only the provided context.

Context:
{context}
"""
    }

    user_message = {
        "role": "user",
        "content": question
    }

    response = client.chat.completions.create(
        model=model,
        messages=[system_message, user_message]
    )

    return response.choices[0].message.content


# User question
question = "What allows computers to understand human language?"


# Retrieve relevant information
context = retrieve_information(question)


# Display question
print("Question:")
print(question)


# Display retrieved information
print("\nRetrieved Information:")
print(context)


# Generate final answer
answer = ask_llm(question, context)


# Display AI response
print("\nAI Response:")
print(answer)

 









