#!/usr/bin/env python3

from sklearn.metrics.pairwise import cosine_similarity
from ollama import Client


# Load your documents
documents = [
    "Document 1 content here.",
    "Document 2 content here.",
    "What kind of integer overflow is undefined behaviour in C++\n---\nsigned integer overflow",
    "What is another hash collision strategy apart from open addressing?\n---\nseparate chaining"
]

OLLAMA_PORT = 11434
DOCKER_LOCALHOST = "http://host.docker.internal"

# Initialize Ollama client
client = Client(
  host=f"{DOCKER_LOCALHOST}:{OLLAMA_PORT}",
)

# Function to generate embeddings for a document
def generate_embeddings(doc):
    response = client.embed("all-minilm", doc)
    return response['embeddings'][0]

# Generate embeddings for all documents
embeddings = [generate_embeddings(doc) for doc in documents]

simils = cosine_similarity(embeddings)
print(simils)
