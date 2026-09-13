
from enum import Enum


class ChunkMethod(str, Enum):
    FIXED = "fixed"
    PUNCTUATION = "punctuation"
    RECURSIVE = "recursive"
    SEMANTIC = "semantic"
    PARENT_CHILD = "parent_child"