import re
import uuid


# =====================================
# Utility
# =====================================

def build_chunk_objects(chunks, page_number, source, file_type, method):
    output = []

    for i, chunk in enumerate(chunks):
        if not chunk:
            continue

        output.append({
            "chunk_id": str(uuid.uuid4()),
            "text": chunk,
            "source": source,
            "file_type": file_type,
            "page_number": page_number,
            "chunk_index": i,
            "method": method
        })

    return output


# =====================================
# Validation
# =====================================

def validate_chunk_parameters(chunk_size, overlap):
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if overlap < 0:
        raise ValueError("overlap cannot be negative")

    if overlap >= chunk_size:
        raise ValueError(
            "overlap must be smaller than chunk_size"
        )


# =====================================
# Fixed Size Chunking
# =====================================

def fixed_size_chunk(text, chunk_size=500, overlap=100):
    validate_chunk_parameters(chunk_size, overlap)

    if not text:
        return []

    chunks = []

    step = chunk_size - overlap

    for start in range(0, len(text), step):
        chunk = text[start:start + chunk_size]

        if chunk.strip():
            chunks.append(chunk)

        if start + chunk_size >= len(text):
            break

    return chunks


# =====================================
# Sentence / Punctuation Chunking
# =====================================

def punctuation_chunk(
    text,
    chunk_size=500,
    overlap_sentences=1
):
    if not text or not text.strip():
        return []

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if overlap_sentences < 0:
        raise ValueError(
            "overlap_sentences cannot be negative"
        )

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text.strip()
    )

    sentences = [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]

    chunks = []
    current = []
    current_length = 0

    for sentence in sentences:

        # --------------------------------
        # Very long sentence
        # --------------------------------

        if len(sentence) > chunk_size:

            if current:
                chunks.append(
                    " ".join(current)
                )
                current = []
                current_length = 0

            long_sentence_chunks = fixed_size_chunk(
                sentence,
                chunk_size=chunk_size,
                overlap=0
            )

            chunks.extend(long_sentence_chunks)

            continue

        additional_length = (
            len(sentence)
            if not current
            else len(sentence) + 1
        )

        # --------------------------------
        # Fits current chunk
        # --------------------------------

        if current_length + additional_length <= chunk_size:

            current.append(sentence)
            current_length += additional_length

        # --------------------------------
        # Doesn't fit
        # --------------------------------

        else:

            if current:
                chunks.append(
                    " ".join(current)
                )

            # Keep last N sentences
            # for semantic context
            if overlap_sentences > 0:
                current = current[
                    -overlap_sentences:
                ]
            else:
                current = []

            current.append(sentence)

            current_length = len(
                " ".join(current)
            )

    # --------------------------------
    # Final chunk
    # --------------------------------

    if current:
        chunks.append(
            " ".join(current)
        )

    return chunks


# =====================================
# Recursive Chunking
# =====================================

def recursive_chunk(
    text,
    chunk_size=500,
    overlap=100,
    separators=None,
):
    if not text or not text.strip():
        return []

    validate_chunk_parameters(
        chunk_size,
        overlap
    )

    if separators is None:
        separators = [
            "\n\n",
            "\n",
            ". ",
            " ",
        ]

    def split_recursive(text, separator_index=0):

        text = text.strip()

        if not text:
            return []

        # ---------------------------------
        # Already small enough
        # ---------------------------------

        if len(text) <= chunk_size:
            return [text]

        # ---------------------------------
        # No separators left
        # ---------------------------------

        if separator_index >= len(separators):
            return fixed_size_chunk(
                text,
                chunk_size,
                overlap
            )

        separator = separators[separator_index]

        parts = text.split(separator)

        # If this separator didn't help,
        # try the next one.
        if len(parts) == 1:
            return split_recursive(
                text,
                separator_index + 1
            )

        chunks = []

        for part in parts:
            part = part.strip()

            if not part:
                continue

            if len(part) <= chunk_size:
                chunks.append(part)

            else:
                chunks.extend(
                    split_recursive(
                        part,
                        separator_index + 1
                    )
                )

        return chunks

    raw_chunks = split_recursive(text)

    # ---------------------------------
    # Combine small pieces
    # ---------------------------------

    final_chunks = []
    current = ""

    for piece in raw_chunks:

        if not current:
            current = piece
            continue

        candidate = f"{current} {piece}"

        if len(candidate) <= chunk_size:
            current = candidate

        else:
            final_chunks.append(current)

            overlap_text = get_character_overlap(
                current,
                overlap
            )

            current = (
                f"{overlap_text} {piece}".strip()
            )

    if current:
        final_chunks.append(current)

    return final_chunks


# =====================================

def get_character_overlap(text, overlap):
    if overlap <= 0:
        return ""

    if len(text) <= overlap:
        return text

    overlap_text = text[-overlap:]

    # Move forward to the next whitespace
    # so we don't start in the middle of a word.
    first_space = overlap_text.find(" ")

    if first_space != -1:
        overlap_text = overlap_text[first_space + 1:]

    return overlap_text.strip()


# =====================================
# Master Chunking Function
# =====================================
def chunk_document(
    text,
    page_number,
    file_type,
    source="unknown",
    method="semantic",
    chunk_size=500,
    overlap=100,
    overlap_sentences=1,
):
    if not text or not text.strip():
        return []

    if method == "fixed":

        chunks = fixed_size_chunk(
            text,
            chunk_size,
            overlap
        )

    elif method == "punctuation":

        chunks = punctuation_chunk(
            text,
            chunk_size,
            overlap_sentences
        )

    elif method == "recursive":

        chunks = recursive_chunk(
            text,
            chunk_size,
            overlap
        )

    elif method == "semantic":
        from app.services.semantic_chunking_service import semantic_chunk
        
        chunks = semantic_chunk(
                text,
                percentile=25
            )
        
    else:
        raise ValueError(
            f"Invalid chunk method: {method}"
        )

    return build_chunk_objects(
        chunks,
        page_number,
        source,
        file_type,
        method
    )

