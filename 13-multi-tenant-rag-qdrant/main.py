from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from qdrant_client.models import Distance, VectorParams
from qdrant_client.models import(
    Distance,
    VectorParams,
    PointStruct,#creating one point that we store in qdrant
    Filter,
    FieldCondition ,#which field we wantt to filter
    MatchValue
)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create local Qdrant client
client = QdrantClient(":memory:")


# Collection name
COLLECTION_NAME = "multi_tenant_documents"

# Embedding size for all-MiniLM-L6-v2
EMBEDDING_SIZE = 384


# Create Qdrant collection
client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(
        size=EMBEDDING_SIZE,
        distance=Distance.COSINE,
    ),
)


print(f"Collection '{COLLECTION_NAME}' created successfully!")

#now we will create a sample documents for different tenants
documents = [
    {
         "id": 1,
        "tenant_id": "tenant_A",
        "text": "Python is a popular programming language used for AI and machine learning."
    },


{
    "id":2,
    "tenant_id": "tenant_A",
    "text":"java is an object-orientated programmming language used for enterprise application."
},

{
    "id":3,
    "tenant_id":"tenant_B",
    "text": "java is an object-oriented programming language commonly used for enterprise application."

},
{
    "id":4,
    "tenant_id":"tenant_B",
    "text":"java application commonly run on the java Virtual Machine,also known as JVM."
}

]

#convert the text into embedding

from qdrant_client.models import PointStruct
points = []

for document in documents:
    vector = model.encode(document["text"]).tolist()

    point = PointStruct(
        id=document["id"],
        vector=vector,
        payload={
            "tenant_id":document["tenant_id"],
            "text":document["text"]
        }
    )

    points.append(point)

    client.upsert(
    collection_name=COLLECTION_NAME,
    points=points
)

print(f"Inserted {len(points)} documents into Qdrant!")

query = "What Libraries does Python support?"

query_vector = model.encode(query).tolist()


#create tenant filter
tenant_filter = Filter(
    must=[
        FieldCondition(
            key="tenant_id",
            match=MatchValue(value="tenant_A")
        )
    ]
)

#search qdrant

results = client.query_points(
    collection_name= COLLECTION_NAME,
    query=query_vector,
    query_filter=tenant_filter,
    limit=2
).points

print("\nSearch Results:")

for result in results:
    print("\nScore:",result.score)
    print("Tenant:",result.payload["tenant_id"])
    print("Text:",result.payload["text"])








    
    