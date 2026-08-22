from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity




#load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

#sentences
sentences = [
    "I love programming.",
    "Coding is something I enjoy.",
    "I enjoy eating pizza."
   
]

#convert text into embeddings

embeddings = model.encode(sentences)


#display sentences and embeddings
for sentence,embedding in zip(sentences,embeddings):
    print(sentence, "->",embedding)

#compare sentence 1 and sentence 2
similarity_1 = cosine_similarity(
    [embeddings[0]],
    [embeddings[1]]
)

#compare sentence 1 and sentence 3
similarity_2 = cosine_similarity(
    [embeddings[0]],
    [embeddings[2]]

)

print("\nSimilarity between:")
print(sentences[0])
print("and")
print(sentences[1])
print("Score:",similarity_1[0][0])

print("\nSimilarity between:")
print(sentences[0])
print("and")
print(sentences[2])
print("Score",similarity_2[0][0])





