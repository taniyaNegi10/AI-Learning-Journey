# 📚 Day 14 — Text Chunking with LangChain

> **Learning AI by Building Real Projects 🚀**

Today I learned about **Text Chunking**, an important preprocessing step in **Retrieval-Augmented Generation (RAG)** systems.

When documents are large, sending the entire document to an LLM is not always practical. **Text chunking** divides a large document into smaller pieces so that relevant information can be processed and retrieved more effectively.

In this project, I implemented and compared three different chunking approaches using **LangChain**:

- 🔹 Fixed-Size Chunking
- 🔹 Paragraph Chunking
- 🔹 Recursive Chunking

---

## 🎯 Learning Objectives

Through this project, I learned:

- What text chunking is
- Why chunking is important in RAG
- How LangChain text splitters work
- How different chunking strategies produce different chunks
- The role of `chunk_size`
- The role of `chunk_overlap`
- The role of `separator`
- How recursive chunking differs from basic character-based splitting

---

# 🔹 1. Fixed-Size Chunking

Fixed-size chunking divides a document into chunks based on a specified target size.

For this implementation, I used LangChain's `CharacterTextSplitter`.

### ⚙️ Configuration

```python
fixed_splitter = CharacterTextSplitter(
    separator="",
    chunk_size=200,
    chunk_overlap=50
)

fixed_chunks = fixed_splitter.split_text(text)

🧠 How It Works
Large Document
      ↓
   Chunking
      ↓
┌─────────────┐
│   Chunk 1   │
├─────────────┤
│   Chunk 2   │
├─────────────┤
│   Chunk 3   │
├─────────────┤
│   Chunk 4   │
└─────────────┘

The configured target chunk_size is 200, with an overlap of 50 between neighboring chunks.

🔁 Chunk Overlap

The overlap allows some content from the previous chunk to appear in the next chunk.

Chunk 1
┌──────────────────────────────┐
│ Previous information         │
│ Shared context               │
└──────────────────────────────┘
               ↓
          50 overlap
               ↓
Chunk 2
┌──────────────────────────────┐
│ Shared context               │
│ New information              │
└──────────────────────────────┘
💡 Observation

Fixed-size chunking is simple and predictable.

However, because the splitting is based primarily on size, a sentence or idea can sometimes be divided between two chunks.



🔹 2. Paragraph Chunking

Paragraph chunking uses paragraph boundaries to divide the document.

For this implementation, I used CharacterTextSplitter with:

paragraph_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=1000,
    chunk_overlap=0
)

paragraph_chunks = paragraph_splitter.split_text(text)
📌 Separator
separator="\n\n"

The \n\n separator represents a blank line between paragraphs in the text file.

🧠 How It Works
Large Document
      ↓
Paragraph Boundaries
      ↓
Paragraph-Based Chunks

For example:

Paragraph 1
      ↓
Paragraph 2
      ↓
Paragraph 3

The splitter uses these paragraph boundaries while creating chunks according to the configured chunk size.

💡 Observation

Paragraph chunking helps preserve the natural structure of the document.

However, multiple paragraphs can still be present in the same chunk when they fit within the configured chunk_size.



🔹 3. Recursive Chunking

Recursive chunking uses a hierarchy of separators to divide text while trying to preserve larger text structures when possible.

For this implementation, I used:

recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=50
)

recursive_chunks = recursive_splitter.split_text(text)
🧠 How It Works

Conceptually, recursive splitting works through increasingly smaller text boundaries:

Large Document
      ↓
   Paragraph
      ↓
    Line
      ↓
   Smaller Text
      ↓
     Chunk

Instead of immediately cutting the text at an arbitrary position, the splitter works through its available splitting boundaries to create chunks close to the desired size.

💡 Observation

Recursive chunking can create more natural text boundaries than simply splitting text based on a fixed position.

It is especially useful when working with documents that contain different levels of text structure.

Note: Recursive chunking uses splitting rules; it does not actually understand the semantic meaning of the text.


## 📊 Chunking Comparison

| Chunking Method | Main Idea | Advantage | Limitation |
|---|---|---|---|
| 🔹 Fixed-Size | Split based on target size | Simple and predictable | Can split sentences or ideas |
| 🔹 Paragraph | Uses paragraph boundaries | Preserves paragraph structure | Chunks can become larger |
| 🔹 Recursive | Uses multiple text boundaries | Can create more natural chunks | More complex than basic splitting |

