# Local Multimodal Document AI (Jina + Chroma + Ollama)

## Overview

This project is a fully local multimodal Retrieval-Augmented Generation
(RAG) system that allows you to:

-   Chat with your documents
-   Search PDFs semantically
-   Understand images and screenshots
-   Process scanned PDFs
-   Run everything completely offline
-   Avoid sending sensitive data to cloud APIs

The system uses modern open-source AI infrastructure to provide a
private document intelligence assistant running entirely on your own
machine.

------------------------------------------------------------------------

## Core Capabilities

This project enables:

-   Local semantic search over documents
-   Chatting with PDFs, images, and notes
-   Multimodal embeddings (text + images)
-   Persistent vector storage
-   Automatic document ingestion
-   Chunk-level retrieval accuracy
-   Fully offline execution
-   No OpenAI API required
-   No external embedding services required

------------------------------------------------------------------------

## Technology Stack

### Backend

-   Python
-   FastAPI
-   Uvicorn

### AI Models

-   jinaai/jina-embeddings-v4 (multimodal embeddings)
-   Ollama (local LLM runtime)
-   Local reasoning model via Ollama (configurable)

### Vector Database

-   ChromaDB (persistent local vector storage)

### Document Processing

-   PyMuPDF (PDF parsing + rendering)
-   Pillow (image handling)

### Infrastructure

-   Docker
-   Docker Compose

### Developer Tools

-   VS Code
-   Git

------------------------------------------------------------------------

## Supported Document Types

The system supports:

-   PDF files
-   Scanned PDFs
-   PNG images
-   JPG images
-   JPEG images
-   Text files
-   Markdown files
-   Screenshots
-   Mixed text/image documents

------------------------------------------------------------------------

## Architecture

The system follows a layered architecture structure:

    FastAPI Application
        |
    Routers
        |
    Services
        |
    Processor Factory
        |
    Document Processors
        |
    Embedding Service
        |
    Vector Store (ChromaDB)
        |
    Local LLM (Ollama)

### Core Layers

#### API Layer

Routers:

-   health
-   ingest
-   documents
-   search
-   chat
-   ui

#### Application Layer

Services:

-   ingestion_service
-   search_service
-   chat_service
-   startup_service

#### Domain Layer

Interfaces:

-   document_processor

Models:

-   ingest_item

Services:

-   chunking_service

#### Infrastructure Layer

Components:

-   jina_embedder
-   chroma_vector_store
-   json_state_repository
-   processor_factory
-   pdf_processor
-   image_processor
-   text_processor

------------------------------------------------------------------------

## How the Pipeline Works

    Documents Folder
        |
    ProcessorFactory
        |
    Document Processors
        |
    Chunking Service
        |
    Jina Embeddings v4
        |
    Chroma Vector Database
        |
    Ollama Local Model
        |
    Answer Generation

------------------------------------------------------------------------

## How Embeddings Work

The system generates embeddings for:

-   text
-   images
-   PDF pages rendered as images
-   mixed content

This enables semantic understanding across multiple content types.

------------------------------------------------------------------------

## Project Structure

    app/
        api/
        application/
        domain/
        infrastructure/
        shared/

Each layer has a clear responsibility following clean architecture
principles.

------------------------------------------------------------------------

## Configuration

Key configuration values include:

AUTO_INGEST_ON_STARTUP

CHROMA_DIR

COLLECTION_NAME

DATA_DIR

DOCS_FOLDER

MODEL_NAME

STATE_FILE

IMAGE_DPI_SCALE

IMAGE_EXTENSIONS

These values control ingestion behavior, storage paths, and embedding
configuration.

------------------------------------------------------------------------

## Running the Project

### Step 1

Install Docker Desktop

### Step 2

Clone repository

    git clone <your-repo-url>

### Step 3

Start services

    docker compose up --build

### Step 4

Open browser

    http://localhost:8000

------------------------------------------------------------------------

## Automatic Document Ingestion

When enabled:

    AUTO_INGEST_ON_STARTUP = True

The system automatically processes files inside the configured documents
folder during startup.

------------------------------------------------------------------------

## Persistent Storage

The system stores vectors locally inside:

    CHROMA_DIR

This ensures embeddings remain available between restarts.

------------------------------------------------------------------------

## Privacy Benefits

Because everything runs locally:

-   Documents never leave your machine
-   No cloud embedding APIs are used
-   No external inference calls are required
-   Sensitive files remain private

------------------------------------------------------------------------

## Example Use Cases

This system supports:

-   Private document search
-   Local research assistants
-   Internal company knowledge bases
-   Offline AI workflows
-   Financial document analysis
-   Resume parsing
-   Contract review assistance
-   Screenshot understanding

------------------------------------------------------------------------

## Hardware Requirements

Minimum:

-   16 GB RAM recommended
-   SSD storage
-   Modern CPU

Optional:

-   NVIDIA GPU for faster local model inference

------------------------------------------------------------------------

## Future Extensions

Possible improvements include:

-   document classification
-   metadata tagging
-   UI enhancements
-   streaming responses
-   multi-user support
-   authentication layer
-   advanced retrieval filters
