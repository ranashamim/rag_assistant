# RAG Assistant

A document-based **Retrieval-Augmented Generation (RAG)** assistant built with FastAPI, Qdrant, SQLite, and SQLAlchemy.

The project started as a basic vector-search RAG system and was progressively extended with multiple chunking strategies, hybrid retrieval, reranking, adaptive query routing, query transformation, parent-child retrieval, and persistent conversation history.

The main goal of the project is to understand and implement the core building blocks of **advanced/adaptive RAG** rather than relying on a single retrieval method.

---

## Features

### Document Processing

* PDF and TXT document parsing
* Page-aware document processing
* Multiple chunking strategies:

  * Fixed-size chunking
  * Punctuation-based chunking
  * Recursive chunking
  * Semantic chunking
  * Parent-child chunking
* Configurable chunk sizes and overlap
* Chunk metadata and document IDs

### Embeddings & Vector Search

* Sentence Transformers embeddings
* `intfloat/multilingual-e5-large`
* 1024-dimensional embeddings
* Normalized embeddings
* Qdrant vector database
* Cosine similarity search

### Retrieval

The project supports several retrieval approaches:

* Dense semantic retrieval
* BM25 keyword retrieval
* Hybrid retrieval
* Reciprocal Rank Fusion (RRF)
* Cross-encoder reranking


### Adaptive RAG

The system analyzes the user's query and selects a retrieval strategy.

Supported query types:

* `simple`
* `complex`
* `ambiguous`
* `broad`

Supported strategies:

| Query type | Strategy              |
| ---------- | --------------------- |
| Simple     | Normal retrieval      |
| Complex    | Query decomposition   |
| Ambiguous  | Query rewriting       |
| Broad      | Multi-query retrieval |

This allows the system to avoid using the same retrieval strategy for every question.

### Query Transformation

Implemented query transformation techniques include:

* Query rewriting
* Multi-query generation
* Query decomposition
* Conversation-aware rewriting

### Parent-Child Retrieval

The project implements parent-child chunking.

Children are used as the precise retrieval units, while the parent provides broader context.

The retrieval pipeline is:

```text
Query
  ↓
Retrieve child chunks
  ↓
Hybrid retrieval
  ↓
RRF
  ↓
Reranking
  ↓
Final child results
  ↓
Expand to parent chunks
  ↓
Build context
  ↓
LLM
```

This allows retrieval to remain precise while generation receives richer surrounding context.

### Conversation History

Conversation history is persisted using:

* SQLite
* SQLAlchemy ORM

---

# Architecture

The overall architecture can be summarized as:

```text
                         ┌──────────────┐
                         │     User     │
                         └──────┬───────┘
                                ↓
                         ┌──────────────┐
                         │   FastAPI    │
                         └──────┬───────┘
                                ↓
                    ┌────────────────────────┐
                    │ Conversation / History │
                    │    SQLite + SQLAlchemy │
                    └────────────┬───────────┘
                                 ↓
                         ┌──────────────┐
                         │ Query Router │
                         └──────┬───────┘
                                ↓
             ┌──────────────────┼──────────────────┐
             ↓                  ↓                  ↓
         Normal             Rewrite          Multi-query /
         Retrieval          Query             Decomposition
             │                  │                  │
             └──────────────────┼──────────────────┘
                                ↓
                    ┌─────────────────────┐
                    │ Hybrid Retrieval    │
                    │                     │
                    │ Dense + BM25        │
                    └──────────┬──────────┘
                               ↓
                         ┌───────────┐
                         │    RRF    │
                         └─────┬─────┘
                               ↓
                         ┌───────────┐
                         │ Reranker  │
                         └─────┬─────┘
                               ↓
                     ┌──────────────────┐
                     │ Parent Expansion │
                     └────────┬─────────┘
                              ↓
                     ┌──────────────────┐
                     │ Context Builder  │
                     └────────┬─────────┘
                              ↓
                         ┌──────────┐
                         │   LLM    │
                         └────┬─────┘
                              ↓
                     Answer + Citations
                              ↓
                    Save conversation
                         to SQLite
```

---

# Document Ingestion Pipeline

```text
Document
   ↓
PDF / TXT Parser
   ↓
Parsed Pages
   ↓
Chunking Strategy
   ↓
Chunk Objects
   ↓
Embedding
   ↓
Qdrant
```

For parent-child chunking:

```text
Document
   ↓
Parent Chunks
   ↓
Child Chunks
   ↓
Embed Child Chunks
   ↓
Store Retrieval Chunks in Qdrant
```

Parent chunks are retained separately so they can later be used to expand retrieved children into richer context.

# Database

The conversation database uses SQLite and SQLAlchemy.

## `conversations`

```text
conversation_id    PRIMARY KEY
created_at
```

## `messages`

```text
id                 PRIMARY KEY
conversation_id    FOREIGN KEY
role
content
created_at
```

Relationship:

```text
Conversation
     │
     │ one-to-many
     ↓
Messages
```

SQLAlchemy `selectinload()` is used to load conversation messages together with the conversation, avoiding detached lazy-loading problems after the database session is closed.

---

# Project Structure

The project is organized around separate services for parsing, chunking, embedding, retrieval, routing, generation, and persistence.

```text
app/
├── config/
│   └── settings.py
│
├── database/
│   ├── database.py
│   └── models.py
│
├── models/
│   ├── enums.py
│   └── models.py
│
├── routers/
│   └── ...
│
├── services/
│   ├── file_service.py
│   ├── chunking_service.py
│   ├── embeddings_service.py
│   ├── qdrant_service.py
│   ├── bm25_service.py
│   ├── retriever.py
│   ├── fusion_service.py
│   ├── reranker_service.py
│   ├── retrieval_service.py
│   ├── query_transformation_service.py
│   ├── router_service.py
│   ├── parent_child_service.py
│   ├── conversation_service.py
│   ├── generation_service.py
│   └── llm_service.py
│
└── main.py
```

---

# Technology Stack

| Technology              | Purpose                         |
| ----------------------- | ------------------------------- |
| Python                  | Main programming language       |
| FastAPI                 | API/backend                     |
| Qdrant                  | Vector database                 |
| Sentence Transformers   | Embeddings and reranking        |
| `multilingual-e5-large` | Embedding model                 |
| BM25                    | Keyword retrieval               |
| RRF                     | Retrieval result fusion         |
| Cross-Encoder           | Reranking                       |
| SQLite                  | Persistent conversation storage |
| SQLAlchemy              | Database ORM                    |
| PyPDF                   | PDF text extraction             |
| LLM API                 | Answer generation               |

---

# Configuration

The project uses environment-based configuration.

Example:

```env
QDRANT_HOST=localhost
QDRANT_PORT=7000
QDRANT_COLLECTION_NAME=documents

EMBEDDING_MODEL_NAME=intfloat/multilingual-e5-large
EMBEDDING_DIMENSION=1024
EMBEDDING_DISTANCE=Cosine

CHUNK_METHOD=parent_child
CHUNK_SIZE=500
CHUNK_OVERLAP=100
CHUNK_OVERLAP_SENTENCES=1

SEMANTIC_CHUNK_PERCENTILE=25

PARENT_CHUNK_SIZE=300
CHILD_CHUNK_SIZE=100
```

API keys should be stored in `.env` and **must not be committed to GitHub**.

---

# Qdrant

Qdrant runs locally using Docker.

Example configuration:

```yaml
services:
  qdrant:
    image: qdrant/qdrant
    container_name: qdrant
    ports:
      - "7000:6333"
```

Start Qdrant:

```bash
docker compose up -d
```

The application connects to Qdrant through:

```text
localhost:7000
```

---

# Running the Project

## 1. Clone the repository

```bash
git clone <your-repository-url>
cd <your-repository>
```

## 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure environment variables

Create a `.env` file and add the required configuration and API keys.

## 5. Start Qdrant

```bash
docker compose up -d
```

## 6. Start FastAPI

For example:

```bash
uvicorn app.main:app --reload
```

The API documentation will then be available through FastAPI's Swagger interface.

---

# Design Principles

### 1. Retrieval before generation

The fundamental principle of this project is:

> **Retrieve the right evidence first, then generate an answer from that evidence.**

### 2. Retrieval should be adaptive

Different questions can require different retrieval strategies.

```text
Simple question
    → Normal retrieval

Complex question
    → Decomposition

Ambiguous question
    → Query rewriting

Broad question
    → Multi-query retrieval
```

### 3. Retrieval and generation are separate

The project keeps retrieval and generation as separate stages:

```text
Query
 ↓
Retrieval
 ↓
Context
 ↓
Generation
```

This makes it easier to experiment with different retrieval strategies without rewriting the generation system.

### 4. Parent-child retrieval separates precision from context

Children are optimized for retrieval precision.

Parents provide broader context for generation.

```text
Child → retrieval precision
Parent → contextual coverage
```

### 5. Persistence belongs outside the retrieval pipeline

Conversation history is handled by the conversation/database layer rather than being mixed into the retrieval implementation.


# Learning Goals

This project was built as a practical exploration of advanced RAG concepts.

<img width="1536" height="1024" alt="diagram" src="https://github.com/user-attachments/assets/b0b71f0c-d32e-499f-89a4-2e6b62afda0b" />


