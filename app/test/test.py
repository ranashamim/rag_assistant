
def create_child_chunks(parent_text, child_size):

    if not parent_text:
        return []

    children_chunks = []

    tokens = parent_text.split()

    for start in range(0, len(tokens), child_size):
        child_tokens = tokens[start:start + child_size]
        child_chunk = " ".join(child_tokens)

        if child_chunk.strip():
            children_chunks.append(child_chunk)

    return children_chunks



print(create_child_chunks("one two three four five", 10))