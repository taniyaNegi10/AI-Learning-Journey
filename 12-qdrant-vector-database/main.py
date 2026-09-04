import os

from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
from groq import Groq



#  Load environment variables


load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")



#  Connect to Qdrant Cloud


client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

print("Connected to Qdrant Cloud!")

#  Connect to Groq


groq_client = Groq(
    api_key=GROQ_API_KEY
)

print("Connected to Groq!")


#  Load embedding model


print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model ready!")


#  Create Qdrant collection


COLLECTION_NAME = "knowledge"
EMBEDDING_SIZE = 384#our embedding model produces vector containing 384 number

if client.collection_exists(COLLECTION_NAME):
    print(f"Deleting existing collection: {COLLECTION_NAME}")
    client.delete_collection(COLLECTION_NAME)


client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(
        size=EMBEDDING_SIZE,
        distance=Distance.COSINE,
    ),
)

print(f"Created collection: {COLLECTION_NAME}")
print(f"Vector size: {EMBEDDING_SIZE}")
print("Distance: Cosine")


#  Load knowledge from knowledge.txt


with open("knowledge.txt", "r", encoding="utf-8") as f:

    documents = [
        line.strip()
        for line in f
        if line.strip()
    ]

print(f"Loaded {len(documents)} documents")



#  Generate embeddings


embeddings = model.encode(documents)

print(f"Generated {len(embeddings)} embeddings")
print(f"Embedding size: {len(embeddings[0])}")


# 8. Create Qdrant points


points = []

for i, embedding in enumerate(embeddings):

    point = PointStruct(
        id=i + 1,#i = 0 ,id = 1
        #i = 2, id = 2
        vector=embedding.tolist(),
        payload={
            "text": documents[i]
        }
    )

    points.append(point)


#  Upload points to Qdrant


client.upsert(
    collection_name=COLLECTION_NAME,
    points=points
)

print(f"Uploaded {len(points)} documents to Qdrant!")



#  Search Qdrant


def search(query, top_k=3):

    query_vector = model.encode(query).tolist()

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
        with_payload=True,
    ).points

    return results



#  Generate answer using Groq


def generate_answer(query, results):

    # Extract text from Qdrant results
    context = "\n\n".join(
        result.payload["text"]
        for result in results
    )

    prompt = f"""
You are a helpful AI assistant.

Answer the user's question using ONLY the provided context.

If the answer cannot be found in the context, say:
"I don't have enough information in the provided knowledge."

Context:
{context}

User Question:
{query}

Answer:
"""

    response = groq_client.chat.completions.create(

        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "You answer questions using retrieved context."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content



#  Ask a question


query = "Why is Qdrant vector database useful for RAG?"

results = search(query, top_k=3)


#  Display retrieved documents


print("\n" + "=" * 60)
print("RETRIEVED DOCUMENTS")
print("=" * 60)

for result in results:

    print(f"\nScore: {result.score:.3f}")
    print(f"Text: {result.payload['text']}")



#  Generate final answer


answer = generate_answer(query, results)


print("\n" + "=" * 60)#repeat 60 times ---final answer ---just formatting or decoration to make the output easier to terminal
print("FINAL ANSWER")
print("=" * 60)

print(answer)



   















