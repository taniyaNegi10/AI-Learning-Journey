
from langchain_text_splitters import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter
)

with open("knowledge.txt", "r") as file:
    text = file.read()


# 1. Fixed-Size Chunking
fixed_splitter = CharacterTextSplitter(
    separator="",
    chunk_size=200,
    chunk_overlap=50
)

fixed_chunks = fixed_splitter.split_text(text)

print("\n========== FIXED-SIZE CHUNKING ==========\n")

for i, chunk in enumerate(fixed_chunks, start=1):
    print(f"CHUNK {i}:")
    print(chunk)
    print()

# 2. Paragraph Chunking
paragraph_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=1000,
    chunk_overlap=0
)

paragraph_chunks = paragraph_splitter.split_text(text)

print("\n========== PARAGRAPH CHUNKING ==========\n")

for i, chunk in enumerate(paragraph_chunks, start=1):
    print(f"CHUNK {i}:")
    print(chunk)
    print()

# 3. Recursive Chunking
recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=50
)

recursive_chunks = recursive_splitter.split_text(text)

print("\n========== RECURSIVE CHUNKING ==========\n")

for i, chunk in enumerate(recursive_chunks, start=1):
    print(f"CHUNK {i}:")
    print(chunk)
    print()












