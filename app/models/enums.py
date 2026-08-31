
from enum import Enum


class ChunkMethod(str, Enum):
    FIXED = "fixed"
    PUNCTUATION = "punctuation"
    RECURSIVE = "recursive"
    SEMANTIC = "semantic"