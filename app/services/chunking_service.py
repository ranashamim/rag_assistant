import uuid
import re
import numpy as np


# =====================================
# Utility
# =====================================

def build_chunk_objects(chunks, source, page, method):

    output = []

    for i, chunk in enumerate(chunks):

        output.append({

            "chunk_id": str(uuid.uuid4()),

            "text": chunk,

            "source": source,

            "page": page,

            "chunk_index": i,

            "method": method,

            "char_count": len(chunk),

            "word_count": len(chunk.split())

        })

    return output


# =====================================
# Fixed Size
# =====================================

def fixed_size_chunk(text, chunk_size=500, overlap=100):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunks.append(text[start:end])

        start = end - overlap

    return chunks


# =====================================
# Punctuation Chunk
# =====================================

def punctuation_chunk(text, chunk_size=500, overlap=100):

    sentences = re.split(r'(?<=[.!?]) +', text)

    chunks = []

    current = ""

    for s in sentences:

        candidate = current + " " + s if current else s

        if len(candidate) <= chunk_size:

            current = candidate

        else:

            chunks.append(current)

            current = current[-overlap:] + " " + s

    if current:

        chunks.append(current)

    return chunks



# =====================================
# Master function
# =====================================

def chunk_document(
    text=None,
    sentences=None,
    embeddings=None,
    source="unknown",
    page=0,
    method="punctuation",
    chunk_size=500,
    overlap=100
):

    if method == "fixed":

        chunks = fixed_size_chunk(text, chunk_size, overlap)

    elif method == "punctuation":

        chunks = punctuation_chunk(text, chunk_size, overlap)

    else:

        raise ValueError("Invalid chunk method")


    return build_chunk_objects(chunks, source, page, method)