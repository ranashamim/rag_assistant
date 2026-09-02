from app.services.chunking_service import recursive_chunk
import numpy as np
import re

from app.config.settings import settings

from app.services.embeddings_service import model



def split_sentences(text):
    if not text or not text.strip():
        return []

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text.strip()
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def embed_sentences(sentences):
    if not sentences:
        return []

    texts = [
        f"passage: {sentence}"
        for sentence in sentences
    ]

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=False,
    )

    return embeddings

def calculate_similarities(embeddings):
    similarities = []

    for i in range(len(embeddings) - 1):

        similarity = np.dot(
            embeddings[i],
            embeddings[i + 1]
        )

        similarities.append(
            float(similarity)
        )

    return similarities

def find_breakpoints(
    similarities,
    strategy="std",
    percentile=25
):

    if not similarities:
        return []

    if strategy == "percentile":

        threshold = np.percentile(
            similarities,
            percentile
        )

    else:

        mean = np.mean(similarities)
        std = np.std(similarities)

        threshold = mean - std

    return [
        i
        for i, similarity in enumerate(similarities)
        if similarity <= threshold
    ]


def merge_small_chunks(
    chunks,
    min_chunk_chars=200
):

    if not chunks:
        return []

    merged = []

    current = chunks[0]

    for next_chunk in chunks[1:]:

        if len(current) < min_chunk_chars:

            current += " " + next_chunk

        else:

            merged.append(current)

            current = next_chunk

    merged.append(current)

    return merged


def split_large_chunks(
    chunks,
    max_chunk_chars=1000,
    overlap=100
):

    final_chunks = []

    for chunk in chunks:

        if len(chunk) <= max_chunk_chars:

            final_chunks.append(chunk)

        else:

            recursive_chunks = recursive_chunk(
                text=chunk,
                chunk_size=max_chunk_chars,
                overlap=overlap
            )

            final_chunks.extend(
                recursive_chunks
            )

    return final_chunks

def create_semantic_chunks(
    sentences,
    breakpoints
):
    if not sentences:
        return []

    chunks = []

    start = 0

    for breakpoint in breakpoints:

        chunk = sentences[
            start:breakpoint + 1
        ]

        if chunk:
            chunks.append(
                " ".join(chunk)
            )

        start = breakpoint + 1

    # Remaining sentences
    if start < len(sentences):
        chunks.append(
            " ".join(sentences[start:])
        )

    return chunks

def semantic_chunk(
    text,
    percentile=25,
    min_chunk_chars=200,
    max_chunk_chars=1000
):

    sentences = split_sentences(text)

    if len(sentences) <= 1:
        return build_metadata(
            sentences,
            method="semantic"
        )

    embeddings = embed_sentences(
        sentences
    )

    similarities = calculate_similarities(
        embeddings
    )

    breakpoints = find_breakpoints(
        similarities,
        strategy="std",
        percentile=percentile
    )

    chunks = create_semantic_chunks(
        sentences,
        breakpoints
    )

    chunks = merge_small_chunks(
        chunks,
        min_chunk_chars
    )

    chunks = split_large_chunks(
        chunks,
        max_chunk_chars
    )

    return chunks
