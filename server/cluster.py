#!/usr/bin/env python3

import logging
from sklearn.metrics.pairwise import cosine_similarity
from ollama import Client

OLLAMA_PORT = 11434
OLLALA_EMBEDDINGS_MODEL = "all-minilm"
DOCKER_LOCALHOST = "http://host.docker.internal"

# Initialize Ollama client
client = Client(
  host=f"{DOCKER_LOCALHOST}:{OLLAMA_PORT}",
)
# Configure the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def healthcheck():
    return client.list()


def generate_embeddings(card):
    try:
        response = client.embed(OLLALA_EMBEDDINGS_MODEL, card)
        return response['embeddings'][0]  # Extract the embedding
    except Exception as e:
        # Log the error using the logger from app.py
        logger.error(f"Error generating embedding for card: {card}. Error: {e}")
        return None


def get_cosine_similarity_matrix(cards):
    # Generate embeddings, skipping cards with failed embeddings
    embeddings = []
    valid_cards = []
    for card in cards:
        embedding = generate_embeddings(card["content"])
        if embedding is not None:
            embeddings.append(embedding)
            valid_cards.append(card)

    if not embeddings:
        # Handle case where no valid embeddings are generated
        logger.error("No valid embeddings generated. Returning an empty similarity matrix.")
        return [], valid_cards

    # Compute cosine similarity matrix for valid embeddings
    simils = cosine_similarity(embeddings)
    return simils, valid_cards


def make_links(cards):
    # Get the cosine similarity matrix and the list of valid cards
    similarity_matrix, valid_cards = get_cosine_similarity_matrix(cards)

    # Handle empty similarity matrix
    if similarity_matrix.size == 0:
        logger.error("No valid links can be created. Returning an empty list.")
        return []

    # Create links based on cosine similarity > 0.8
    links = []
    for i, card in enumerate(valid_cards):
        for j, other_card in enumerate(valid_cards):
            if i != j and similarity_matrix[i][j] > 0.8:
                links.append({'source': card['id'], 'target': other_card['id']})

    return links


