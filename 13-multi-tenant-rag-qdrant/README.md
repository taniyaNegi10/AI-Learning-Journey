# Day 13 — Multi-Tenant RAG with Qdrant

> Building my AI engineering skills by learning concepts and implementing them through hands-on projects.

## 📌 Overview

In this project, I learned how to build a **multi-tenant retrieval system using Qdrant**.

A multi-tenant system allows multiple users or organizations to use the same application while keeping their data logically separated.

For example:

- **Tenant A** → Python-related documents
- **Tenant B** → Java-related documents

When Tenant A performs a search, the system should retrieve information only from Tenant A's documents.

This project demonstrates how **Qdrant payload filtering** can be used to achieve tenant-aware document retrieval.

---

## 🎯 What I Learned

Through this implementation, I learned:

- What multi-tenancy means in AI applications
- Why data isolation is important in multi-user systems
- How Qdrant stores vector embeddings
- How to store metadata using Qdrant payloads
- How to filter vector searches using `tenant_id`
- How `Filter`, `FieldCondition`, and `MatchValue` work
- How semantic search works with embeddings
- How tenant-aware retrieval can be used in RAG applications

---

## 🧠 What is Multi-Tenant RAG?

A **multi-tenant RAG system** allows multiple users or organizations to use the same RAG application while retrieving information only from their own documents.

### Example

Imagine an AI chatbot used by two companies:

```text
Company A
 ├── HR Policy
 ├── Leave Policy
 └── Employee Handbook

Company B
 ├── HR Policy
 ├── Salary Policy
 └── Company Guidelines

 Both tenants can use the same vector database, but when Tenant A performs a search, the system should retrieve information only from Tenant A's documents.

To achieve this, every document is stored with a tenant_id in its Qdrant payload. During retrieval, a metadata filter is applied so that the vector search is restricted to the requested tenant.

This project focuses on implementing the tenant-aware retrieval layer, which can serve as a foundation for a complete multi-tenant RAG application.


## Learning Objectives

Through this project, I learned and practiced:

Multi-tenancy in AI applications
Tenant-level data isolation
Vector databases
Semantic search
Text embeddings
Qdrant collections and points
Qdrant payloads
Metadata-based filtering
Tenant-aware vector retrieval
The role of tenant filtering in RAG systems

🧠 What is Multi-Tenant RAG?

Multi-Tenant RAG refers to a Retrieval-Augmented Generation architecture where multiple users or organizations can use the same AI application while retrieval is restricted to the documents belonging to the appropriate tenant.

                         User
                           │
                           ▼
                         Query
                           │
                           ▼
                  Generate Embedding
                           │
                           ▼
                        Qdrant
                           │
                    Tenant Filtering
                           │
                           ▼
               Relevant Tenant Documents
                           │
                           ▼
                          LLM
                           │
                           ▼
                    Final Answer



🏗️ Architecture
                         ┌───────────────────┐
                         │    User Query     │
                         └─────────┬─────────┘
                                   │
                                   ▼
                      ┌────────────────────────┐
                      │ Sentence Transformer   │
                      │   all-MiniLM-L6-v2      │
                      └────────────┬───────────┘
                                   │
                                   ▼
                          Query Embedding
                                   │
                                   ▼
                       ┌──────────────────────┐
                       │       Qdrant         │
                       │    Vector Database   │
                       └──────────┬───────────┘
                                  │
                                  ▼
                       ┌──────────────────────┐
                       │    Tenant Filter     │
                       │   tenant_id = X      │
                       └──────────┬───────────┘
                                  │
                                  ▼
                     Relevant Tenant Documents
                                  │
                                  ▼
                          Retrieved Results

🔍 How the System Works
1. Create Tenant-Specific Documents
Tenant A
├── Python programming
└── Python libraries

Tenant B
├── Java programming
└── Java Virtual Machine

2. Generate Embeddings

Each document is converted into a numerical vector using the all-MiniLM-L6-v2 sentence-transformer model.

Text
 ↓
Embedding Model
 ↓
[0.021, -0.183, 0.094, ...]
 ↓
384-dimensional vector

3. Store Vectors in Qdrant
ID
Vector
Payload

4. Convert the User Query into an Embedding
"What libraries does Python support?"

5. Apply Tenant Filtering
tenant_id = tenant_A

6. Perform Semantic Search

Qdrant compares the query vector with stored vectors and retrieves the most semantically similar documents that also satisfy the tenant filter.

7. Return Tenant-Specific Results

Only documents belonging to the requested tenant are returned.


🛠️ Tech Stack
Technology	               Purpose
Python         	        Core programming language
Qdrant	               Vector database
Qdrant Client	         Python client for interacting with Qdrant
Sentence Transformers	 Text embedding generation
all-MiniLM-L6-v2	     Embedding model
Cosine Similarity	    Vector similarity measurement
Git & GitHub         Version control and project documentation


⚙️ Installation
Clone the Repository
git clone https://github.com/taniyaNegi10/AI-Learning-Journey.git


Navigate to the Project
cd AI-Learning-Journey/13-multi-tenant-rag-qdrant

Activate the Virtual Environment
source ../.venv/bin/activate


Install Dependencies
pip install -r requirements.txt

💡 Key Learning

One of the main lessons from this project is that semantic similarity alone is not enough for multi-tenant retrieval.

A vector database may contain documents belonging to many different users or organizations.

Therefore, retrieval needs to consider both:

Semantic Relevance
       +
Tenant Metadata
       ↓
Tenant-Aware Retrieval

This allows the system to find semantically relevant information while restricting the search to a particular tenant.


.

🔒 Security Considerations

The tenant filter implemented here demonstrates the retrieval-level concept of tenant isolation.

In a production application, the tenant filter should not be considered the only security mechanism.

A production-ready multi-tenant system would additionally require:

Authentication
Authorization
Server-side tenant identification
Access-control validation
Secure document ingestion
Tenant ownership checks
API security
Database security
Monitoring and auditing

This project is a learning implementation of tenant-aware retrieval rather than a complete production security architecture.


.

🚀 Future Improvements

The current implementation focuses on the multi-tenant retrieval layer.

Planned improvements include:

Connect retrieved context to an LLM
Build a complete RAG pipeline
Add document upload functionality
Support PDF, DOCX and TXT documents
Implement automatic document chunking
Automatically associate uploaded documents with tenants
Build a FastAPI backend
Add authentication and authorization
Use persistent Qdrant storage
Add conversation history
Build a frontend chat interface
Deploy the complete application

