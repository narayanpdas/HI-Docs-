# HIDocs: A production-grade Retrieval-Augmented Generation (RAG) platform decoupled from notebook environments.

## Test in Production : LINK...

## ℹ️ About HIDocs:

HIDocs is a high-performance web application engineered to facilitate semantic search and QA over unstructured documents. Built on FastAPI, it leverages the RAG (Retrieval-Augmented Generation) architecture to ground LLM responses in factual data.

Unlike standalone LLMs which are prone to hallucinations, HIDocs ensures deterministic and verifiable outputs by retrieving context directly from the source material before generation.

## Architectural Motivation:

**Why build this?** While tools like NotebookLM exist, they function as "black boxes" with data privacy concerns. Conversely, most open-source tutorials rely on monolithic Jupyter Notebooks that lack scalability.

HIDocs bridges this gap by providing:

- Full Data Sovereignty: A self-hosted alternative where user data never leaves the encrypted container.

- Production Architecture: Moving beyond scripts to a modular, API-first design (Router-Service-Model pattern).

- Security: Implementing strict API key validation and Pydantic-based schema enforcement.

## 🎯 The Goal:

The primary objective is to demonstrate a scalable RAG pipeline that prioritizes:

- **Asynchronous Ingestion:** Utilizing FastAPI BackgroundTasks to handle heavy PDF parsing without blocking the main thread.

![Ingestion Pipeline]()
_(Description: Document Ingestion Loop for duplication-proof, instant feedback and backgroundTask Processing capability.)_

- **RAG Retrieval Loop:**
  The chat engine uses WebSockets for real-time latency. It retrieves context chunks from ChromaDB and injects them into the LLM context window dynamically.

![Chat Flow](link_to_your_chat_flow_image_here)
_(Description: WebSocket communication loop verifying API keys and querying the RAG engine)_

- **Type Safety and Segregated Endpoint Design:** Strict validation using Pydantic to prevent runtime errors as well as structured endpoints for better developement cycle.

![Endpoints](link_to_your_endpoint_flow_image_here)
_(Description: All Endpoints with their brief functions)_

- **Modular Design:** A clean separation of concerns (Ingestion, Embedding, Retrieval) for maintainability, via Engine like design pattern.

## ⚙️ Tech Stack:

### Server-Side:

- python(3.11)
- FastAPI
- SQLAlchemy
- Langchain
- Pytorch and Transformers
- ChromaDb
- Sqlite
- Docker

### For the WebUI:

- React with ChakraUI (TypeScript)

## 🚀 Getting Started:

### Prerequisites

- Python 3.11+
- Docker (optional, for containerized deployment)

1. **Clone the Repository**

   ```bash
   git clone [https://github.com/narayanpdas/HI-Docs-.git](https://github.com/narayanpdas/HI-Docs-.git)

   cd HIDocs
   ```

2. **Backend Setup:**

   ```bash
   cd ./Backend
   pip install -r requirements.txt
   fastapi dev main.py
   ```

   For Production Mode:

   ```bash
    fastapi run main.py
   ```

3. **Backend(Docker-Version):**

   ```bash
   docker-compose up --build
   ```

4. **Frontend Setup:(Optional if UI interface is required):**
   ```bash
   cd ./Frontend
   npm install
   npm run dev
   ```
   For Production Mode (with an appropirate server):
   ```bash
   npm run build
   ```

## Version Features(Current Version:1):

- Optimized for text-heavy PDF (High-accuracy parsing for contracts, research papers, and documentation).

- Implemented 3 types of search options for broader,specific and Comprehensive searches.

- Customized Search Option (User can Choose which Pdfs to search through).

## Currently Working (💡Future Ideas):

Server & Infrastructure:

- Multiple document type Support for .docx and .md ingestion.

- API DashBoard: Token usage tracking and analytics.

- Redis Caching: Caching frequent semantic queries for low-latency responses.

- SSE (Server-Sent Events): Real-time upload status tracking.

RAG Engine Based:

- More Optimized and faster search with Hybrid structure(Semantic + Keyword(BM25) ).

- Better Chunking and embedding with intelligent systems to recognize and use Tables, images, links etc in the document.
